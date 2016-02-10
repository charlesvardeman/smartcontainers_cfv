from util import which
from sarge import Command, Capture, get_stdout, get_stderr, capture_stdout
from io import TextIOWrapper
import re
import json
import subprocess
import time
import datetime
import socket
import os
import random
import provinator
import docker.tls as tls
import docker
import client

# We need to docker version greater than 1.6.0 to support
# the label functionality.
min_docker_version = '1.6.0'

# Default docker commands that sc can handle.
snarf_docker_commands = ['commit', 'build', 'stop', 'run']
# Default docker label key where smart container graph is stored.
smart_container_key = 'sc'


class Error(Exception):
    """Base class for docker module exceptions"""
    pass


class DockerNotFoundError(RuntimeError):
    """Exception raised for missing docker command.

    Attributes:
        msg -- explaination of error
    """

    def __init__(self, msg):
        msg = "Please make sure docker is installed and in your path."
        self.arg = msg


class DockerInsuficientVersionError(RuntimeError):
    """Exception raised for wrong version of docker command."""

    def __init__(self, msg):
        msg = "Please make sure docker is greater than %s" % min_docker_version
        self.arg = msg


class DockerServerError(RuntimeError):
    def __init__(self, msg):
        msg = "Cannot connect to server"
        self.arg = msg


class DockerImageError(RuntimeError):
    def __init__(self, msg):
        msg = "No docker image specified or found."
        self.arg = msg

class DockerInputError(RuntimeError):
    def __init__(self, msg):
        msg = "Invalid input identified"
        self.arg = msg

