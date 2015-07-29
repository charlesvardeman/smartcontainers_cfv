from util import which
from sarge import get_stdout

min_docker_version = '1.6.0'

class Error(Exception):
    """Base class for docker module exceptions"""
    pass

class DockerNotFoundError(RuntimeError):
    """Exception raised for missing docker command.

    Attributes:
        msg -- explaination of error
    """

    def __init__(self):
        msg = "Please make sure docker is installed and in your path."
        self.arg = msg

class Docker:
    def __init__(self, command):
        self.command = command
        self.location = None

    def sanity_check(self):
        """sanity_check checks existence and executability of docker."""
        if self.location is None:
            location = self.find_docker()
            if location is None:
                raise DockerNotFoundError
        self.check_docker_version()

    def find_docker(self):
        """find_docker searches paths and common directores to find docker."""
        self.location = which("docker")
        return self.location

    def check_docker_version(self):
        output = get_stdout('docker --version')
        # in docker 1.7.1 version is at 2 position in returned string
        version = output.split()[2]
        # remove comma from out put if in string
        if ',' in version:
            version = version[:-1]
        assert self.ver_cmp(version, min_docker_version) > 0

    def do_command(self):
        pass

    def capture_command(self):
        line = self.command
        return line

    def capture_cmd_workflow(self):
        pass

    # Function to compare sematic versioning
    # See http://zxq9.com/archives/797 for explaination
    # and http://semver.org/ for information on semantic versioning
    def ver_tuple(self, z):
        return tuple([int(x) for x in z.split('.') if x.isdigit()])

    def ver_cmp(self, a, b):
        return cmp(self.ver_tuple(a), self.ver_tuple(b))
