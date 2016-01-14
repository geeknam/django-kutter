import subprocess
import webbrowser
import os


class CommandLine(object):

    def __init__(self, command):
        self.command = command
        self.command_split = command.split(' ')

    def run(self, with_envs=True):
        if with_envs:
            process = subprocess.Popen(
                self.command_split, stdout=subprocess.PIPE,
            )
        else:
            process = subprocess.Popen(
                self.command_split, stdout=subprocess.PIPE,
                env=dict(os.environ)
            )
        return process.communicate()

    def get_return(self):
        return subprocess.check_output(
            self.command_split
        ).split('\n')[0]


def create_docker_machine():

    print 'Creating a new docker-machine: {{cookiecutter.repo_name}}...'
    CommandLine(
        'docker-machine create --driver virtualbox {{cookiecutter.repo_name}}'
    ).run()


def set_envs():
    output = CommandLine('docker-machine env {{cookiecutter.repo_name}}').run()
    output = [
        line
        for line in output[0].split('\n')
        if line.startswith('export')
    ][:-1]

    for line in output:
        env = line.split(' ')[1]
        key, value = env.split('=')
        os.environ[key] = value[1:-1]


def docker_compose_up():
    print 'Firing up new "{{cookiecutter.repo_name}}" containers...'
    CommandLine('docker-compose up -d').run()


def get_ip():
    return CommandLine(
        'docker-machine ip {{cookiecutter.repo_name}}'
    ).get_return()


def append_host_file(ip):
    CommandLine(
        'sudo echo "%s {{cookiecutter.repo_name}}.dev" >> /etc/hosts' % ip
    ).run()


create_docker_machine()
set_envs()
docker_compose_up()
ip = get_ip()
append_host_file(ip)
webbrowser.open('http://{{cookiecutter.repo_name}}.dev')
