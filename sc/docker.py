from util import which
from sarge import Command, get_stdout, get_stderr

# We need to docker version greater than 1.6.0 to support
# the label functionality.
min_docker_version = '1.6.0'


snarf_docker_commands = ['run', 'build']


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


class Docker:
    def __init__(self, command):
        self.command = command
        self.location = None
        self.imageID = None

    def sanity_check(self):
        """sanity_check checks existence and executability of docker."""
        if self.location is None:
            self.find_docker()
        self.check_docker_version()
        self.check_docker_connection()

    def find_docker(self):
        """find_docker searches paths and common directores to find docker."""
        self.location = which("docker")
        if self.location is None:
            raise DockerNotFoundError("Please make sure docker is installed "
                "and in your path")
        return self.location

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
        line = self.command
        return line

    def capture_cmd_workflow(self):
        print "Capture command workflow"
        pass

    def put_label(self, label):
        pass

    def get_label(self):
        pass

    # Function to compare sematic versioning
    # See http://zxq9.com/archives/797 for explaination
    # and http://semver.org/ for information on semantic versioning
    def ver_tuple(self, z):
        return tuple([int(x) for x in z.split('.') if x.isdigit()])

    def ver_cmp(self, a, b):
        return cmp(self.ver_tuple(a), self.ver_tuple(b))
