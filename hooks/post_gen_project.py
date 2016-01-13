import subprocess
import webbrowser
import os


def create_docker_machine():
    commands = [
        'docker-machine', 'create', '--driver',
        'virtualbox', '{{cookiecutter.repo_name}}'
    ]
    print 'Creating a new docker-machine: {{cookiecutter.repo_name}}...'
    process = subprocess.Popen(
        commands, stdout=subprocess.PIPE
    )
    process.communicate()


def set_envs():

    envs = [
        'docker-machine', 'env', 'kutta'
    ]
    process = subprocess.Popen(
        envs, stdout=subprocess.PIPE
    )
    res = process.communicate()[0].split('\n')
    output = [
        line
        for line in res
        if line.startswith('export')
    ][:-1]

    for line in output:
        env = line.split(' ')[1]
        key, value = env.split('=')
        os.environ[key] = value


def docker_compose_up():
    commands = [
        'docker-compose', 'up', '-d',
    ]
    print 'Firing up new "{{cookiecutter.repo_name}}" containers...'
    process = subprocess.Popen(
        commands, stdout=subprocess.PIPE,
        env=dict(os.environ)
    )
    process.communicate()


def open_browser():
    ip = subprocess.check_output(
        ['docker-machine', 'ip', '{{cookiecutter.repo_name}}']
    ).split('\n')[0]
    webbrowser.open('http://%s' % ip)


create_docker_machine()
set_envs()
docker_compose_up()
open_browser()
