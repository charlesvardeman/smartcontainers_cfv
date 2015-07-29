from util import which

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

    def find_docker(self):
        """find_docker searches paths and common directores to find docker."""
        self.location = which("docker")
        return self.location

    def do_command(self):
        pass

    def capture_command(self):
        line = self.command
        return line

    def capture_cmd_workflow(self):
        pass
