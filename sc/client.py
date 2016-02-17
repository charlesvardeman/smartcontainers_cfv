# Client.py

import docker
import docker.tls as tls
import os
import scMetadata
import io
import pprint
import tempfile
import tarfile
import provinator
import re
import json
import ast

class scClient(docker.Client):
    def __init__(self, *args, **kwargs):
        super(scClient, self).__init__(*args, **kwargs)

        # Test configuration for docker-machine. We need a way
        # to set the sockets file if on linux.
        # Get command line arguments for DOCKER HOST
        docker_host = os.environ["DOCKER_HOST"]
        docker_cert_path = os.environ["DOCKER_CERT_PATH"]
        docker_machine_name = os.environ["DOCKER_MACHINE_NAME"]

        # Build tls information

        tls_config = tls.TLSConfig(
            client_cert=(os.path.join(docker_cert_path, 'cert.pem'), os.path.join(docker_cert_path,'key.pem')),
            ca_cert=os.path.join(docker_cert_path, 'ca.pem'),
            verify=True,
            assert_hostname = False
        )
        # Replace tcp: with https: in docker host.
        docker_host_https = docker_host.replace("tcp","https")
        self.dcli = docker.Client(base_url=docker_host_https, tls=tls_config)

        self.scmd = scMetadata.scMetadata()
        self.provfilepath = "/SmartContainer/"
        self.provfilename = "SCProv.jsonld"
        self.label_prefix = "smartcontainer"


    def info(self):
        print "Now we can have an awesome smart cake"
        super(scClient, self).info()

    def commit(self, container, repository=None, tag=None, message=None,
               author=None, conf=None):
        if self.hasProv(container,self.provfilename,self.provfilepath):
            #Retrieve provenance file from the container
            self.fileCopyOut(container,self.provfilename, self.provfilepath)
            #Append provenance data to file
            self.scmd.appendData(self.provfilename)
            #Copy provenance file back to the container
            self.fileCopyIn(container, self.provfilename, self.provfilepath)
            #Remove the local copy of the provenance file
            os.remove(self.provfilename)
            os.remove('temp.tar')
            # #Commit the container changes
            newImage = self.dcli.commit(container=container, repository=repository, tag=tag, message=message,
                         author=author, conf=conf)
            #print(newImage['Id'])
            thisID = newImage['Id']
            #Get the label information from provinator
            provOutput = provinator.get_commit_label()
            provOutput = re.sub('[\t\r\n\s+]', '', provOutput)
            newLabel =  "{'" + self.label_prefix + "':'" + provOutput + "'}"
            newLabel = ast.literal_eval(newLabel)
            #Write the label to the new image
            newContainer = self.dcli.create_container(image=thisID, command="/bin/bash", labels=newLabel)
            self.dcli.commit(container=newContainer,repository=repository,tag=tag, message=message, author=author, conf=conf)
            self.dcli.remove_container(newContainer)

        else:
            pass

    def fileCopyOut(self, containerid, filename, path):
        tarObj, stats = self.dcli.get_archive(container=containerid,path=path + filename)
        with open('temp.tar', 'w') as destination:
            for line in tarObj:
                destination.write(line)
            destination.seek(0)
            thisTar = tarfile.TarFile(destination.name)
            thisTar.extract(self.provfilename)

    def fileCopyIn(self, containerid, filename, path):
        with self.simple_tar(filename) as thisTar:
            self.dcli.put_archive(containerid, path, thisTar)

    def hasProv(self, containerid, filename, path):
        execid = self.dcli.exec_create(container=containerid, stdout=True, cmd='ls ' + path)
        text = self.dcli.exec_start(exec_id=execid)
        if 'SCProv.jsonld' in text:
            return True
        return False

    def simple_tar(self, path):
        f = tempfile.NamedTemporaryFile()
        t = tarfile.open(mode='w', fileobj=f)

        abs_path = os.path.abspath(path)
        t.add(abs_path, arcname=os.path.basename(path), recursive=False)

        t.close()
        f.seek(0)
        return f