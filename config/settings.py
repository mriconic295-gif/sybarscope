import json, os

CONFIG_FILE = os.path.join("config", "settings.json")

def load_config():
    default = {
        "theme": "Dark",
        "timeout": 10,
        "max_threads": 5,
        "cache_enabled": True,
        "log_level": "INFO"
    }
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return { **default,** config}
    except FileNotFoundError:
        return default

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
