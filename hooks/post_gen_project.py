import subprocess

commands = [
    'docker-machine', 'create', '--driver',
    'virtualbox', '{{cookiecutter.repo_name}}'
]

process = subprocess.Popen(
    commands, stdout=subprocess.PIPE
)
process.communicate()
