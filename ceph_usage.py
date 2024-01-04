#! /bin/python

"""
Calculate provisioned space
"""

import subprocess
import json
import sys

# get pool names
command = "ceph df --format json"
jsonout = json.loads(subprocess.check_output(command.split()))

# Get pools out of that
pools = [pool['name'] for pool in jsonout["pools"] if "." not in pool['name']]

print(pools)

#
total_provisioned_size = 0.0
total_used_size = 0.0

for pool in pools:
    command = "rbd du --format json -p " + pool
    print("NOW RUNNING:" + command)
    jsonout = json.loads(subprocess.check_output(command.split()))
    total_provisioned_size += jsonout["total_provisioned_size"]
    total_used_size += jsonout["total_used_size"]
    print("total_used_size for this pool:" + str(total_used_size))
    print("total_provisioned_size for this pool:" + str(total_provisioned_size))

print("total_provisioned_size: " + total_provisioned_size)
print("total_used_size: " + total_used_size)

