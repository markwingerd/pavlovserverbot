import os, subprocess

def get_env(env_name):
    # TODO: Add user friendly error?
    return os.environ[env_name]

def get_process():
    # Returns the process ids as a string
    process = subprocess.Popen('pgrep PavlovServer', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid, err = process.communicate()
    return pid

def run_script(script_name):
    subprocess.call('scripts/{}'.format(script_name), shell=True)
