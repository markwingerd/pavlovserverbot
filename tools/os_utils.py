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

def get_file(path):
    with open(path, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
    return lines

def save_file(path, lines):
    with open(path, 'w') as f:
        for line in lines:
            if line.endswith('\n'):
                f.write(line)
            else:
                f.write('{}\n'.format(line))
