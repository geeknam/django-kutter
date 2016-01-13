import subprocess
import webbrowser

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


def docker_compose_up():
    commands = [
        'docker-compose', 'up', '-d',
    ]
    print 'Firing up new "{{cookiecutter.repo_name}}" containers...'
    process = subprocess.Popen(
        commands, stdout=subprocess.PIPE
    )
    process.communicate()


def open_browser():
    ip = subprocess.check_output(
        ['docker-machine', 'ip', '{{cookiecutter.repo_name}}']
    ).split('\n')[0]
    webbrowser.open('http://%s' % ip)


create_docker_machine()
docker_compose_up()
open_browser()