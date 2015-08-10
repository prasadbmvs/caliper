## wuyanjun 00291783
## wu.wu@hisilicon.com
## Copyright

#!/usr/bin/python

import os
import sys
import logging
import pdb
import re
import shutil
import subprocess

import test_perf_tranver as traverse
import caliper.server.utils as server_utils
from caliper.client.shared import caliper_path

CALIPER_DIR = caliper_path.CALIPER_DIR
OUT_DIR = caliper_path.RESULTS_DIR 
LOCATION = os.path.dirname(sys.modules[__name__].__file__)

def get_targets_data(outdir):
    yaml_dir = os.path.join(outdir, 'yaml')
    yaml_files = []
    json_files = []
    for root, dirs, files in os.walk(yaml_dir):
        for i in range(0, len(files)):
            if re.search('_score_post\.yaml', files[i]):
                yaml_name = os.path.join(root, files[i])
                yaml_files.append(yaml_name)
            else:
                if re.search('.json', files[i]):
                    json_name = os.path.join(root, files[i])
                    json_files.append(json_name)
    return (yaml_files, json_files)

def traverse_caliper_output(hosts):

    YAML_DIR = os.path.join(OUT_DIR, 'yaml')
    host_name = server_utils.get_host_name(hosts)
    host_yaml_name = host_name + '_score.yaml'
    host_yaml_file = os.path.join(YAML_DIR, host_yaml_name)
    try:
        return_code = traverse.traverser_perf(hosts, host_yaml_file)
    except Exception, e:
        logging.info(e)
        raise
    else:
        if return_code != 1:
            logging.info("there is wrong when dealing the yaml file")

def parser_caliper(host):
    try:
        traverse_caliper_output(host)
    except Exception, e:
        logging.info(e.args[0], e.args[1])
        return

    file_lists = []
    (file_lists, json_files) = get_targets_data(OUT_DIR)

    if caliper_path.judge_caliper_installed():
        if not os.path.exists(caliper_path.FRONT_END_DIR):
            shutil.copytree(caliper_path.FRONT_TMP_DIR, caliper_path.FRONT_END_DIR)

    if not os.path.exists(caliper_path.HTML_DATA_DIR):
        os.makedirs(caliper_path.HTML_DATA_DIR)

    if file_lists:
        for yaml_file in file_lists:
            shutil.copy(yaml_file, caliper_path.HTML_DATA_DIR)

    if json_files:
        for json_file in json_files:
            shutil.copy(json_file, caliper_path.HTML_DATA_DIR)
