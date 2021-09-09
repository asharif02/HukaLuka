#! /usr/bin/env python3

import subprocess

# EXAMPLE 1: running a command
#subprocess.run('ls') 
#subprocess.run('ls -la', shell=True)
'''
shell=True should be used as an arguement to avoid errors
in Windows. It also allows you to run commands as a single
string. Only use shell=True if you are passing in the
arguments yourself (it is a security hazard)
'''

subprocess.run(['ls', '-la']) # arguments need to be in a list if you're not using shell=True



