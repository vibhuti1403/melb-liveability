import argparse
import sys


def create_instances_file(n_instances):
    with open("host_vars/instances.yaml", 'w') as file:
        file.write("# ****************************** Security group ******************************\n")
        file.write("security_groups:\n")
        for i in range(1, n_instances+1):
            file.write("  - name: instance{}-security-group\n".format(i))
            file.write("    description: \"security group for instance {}\"\n".format(i))
        file.write("\n")
        file.write("security_group_rules:\n")
        for port in [22,80,1313,5984,4369,9100]:
            for i in range(1, n_instances+1):
                file.write("  - name: instance{}-security-group\n".format(i))
                file.write("    protocol: tcp\n")
                file.write("    port_range_min: "+str(port)+"\n")
                file.write("    port_range_max: "+str(port)+"\n")
                file.write("    remote_ip_prefix: 0.0.0.0/0\n")
        for masterport in [5000,3000]:
            file.write("  - name: instance1-security-group\n")
            file.write("    protocol: tcp\n")
            file.write("    port_range_min: "+str(masterport)+"\n")
            file.write("    port_range_max: "+str(masterport)+"\n")
            file.write("    remote_ip_prefix: 0.0.0.0/0\n")
        file.write("\n")
        file.write("# ****************************** Volume ******************************\n")
        file.write("volumes:\n")
        for i in range(1, n_instances+1):
            file.write("  - vol_name: instance{}-volume\n".format(i))
            file.write("    vol_size: 60\n")
            file.write("    device: /dev/vdb\n")
            file.write("    mountpoint: /data\n")
        file.write("\n")

        file.write("# ****************************** Instance ******************************\n")
        file.write("instances:\n")
        for i in range(1, n_instances + 1):
            file.write("  - name: instance{}\n".format(i))
            file.write("    security_groups: instance{}-security-group\n".format(i))
            file.write("    volume_ids: '{{ instance{}_volumes|default([]) }}'\n".format(i))
            file.write("    volumes: ['instance{}-volume']\n".format(i))
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='n instances to be created')
    args = parser.parse_args()
    create_instances_file(int(args.n))