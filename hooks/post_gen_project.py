import subprocess

commands = [
    'docker-machine', 'create', '{{cookiecutter.repo_name}}'
]

process = subprocess.Popen(
    commands, stdout=subprocess.PIPE
)
process.communicate()
