import os

def get_env(env_name):
    # TODO: Add user friendly error?
    return os.environ[env_name]
