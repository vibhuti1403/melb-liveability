#!/usr/bin/env bash

. ./unimelb-COMP90024-2022-grp-27-openrc.sh; ansible-playbook config_instances.yaml --ask-become-pass -i inventory/application_hosts.ini