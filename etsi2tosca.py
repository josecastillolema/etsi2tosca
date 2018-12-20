#!/usr/bin/python

# Author: Jose Castillo Lema <josecastillolema@gmail.com>

"Main module of tosca2etsi"

import sys
#import netaddr
import yaml
#import subprocess
#from collections import defaultdict
#from jinja2 import Template

def parse_tosca(path):
    "Parses the yaml file corresponding to the TOSCA vnfd ou vnnffgg template."
    try:
        yaml_file = open(path, 'r')
    except IOError:
        print 'File does not exist'
        sys.exit()
    content = yaml_file.read()
    parsed_file = yaml.load(content)
    return parsed_file

def analize_tosca(parsed_tosca):
    "Parses the yaml file corresponding to the TOSCA vnfd ou vnnffgg template."
    print parsed_tosca

if __name__ == '__main__':
    usage = """Usage: tosca2etsi FILE

Converts TOSCA NFV templates into ETSI profile

Options:
  -h, --help            show this help message and exit"""
    if len(sys.argv) > 2:
        sys.exit(usage)
    elif len(sys.argv) == 2:
        if (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
            sys.exit(usage)
        else:
            parsed_tosca = parse_tosca(sys.argv[1])
            analize_tosca(parsed_tosca)
    else:
        sys.exit(usage)