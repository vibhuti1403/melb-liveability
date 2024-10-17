#!/usr/bin/env bash

. ./unimelb-COMP90024-2022-grp-27-openrc.sh; ansible-playbook deploy_application.yaml --ask-become-pass -i inventory/application_hosts.ini