import platform
import subprocess
import sys

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

ping(sys.argv[1])