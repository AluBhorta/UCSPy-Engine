import json

def parse_config_file(fpath="ucsp.config.json"):
    with open(fpath) as f:
        return json.load(f)
