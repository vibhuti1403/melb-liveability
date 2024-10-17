import argparse
import sys
import json

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def createConfig(n_instances):
    categories=json.load(open("host_vars/application.json"))['categories'].split(',')
    categories=list(split(categories,n_instances))
    for i in range(0, n_instances):
        with open('config/application.env', 'r') as file :
            filedata = file.read()
            filedata = filedata.replace('<categories>', ','.join(categories[i]))
        with open('../Harvester_T/configs/instance'+str(i+1)+'.env','w') as file_write:
            file_write.write(filedata)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='n instances')
    args = parser.parse_args()
    createConfig(int(args.n))