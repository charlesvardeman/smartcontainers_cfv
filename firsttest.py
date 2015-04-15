import provmodified as prov
import docker


docker.bind_ns("test", "http://tw.rpi.edu/ns/test#")

image = docker.Image("test:image")
image.set_label("example image")

#activity = prov.Activity("test:activity")
#activity.set_label("example activity")

print(docker.serialize(format="turtle"))
