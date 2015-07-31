import pytest
import os

# Test code that discovers docker command
def test_find_docker():
    from sc import docker
    oldpath = os.environ["PATH"]
    with pytest.raises(docker.DockerNotFoundError):
        dockertester = docker.Docker('help')
        # check that exceptions are being raised.
        os.environ["PATH"] = "NULL"
        location = dockertester.find_docker()
    os.environ["PATH"] = oldpath
    location = dockertester.find_docker()
    assert location is not None

def test_docker_version():
    from sc import docker
    with pytest.raises(docker.DockerInsuficientVersionError):
        # This will fail if docker ever gets to version 100
        dockertester = docker.Docker("--help")
        dockertester.check_docker_version("100.100.100")

def test_check_docker_connection():
    from sc import docker
    dockertester = docker.Docker("--help")
    docker_host = os.environ["DOCKER_HOST"]
    with pytest.raises(docker.DockerServerError):
        os.environ["DOCKER_HOST"] = "tcp://0.0.0.0"
        dockertester.check_docker_connection()
    os.environ["DOCKER_HOST"] = docker_host
    dockertester.check_docker_connection()

# Test all sanity checks to make sure docker is there.
def test_sanity():
    from sc import docker
    dockertester = docker.Docker('help')
    dockertester.sanity_check()

# This test should pass through since we don't capture the
# provenance of help.
def test_do_command_simple():
    from sc import docker
    dockertester = docker.Docker('--help')
    dockertester.do_command()

def test_do_command_run():
    from sc import docker
    dockertester = docker.Docker('run /usr/bin/uname')
    dockertester.do_command()
