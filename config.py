import logging
from dotenv import load_dotenv
import toml
import os

_config = {}


def get_config():
    if not _config:
        raise Exception("Config not initialized")
    return _config


def resolve_path(path: str) -> str:
    if os.path.isabs(path):
        return path

    current_dir = os.getcwd()
    candidate = os.path.join(current_dir, path)
    if os.path.exists(candidate):
        return candidate
    return path


def init_config(env_file: str, config_file: str):
    global _config
    env_file = resolve_path(env_file)
    config_file = resolve_path(config_file)

    logging.info(f"loading env file: {env_file}")
    load_dotenv(env_file, override=True)
    logging.info("loading env file successfully!")

    logging.info(f"loading config file: {config_file}")
    _config = toml.load(config_file)
    logging.info("loading config file successfully!")

    return _config