class DockerCli:
    def __init__(self, command):
        self.command = command
        self.label_prefix = "smartcontainer"
        self.location = self.find_docker()
        self.imageID = None
        self.container = None
        self.metadata = {}
        self.smartcontainer = {}
        self.provfilename = "SCProv.jsonld"
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
        self.dcli = client.scClient(base_url=docker_host_https, tls=tls_config)
        #print self.dcli.info()
    def sanity_check(self):
        """sanity_check checks existence and executability of docker."""
        if self.location is None:
            self.find_docker()
        self.check_docker_version()
        self.check_docker_connection()

    def find_docker(self):
        """find_docker searches paths and common directores to find docker."""
        location = which("docker")
        if location is None:
            raise DockerNotFoundError("Please make sure docker is installed "
                                      "and in your path")
        return location

    def check_docker_version(self, min_version=min_docker_version):
        """check_docker_version makes sure docker is of a min version"""
        output = get_stdout('docker --version')
        # in docker 1.7.1 version is at 2 position in returned string
        version = output.split()[2]
        # remove comma from out put if in string
        if ',' in version:
            version = version[:-1]
        if self.ver_cmp(version, min_version) < 0:
            raise DockerInsuficientVersionError(
                "Please  make sure docker is greater than %s" % min_version)

    def check_docker_connection(self):
        output = get_stdout('docker images')
        # This checks if we can get a connection to the remote docker
        # server. It assumes the output of the "docker images"" command is
        # of the form: "Get http:///var/run/docker.sock/v1.19/images/json: dial
        # unix /var/run/docker.sock: no such file or directory. Are you trying
        # to connect to a TLS-enabled daemon without TLS?"
        if 'IMAGE ID' not in output:
            raise DockerServerError("Docker cannot connect to daemon")

    def do_command(self):
        """do_command is main entry point for capturing docker commands"""
        # First run the command and capture the output.
        # For efficiency this should probably change such that
        # if a command doesn't have a capture handler we execute
        # the command uncaptured. Most commands are going to be captured
        # for provenance, so this efficiency concern is probably moot.

        if self.location is None:
            self.find_docker()
        cmd_string = str(self.location) + ' ' + self.command
        capture_flag = False
        print cmd_string

        for name in snarf_docker_commands:
            if name in self.command:
                if name == 'build':
                    self.capture_cmd_build(cmd_string) #Captures information from logs.
                    capture_flag = True
                elif name == 'commit':
                    self.capture_cmd_commit(cmd_string)
                    capture_flag = True
                elif name == 'run':
                    #Execute some procedure
                    capture_flag = True
                elif name == 'stop':
                    #Execute some procedure
                    capture_flag = True
        if not capture_flag:
            #print 'here'
            subprocess.call(cmd_string, shell=True)

    def capture_command(self):
        pass

    def capture_cmd_build(self,cmd_string):
        output = capture_stdout(cmd_string)
        print output.stdout
        print 'build'
        #pass

    def capture_cmd_commit(self,cmd_string):
        #Initialize variables
        hasProv = False

        #Parse the command string to get the container id
        #command = cmd_string.rsplit(' ', 1) [0]
        container_id = cmd_string.rsplit(' ', -1) [2]
        new_name_tag = cmd_string.rsplit(' ', -1) [3]
        if ':' in new_name_tag:
            new_name = new_name_tag.rsplit(':', -1) [0]
            new_tag = new_name_tag.rsplit(':', -1) [1]
        else:
            new_name = new_name_tag
            new_tag = ''
        print new_name
        #
        file = capture_stdout("docker exec " + container_id + " ls /SmartContainer/")
        for line in file.stdout:
            if self.provfilename in line:
                hasProv = True
        if hasProv:
            #Retrieve provenance file from the container
            copy_cmd =  str(self.location) + ' cp ' + container_id + ":/SmartContainer/" + self.provfilename + " ."
            rm_container = Command(copy_cmd)
            rm_container.run()
            #Append provenance data to file
            self.add_prov_data(container_id)
            #Copy provenance file back to the container
            copy_cmd =  str(self.location) + ' cp ' + self.provfilename + " " + container_id + ":/SmartContainer/" + self.provfilename
            rm_container = Command(copy_cmd)
            rm_container.run()
            #Remove the local copy of the provenance file
            os.remove(self.provfilename)
            self.container_save_as(container_id, new_name, new_tag)
            #Build new label string... information from Chuck needed.
            new_label_string = provinator.get_commit_label()
            #Write string to new image using put_label_image
            image_id = self.get_imageID(new_name)
            #print image_id
            self.set_image(image_id)
            self.put_label_image(new_label_string)
        else:
            pass

        #image_name = cmd_string.rsplit(' ', 1) [1]
        #image_id = self.get_imageID(image_name)
        #self.set_image(image_id)
        #label = self.get_label()
        #run_time = str(datetime.datetime.now())
        #host_name = socket.gethostname()
        #this_user = os.getlogin()
        #prev_container = self.get_prev_container()
        #docker_path = str(self.location)
        #docker_version = self.get_docker_version()
        #hash = random.getrandbits(32)
        #prev_label = self.get_label()
        #print "hash value: %08x" % hash
        #subprocess.Popen(cmd_string, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        #time.sleep(1)
        #container_id = self.get_containerID(image_name)
        #print 'CID:' + container_id
        #print 'commit'

    def add_prov_data(self,container_id):
        with open('SCProv.jsonld', 'a') as provfile:
            # provfile.write('<sc:' + str(random.getrandbits(32)) + '> a prov:Image ;\n')
            # provfile.write('\trdfs: label "image updated programmatically"\n')
            # provfile.write('\tprov:wasAttributedTo <http://orcid.org/0000-0003-4091-6059>;\n')
            # provfile.write('\tprov:wasGeneratedBy <sc:' + str(self.get_containerImage(container_id)) + '>.\n')
            provfile.write(provinator.get_commit_data())

    def put_label_image(self, label):
        """put_label attaches json metadata to smartcontainer label"""

        # Due to the structure of docker, we have to do this in a series of
        # steps. This method attaches a label to a image by creating a
        # temporary container with a label using docker run. We then save that
        # container to a new image with the same.

        # Only proceed if the input string is valid Json
        if self.validate_json(label):
            if self.imageID is not None:

                # First get tag and name for image id passed to method
                repository, tag = self.get_image_info()

                # Now "attach" the label by running a new container from the imageID
                # Not using do_command because of potential for endless looping if we are writing labels
                # in the capture_cmd_workflow routine.
                label_cmd_string = str(self.location) + " run --name=labeltmp --label=" + \
                                  self.label_prefix + "='" + label + "' " + self.imageID + " /bin/echo"
                subprocess.call(label_cmd_string, shell=True)
                # label_cmd_string = " run --name=labeltmp --label=" + \
                #                    self.label_prefix + "='" + label + "' " + imageID + " /bin/echo"
                # self.set_command(label_cmd_string)
                # self.do_command()

                # Save container with new label to new image with previous repo and tag
                self.container_save_as('labeltmp', repository, tag)

                # Stop the running container so it can be removed
                self.stop_container('labeltmp')

                # remove temporary container
                self.remove_image('labeltmp')
            else:
                raise DockerInputError("Image ID invalid")
        else:
            raise DockerInputError("Not a valid Json string")

    def container_save_as(self, name, saveas, tag):
        """ Saves a container to a new image
        :param name: the name of the container to be saved
        :param saveas: the name of the image to be created
        :param tag: the tag attached to the new image
        :return: none
        """
        commit_cmd_string = str(self.location) + ' commit ' + name + ' ' + saveas
        if tag != "":
            commit_cmd_string = commit_cmd_string + ':' + tag
        commit = Command(commit_cmd_string)
        commit.run()

    def stop_container(self, name):
        """ stops a specified container
        :param name: name of the container to stop
        :return:none
        """
        stop_container_string = str(self.location) + ' stop ' + name
        stop_container = Command(stop_container_string)
        stop_container.run()

    def remove_image(self, name):
        """ removes a named image
        :param name: the name of the image to be removed
        :return: none
        """
        rm_container_string = str(self.location) + ' rm ' + name
        rm_container = Command(rm_container_string)
        rm_container.run()

    def validate_json(self,jsonString):
        """ validate_json performs a simple test of validity by attempting a load of the string
        :param jsonString:
        :return: true if successful
        """
        try:
            json_object = json.loads(jsonString)
        except ValueError, e:
            return False
        return True


    def get_label(self):
        """get_label returns smartconainer json string from docker image or container"""
        self.get_metadata()

        if bool(self.metadata):
            AllDictionary = json.loads(self.metadata)
            ConfigDictionary = AllDictionary["Config"]
            label = ConfigDictionary["Labels"]
        return label

    def get_prev_container(self):
        """
        :return: Container ID of previous container from docker image
        """
        self.get_metadata()

        if bool(self.metadata):
            AllDictionary = json.loads(self.metadata)
            #ConfigDictionary = AllDictionary["Config"]
            container = AllDictionary["Container"]
        return container

