# Client.py

import docker
import docker.tls as tls
import os
import scMetadata

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

    def info(self):
        print "Now we can have an awesome smart cake"
        super(scClient, self).info()

    def commit(self, container, repository=None, tag=None, message=None,
               author=None, conf=None):
        self.dcli.commit(container=container, repository=repository, tag=tag, message=message,
                         author=author, conf=conf)
