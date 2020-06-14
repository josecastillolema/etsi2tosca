# etsi2tosca
Converts ETSI NFV templates into TOSCA profile.

Use
--------------
```
Usage: etsi2tosca FILE

Converts ETSI NFV templates into TOSCA profile

Options:
  -h, --help            show this help message and exit
```

Examples
--------------

Example 1:
```yaml
$ ./etsi2tosca.py samples/opencv_transcoder_vnfd.yaml 
tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0

description: OpenCV Transcoder VNF

metadata:
  template_name: opencv_transcoder_vnf

topology_template:
  inputs:
   ssh-hostname:
     type: string
      default: <rw_mgmt_ip>

   ssh-username:
     type: string
      default: ubuntu

   ssh-password:
     type: string
      default: 5ginfire

   ssh-private-key:
     type: string

   stream-ip:
     type: string

   output-port:
     type: integer

  node_templates:
    VDU1:
      type: tosca.nodes.nfv.VDU.Tacker
      capabilities:
        nfv_compute:
          properties:
            num_cpus: 8
            mem_size: 8192 MB
            disk_size: 20 GB
      properties:
        image: opencv_transcoder_image
        mgmt_driver: noop
        user_data:
          str_replace:
            template: {get_file: transcoder_cloud_init.cfg}

    CP0
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        management: false
        order: 0
        anti_spoofing_protection: false
      requirements:
        - virtualLink:
            node: VL0
        - virtualBinding:
            node: VDU1
    CP1
      type: tosca.nodes.nfv.CP.Tacker
      properties:
        management: false
        order: 1
        anti_spoofing_protection: false
      requirements:
        - virtualLink:
            node: VL1
        - virtualBinding:
            node: VDU1

    VL0
      type: tosca.nodes.nfv.VL
      properties:
        network_name: eth0
        vendor: 5GinFIRE

    VL1
      type: tosca.nodes.nfv.VL
      properties:
        network_name: eth1
        vendor: 5GinFIRE
```

Example 2:
```
$ ./etsi2tosca.py samples/opencv_transcoder_vnfd.yaml > opencv_transcoder_vndf_tosca.yaml
```
