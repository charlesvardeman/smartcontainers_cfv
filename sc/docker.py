from util import which
from sarge import Command, Capture, get_stdout, get_stderr, capture_stdout
from io import TextIOWrapper
import re
import json
import subprocess

# We need to docker version greater than 1.6.0 to support
# the label functionality.
min_docker_version = '1.6.0'

# Default docker commands that sc can handle.
snarf_docker_commands = ['run', 'build']
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


class Docker:
    def __init__(self, command):
        self.command = command
        self.label_prefix = "smartcontainer"
        self.location = self.find_docker()
        self.imageID = None
        self.container = None
        self.metadata = {}
        self.smartcontainer = {}

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
        p = Command(cmd_string)
        p.run(async=True)

        for name in snarf_docker_commands:
            if name in self.command:
                self.capture_cmd_workflow()

    def capture_command(self):
        pass

    def capture_cmd_workflow(self):
        pass

    def put_label_image(self, label, imageID):
        """put_label attaches json metadata to smartcontainer label"""

        # Due to the structure of docker, we have to do this in a series of
        # steps. This method attaches a label to a image by creating a
        # temporary container with a label using docker run. We then save that
        # container to a new image with the same.

        # Only proceed if the input string is valid Json
        if self.validate_json(label):

            # First get tag and name for image id passed to method
            repository, tag = self.get_image_info(imageID)

            # Now "attach" the label by running a new container from the imageID
            label_cmd_string = str(self.location) + " run --name=labeltmp --label=" + \
                               self.label_prefix + "='" + label + "' " + imageID + " /bin/echo"
            #print label_cmd_string
            subprocess.call(label_cmd_string, shell=True)

            # Save container with new label to new image with previous repo and tag
            self.container_save_as('labeltmp', repository, tag)

            # Stop the running container so it can be removed
            self.stop_container('labeltmp')

            # remove temporary container
            self.remove_image('labeltmp')
        else:
            print "Invalid Input: not a valid Json string"

    def container_save_as(self, name, saveas, tag):
        """ Saves a container to a new image
        :param name: the name of the container to be saved
        :param saveas: the name of the image to be created
        :param tag: the tag attached to the new image
        :return: none
        """
        commit_cmd_string = str(self.location) + ' commit ' + name + ' ' + saveas + ':' + tag
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


    def get_label(self, image):
        """get_label returns smartconainer json string from docker image or container"""
        self.get_metadata(image)

        if bool(self.metadata):
            AllDictionary = json.loads(self.metadata)
            ConfigDictionary = AllDictionary["Config"]
            label = ConfigDictionary["Labels"]
        return label


# Quick hack to get image id for current phusion/baseimage
# for testing purposes. We assume that the image has already
# been pulled from the docker hub repo.
    def get_imageID(self, container):
        # default_container = "phusion/baseimage"
        imageID = None
        docker_command = str(self.location) + ' images'
        output = capture_stdout(docker_command)
        for line in TextIOWrapper(output.stdout):
            if container in repr(line):
                imageID = line.split()[2]
        if imageID is None:
            raise DockerImageError
        return imageID


    def get_image_info(self, imageID):
        docker_command = str(self.location) + ' images'
        output = capture_stdout(docker_command)
        for line in TextIOWrapper(output.stdout):
            if imageID in repr(line):
                repository = line.split()[0]
                tag = line.split()[1]
        if imageID is None:
            raise DockerImageError
        return repository, tag


# Each image has a metadata record. This returns a list of all label
# strings contained in the metadata.
    def get_metadata(self, image):
        docker_command = str(self.location) + ' inspect ' + image
        print docker_command
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
            #if not line: break
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
        self.command = command

    # Function to compare sematic versioning
    # See http://zxq9.com/archives/797 for explaination
    # and http://semver.org/ for information on semantic versioning
    def ver_tuple(self, z):
        return tuple([int(x) for x in z.split('.') if x.isdigit()])

    def ver_cmp(self, a, b):
        return cmp(self.ver_tuple(a), self.ver_tuple(b))