# Quick hack to get image id for current phusion/baseimage
# for testing purposes. We assume that the image has already
# been pulled from the docker hub repo.
    def get_imageID(self, image):
        # default_container = "phusion/baseimage"
        imageID = None
        docker_command = str(self.location) + ' images'
        output = capture_stdout(docker_command)
        for line in TextIOWrapper(output.stdout):
            if image in repr(line):
                imageID = line.split()[2]
        if imageID is None:
            raise DockerImageError('No Image')
        return imageID

    def get_containerID(self, image):
        containerID = None
        docker_command = str(self.location) + ' ps -a'
        #print docker_command
        output = capture_stdout(docker_command)
        for line in TextIOWrapper(output.stdout):
            if image in repr(line):
                containerID = line.split()[0]
        if containerID is None:
            raise DockerImageError('No Container')
        return containerID

    def get_containerImage(self, containerID):
        imageName = None
        docker_command = str(self.location) + ' ps -a'
        #print docker_command
        output = capture_stdout(docker_command)
        for line in TextIOWrapper(output.stdout):
            if containerID in repr(line):
                imageName = line.split()[1]
        if imageName is None:
            raise DockerImageError('No Image for Container')
        return imageName

    def get_docker_version(self):
        docker_version = None
        docker_command = str(self.location) + " version --format '{{.Server.Version}}'"
        output = capture_stdout(docker_command)
        for line in TextIOWrapper(output.stdout):
            docker_version = line
        return docker_version

    def get_image_info(self):
        docker_command = str(self.location) + ' images'
        output = capture_stdout(docker_command)
        if self.imageID is not None:
            for line in TextIOWrapper(output.stdout):
                if self.imageID in repr(line):
                    repository = line.split()[0]
                    tag = line.split()[1]
            return repository, tag
        else:
            raise DockerImageError



# Each image has a metadata record. This returns a list of all label
# strings contained in the metadata.
    def get_metadata(self):
        docker_command = str(self.location) + ' inspect ' + self.imageID
        p = Command(docker_command, stdout=Capture(buffer_size=-1))
        p.run()
        # Testing directly in the string works if the output is only
        # one line.
        # if 'No such image' in p.stdout:
        # raise DockerImageError
        # data = [json.loads(str(item)) for item in p.stdout.readline().strip().split('\n')]
        json_block = []
        line = p.stdout.readline()
        while (line):
            if 'no such image' in line:
                raise DockerImageError
            # Stupid sarge appears to add a blank line between
            # json statements. This checks for a blank line and
            # cycles to the next line if it is blank.
            if re.match(r'^\s*$', line):
                line = p.stdout.readline()
                continue
            json_block.append(line)
            line = p.stdout.readline()
        s = ''.join(json_block)
        s = s[1:-2]
        self.metadata = s


    def set_image(self, image):
        """set_image
            sets docker image id to docker object.
            :param image: image id
            """
        self.imageID = image


    def set_command(self, command):
        """set_command
            sets the docker command to docker object
            :param command: docker command
            """
        if len(command) > 0:
            self.command = command
        else:
            raise DockerInputError("Invalid Command")

    # Function to compare sematic versioning
    # See http://zxq9.com/archives/797 for explaination
    # and http://semver.org/ for information on semantic versioning
    def ver_tuple(self, z):
        return tuple([int(x) for x in z.split('.') if x.isdigit()])

    def ver_cmp(self, a, b):
        return cmp(self.ver_tuple(a), self.ver_tuple(b))

