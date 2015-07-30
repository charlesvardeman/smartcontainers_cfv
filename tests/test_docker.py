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
        print "PATH orig is: %s" % os.environ["PATH"]
        location = dockertester.find_docker()
    os.environ["PATH"] = oldpath
    print "PATH should be orig is: %s" % os.environ["PATH"]
    location = dockertester.find_docker()
    assert location is not None

def test_docker_version():
    from sc import docker
    with pytest.raises(docker.DockerInsuficientVersionError):
        # This will fail if docker ever gets to version 100
        dockertester = docker.Docker("--help")
        dockertester.check_docker_version("100.100.100")

# Test all sanity checks to make sure docker is there.
def test_sanity():
    from sc import docker
    dockertester = docker.Docker('help')
    dockertester.sanity_check()
