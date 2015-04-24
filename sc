#!/usr/bin/python
import provmodified as prov
import docker
import json
import subprocess, sys, os



def main():
    #no user input error handling here. I assume user always input right args.
    cmd = sys.argv
    
    if cmd[1] == "genMeta":
        obj = cmd[2]
        docker.bind_ns("test", "http://tw.rpi.edu/ns/test#")
        image = docker.Image("docker inspect "+obj,"test:image")
        image.set_label("example image")
        print(docker.serialize(format="turtle"))
        
    else:
        print "errors"
        

if __name__ == "__main__":
    main()
