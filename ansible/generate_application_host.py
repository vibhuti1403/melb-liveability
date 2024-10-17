import argparse
def create_instances(hosts):
    with open("inventory/application_hosts.ini", "w") as file:
        file.write("[instances]\n")
        for host in hosts:
            file.write(host+'\n')
        file.write("\n")

def create_db(hosts):
    with open("inventory/application_hosts.ini", "a") as file:
        file.write("[database:children]\n")
        file.write("masternode\n")
        file.write("workers\n")
        file.write("\n")
        file.write("[masternode]\n")
        file.write("{}\n".format(hosts[0]))
        file.write("\n")
        file.write("[workers]\n")
        for host in hosts[1:]:
            file.write("{}\n".format(host))
        file.write("\n")


if __name__ == "__main__":
    with open("inventory/wm_inventory_file.ini") as f:
        hosts_starts = False
        hosts = []

        for line in f.readlines():
            line = line.replace("\n", "")

            # no hosts any more
            if hosts_starts:
                if line == "":
                    hosts_starts = False

            # has hosts e.g.: 192.168.0.1
            if hosts_starts:
                hosts.append(line)

            # starts reading hosts
            if line == "[instances]":
                hosts_starts = True
    create_instances(hosts)
    create_db(hosts)

