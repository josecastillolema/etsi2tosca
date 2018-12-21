#!/usr/bin/python

# Author: Jose Castillo Lema <josecastillolema@gmail.com>

"Main module of etsi2tosca"

import sys
#import netaddr
import yaml
#import subprocess
#from collections import defaultdict
#from jinja2 import Template

etsi = {}

def parse_tosca(path):
    "Parses the yaml file corresponding to the ETSI vnfd template."
    try:
        yaml_file = open(path, 'r')
    except IOError:
        print 'File does not exist'
        sys.exit()
    content = yaml_file.read()
    parsed_file = yaml.load(content)
    return parsed_file

def analize_tosca(parsed_tosca, debug):
    "Analizes the ETSI template."
    parsed_tosca = parsed_tosca['vnfd:vnfd-catalog']['vnfd:vnfd'][0]
    name = parsed_tosca['name']
    etsi['name'] = name
    if debug:
        print 'name', name
    description = parsed_tosca['description']
    etsi['description'] = description
    if debug:
        print 'description', description
    vendor = parsed_tosca['vendor']
    etsi['vendor'] = vendor
    if debug:
        print 'vendor', vendor
    vdu = parsed_tosca['vdu'][0]
    image = vdu['image']
    etsi['image'] = image
    if debug:
        print 'image', image
    cloudinit = vdu['cloud-init-file']
    if debug:
        print 'cloudinit', cloudinit
    etsi['cloudinit'] = cloudinit
    if vdu['vm-flavor']:
        flavor = vdu['vm-flavor']
        mem = flavor['memory-mb']
        etsi['mem'] = mem
        if debug:
            print 'mem', mem
        vcpu = flavor['vcpu-count']
        etsi['vcpu'] = vcpu
        if debug:
            print 'vcpu', vcpu
        disk = flavor['storage-gb']
        etsi['disk'] = disk
        if debug:
            print 'disk', disk
    if vdu['external-interface']:
        ints = vdu['external-interface']
        etsi['ints'] = []
        for i in ints:
            if debug:
                print i['name']
            etsi['ints'].append(i['name'])
            if debug:
                print i['vnfd-connection-point-ref']
            etsi['ints'].append(i['vnfd-connection-point-ref'])
    if parsed_tosca['connection-point']:
        cps = parsed_tosca['connection-point']
        etsi['cps']=[]
        for i in cps:
            if debug:
                print i['name']
            etsi['cps'].append(i['name'])
    config = parsed_tosca['vnf-configuration']['service-primitive'][0]['parameter']
    etsi['config'] = []
    for i in config:
        if debug:
            print i['name']
        if debug:
            print i['data-type']
        if i.has_key('default-value'):
            if debug:
                print i['default-value']
            #etsi['config'].append(i['default-value'])
            etsi['config'].append((i['name'],i['data-type'],i['default-value']))
        else:
            etsi['config'].append((i['name'],i['data-type']))

    config2 = parsed_tosca['vnf-configuration']['service-primitive'][1]['parameter']
    etsi['config2'] = []
    for i in config2:
        if debug:
            print i['name']
        if debug:
            print i['data-type']
        etsi['config2'].append((i['name'],i['data-type']))

def create_etsi():
    #print etsi
    #print
    print 'tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0'
    print
    print 'description:', etsi['description']
    print
    print 'metadata:'
    print '  template_name:', etsi['name']
    print
    print 'topology_template:'
    print '  inputs:'
    for i in etsi['config']:
        print '   %s:' % i[0]
        print '     type:', i[1].lower()
        if len(i)==3:
            print '      default:', i[2]
        print
    for i in etsi['config2']:
        print '   %s:' % i[0]
        print '     type:', i[1].lower()
        if len(i)==3:
            print '      default:', i[2]
        print
    print '  node_templates:'
    print '    VDU1:'
    print '      type: tosca.nodes.nfv.VDU.Tacker'
    print '      capabilities:'
    print '        nfv_compute:'
    print '          properties:'
    print '            num_cpus:', etsi['vcpu']
    print '            mem_size:', etsi['mem'], 'MB'
    print '            disk_size:', etsi['disk'], 'GB'
    print '      properties:'
    print '        image:', etsi['image']
    print '        mgmt_driver: noop'
    print '        user_data:'
    print '          str_replace:'
    print '            template: {get_file: %s}' % etsi['cloudinit']
    print
    for i in range(0,len(etsi['cps'])):
       print '    CP%s' % i
       print '      type: tosca.nodes.nfv.CP.Tacker'
       print '      properties:'
       print '        management: false'
       print '        order:', i
       print '        anti_spoofing_protection: false'
       print '      requirements:'
       print '        - virtualLink:'
       print '            node: VL%s' % i
       print '        - virtualBinding:'
       print '            node: VDU1'
    print
    for i in range(0,len(etsi['cps'])):
        print '    VL%s' % i
        print '      type: tosca.nodes.nfv.VL'
        print '      properties:'
        print '        network_name:', etsi['ints'][i*2]
        print '        vendor:', etsi['vendor']
        print

if __name__ == '__main__':
    usage = """Usage: etsi2tosca FILE

Converts ETSI NFV templates into TOSCA profile

Options:
  -h, --help            show this help message and exit"""
    if len(sys.argv) > 2:
        sys.exit(usage)
    elif len(sys.argv) == 2:
        if (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
            sys.exit(usage)
        else:
            parsed_tosca = parse_tosca(sys.argv[1])
            #print parsed_tosca
            #print
            analize_tosca(parsed_tosca, debug=False)
            #print
            create_etsi()
    else:
        sys.exit(usage)