#! /bin/python

import json
import subprocess
from pprint import pprint
def pool_root_mapping():
    """
    Figure out the root to pool map.

    Returns a dict of the form {"root_name1": ["pool1", "pool2"],
                                "root_name2": ["pool3", "pool4"]}
    """
    # This is rule_id and root_name mapping.
    command = "ceph osd crush dump --format json"
    jsonout = json.loads(subprocess.check_output(command.split()))
    rules = {}

    for rule in jsonout["rules"]:

        crush_rule_id = rule["rule_id"]
        item_name_found = False

        for step in rule["steps"]:
            if "item_name" in step:
                item_name = step["item_name"]
                item_name_found = True
                break

        if not item_name_found:
            raise Exception("item_name not found.")

        rules[crush_rule_id] = item_name

    # This gives pool name to crush_rule_id mapping.
    command = "ceph osd pool ls detail --format json"
    jsonout = json.loads(subprocess.check_output(command.split()))
    pool_root_map = {}
    for item in jsonout:
        root_name = rules[item["crush_rule"]]
        pool_name = item["pool_name"]

        if root_name in pool_root_map:
            pool_root_map[root_name].append(pool_name)
        else:
            pool_root_map[root_name] = [pool_name]

    return pool_root_map

pprint(pool_root_mapping())
