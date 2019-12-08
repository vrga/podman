podman
=========

A simple podman role to allow installation of it on Ubuntu systems from version 16.04 upwards.

Requirements
------------
ansible >= 2.8

Role Variables
--------------

This role will set up the following variables into files by default.
My personal use assumption is to use docker containers off of docker.io,
So the default configuration accepts containers from them.
```
containers_policy: # /etc/containers/policy.json
  default:
    - type: reject
  transports:
    docker:
      docker.io:
        - type: insecureAcceptAnything
```

Same with search registries
```
registries: # /etc/containers/registries.conf
  search:
    - docker.io
  insecure: []
  block: []
```

The default network will allow routing container traffic to the public internet.
Assumption is that the users know how to configure CNI networking.
```
cni_networking:
  - filename: 87-podman-bridge # /etc/cni/net.d/87-podman-bridge.conflist
    cniVersion: 0.4.0
    name: podman
    plugins:
      - type: bridge
        bridge: cni-podman0
        isGateway: true
        ipMasq: true
        ipam:
          type: host-local
          routes:
            - dst: 0.0.0.0/0
          ranges:
            - - subnet: 10.88.0.0/16
                gateway: 10.88.0.1
      - type: portmap
        capabilities:
          portMappings: true
      - type: firewall
        backend: iptables
```

Example Playbook
----------------

```,]
- hosts: localhost
  roles:
    - ../roles/podman
```

License
-------
BSD-3-Clause

Author Information
------------------

[Fran Pavelić](https://github.com/vrga/)
