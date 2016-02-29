import pytest
import os

# Test code that discovers docker command
def test_find_docker():
    from sc import dockercli
    oldpath = os.environ["PATH"]
    with pytest.raises(dockercli.DockerNotFoundError):
        dockertester = dockercli.DockerCli('help')
        # check that exceptions are being raised.
        os.environ["PATH"] = "NULL"
        location = dockertester.find_docker()
    os.environ["PATH"] = oldpath
    location = dockertester.find_docker()
    assert location is not None

def test_docker_version():
    from sc import dockercli
    with pytest.raises(dockercli.DockerInsuficientVersionError):
        # This will fail if docker ever gets to version 100
        dockertester = dockercli.DockerCli("--help")
        dockertester.check_docker_version("100.100.100")

def test_check_docker_connection():
    from sc import dockercli
    dockertester = dockercli.DockerCli("--help")
    docker_host = os.environ["DOCKER_HOST"]
    with pytest.raises(dockercli.DockerServerError):
        os.environ["DOCKER_HOST"] = "tcp://127.0.0.1:1000"
        dockertester.check_docker_connection()
    os.environ["DOCKER_HOST"] = docker_host
    dockertester.check_docker_connection()

# Test all sanity checks to make sure docker is there.
def test_sanity():
    from sc import dockercli
    dockertester = dockercli.DockerCli('help')
    dockertester.sanity_check()

# This test should pass through since we don't capture the
# provenance of help.
def test_do_command_simple():
    from sc import dockercli
    dockertester = dockercli.DockerCli('--help')
    dockertester.do_command()

def test_do_command_run():
    from sc import dockercli
    dockertester = dockercli.DockerCli('run /usr/bin/uname')
    dockertester.do_command()

# Tests function that returns the current image id for
# "phusion/baseimage"
def test_get_imageID():
    from sc import dockercli
    dockertester = dockercli.DockerCli('images')
    imageID = dockertester.get_imageID("phusion/baseimage")
    # assert imageID == "e9f50c1887ea"

def test_put_label_image():
    from sc import dockercli
    dockertester = dockercli.DockerCli('images')
    imageID = dockertester.get_imageID("phusion/baseimage")
    dockertester.set_image(imageID)
    label = '{"Description":"A containerized foobar","Usage":"docker run --rm example/foobar [args]","License":"GPL","Version":"0.0.1-beta","aBoolean":true,"aNumber":0.01234,"aNestedArray":["a","b","c"]}'
    dockertester.put_label_image(label)

def test_docker_get_metadata():
    from sc import dockercli
    dockertester = dockercli.DockerCli('images')
    imageID = dockertester.get_imageID("phusion/baseimage")
    dockertester.set_image(imageID)
    label = dockertester.get_metadata()

def test_docker_get_label():
    from sc import dockercli
    dockertester = dockercli.DockerCli('images')
    imageID = dockertester.get_imageID("phusion/baseimage")
    dockertester.set_image(imageID)
    label = dockertester.get_label()
