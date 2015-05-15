#!/usr/bin/env python
"""Smart Container wrapper for docker

Usage: sc

Options:
    -h, --help     show help file
    -g, --genMeta  print raw json-ld metadata from docker container
    -r, --run      run docker image with cmd and generate a new container

Example:
    sc --genMeta <image>
    sc --genMeta <container label>
"""

import provmodified as prov
import collections
import docker
import json
from optparse import OptionParser
import subprocess
import sys
import os
from rdflib import plugin, BNode, Graph


def usage():
    print __doc__


def main(argv):
    parser = OptionParser()
    parser.add_option('-g', '--genMeta', dest='image', help='Docker image name')
    parser.add_option('-c', '--create', dest='cmd', help='Docker run image cmd')
    try:
        (options, args) = parser.parse_args()
    except SystemExit:
        return

    if options.image:
        docker.bind_ns("test", "http://daspos.crc.nd.edu/test#")
        dic = docker.inspect_json("docker inspect " + options.image)
        graph = initialGraph(options.image,dic)
        
        g = docker.serialize(format='n3')
        context = {"docker": "http://www.example.org/ns/docker#", "prov": "http://www.w3.org/ns/prov#"}
        g2 = Graph().parse(data=g, format='n3')
        g3 = g2.serialize(format='json-ld', indent=4)
        
        
        


        g3 = g3.replace('\n','')
        g3 = g3.replace(' ','')
        g3 = convert(g3)
        print g3
        print
        print
        print
        g4= Graph().parse(data=g3, format='json-ld',context=context)
        #print g4.serialize(format='turtle')
        
        con_id = docker.create_container("docker create  --label=data='"+g3+"' "+options.image+" "+options.cmd)
        docker.run("docker start "+con_id)
        container = docker.inspect_json("docker inspect " + con_id)
        
        container = convert(container)
        #container = container.replace('\n','')
        #container = container.replace(' ','')
        print
        print
        previousdata = container['Config']['Labels']['data']
        print previousdata
        
        newgraph= Graph().parse(data=previousdata, format='json-ld',context=context)
       
        
        print newgraph.serialize(format='turtle')
        #print len(g2)
        #for each in g2:
        #        print each

        #qres = g2.query(
        #        """SELECT DISTINCT ?a ?b
        #        WHERE {
        #            ?a prov:hadDerivation ?b .
        #        }""")

        #for row in qres:
        #    print("%s wasDerivedFrom %s" % row)
        #

def initialGraph(obj, dic):

        parent = BNode()

        id = docker.get_id(dic)

        type = docker.get_type(dic)

        if type == "Image":
                container = docker.get_container(dic)
                parentImage = docker.get_parentImage(dic)
                if parentImage != "":
                        dataset = docker.inspect_json("docker inspect " + parentImage)
                        parent = initialGraph(parentImage, dataset)

        elif type == "Container":
                image = docker.get_image(dic)

        else:
                return
        # docker.bind_ns("test", "http://tw.rpi.edu/ns/test#")
        image = docker.Image("docker inspect " + obj, "test:" + id)
        image.set_label("example image")
        image.set_was_derived_from(parent)
        return image
        
def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data
     

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    main(sys.argv[1:])
