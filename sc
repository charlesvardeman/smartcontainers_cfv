#!/usr/bin/env python
"""Smart Container wrapper for docker

Usage: sc

Options:
    -h, --help     show help file
    -g, --genMeta  print raw json-ld metadata from docker container

Example:
    sc --genMeta <image>
    sc --genMeta <container label>
"""

import provmodified as prov
import docker
import json
from optparse import OptionParser
import subprocess
import sys
import os
from rdflib import plugin, BNode


def usage():
    print __doc__


def main(argv):
    parser = OptionParser()
    parser.add_option('-g', '--genMeta', dest='image', help='Docker image name')
    try:
        (options, args) = parser.parse_args()
    except SystemExit:
        return

    if options.image:
        docker.bind_ns("test", "http://daspos.crc.nd.edu/test#")
        dic = docker.inspect_json("docker inspect " + options.image)
        # graph = initialGraph(obj,dic)
        g = docker.serialize(format="turtle")
        g2 = docker.returnGraph()

        print type(g2)

        qres = g2.query(
                """SELECT DISTINCT ?a ?b
                WHERE {
                    ?a prov:hadDerivation ?b .
                }""")

        for row in qres:
            print("%s wasDerivedFrom %s" % row)

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
     

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        sys.exit()
    main(sys.argv[1:])
