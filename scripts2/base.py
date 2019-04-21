import os
import subprocess
import re

ROOT = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

RELEASE_FILE_NAME = 'RELEASE.md'
RELEASE_FILE = os.path.join(ROOT, RELEASE_FILE_NAME)

PROJECT_TOML_FILE_NAME = 'pyproject.toml'
PROJECT_TOML_FILE = os.path.join(ROOT, PROJECT_TOML_FILE_NAME)

CHANGELOG_FILE_NAME = 'CHANGELOG.md'
CHANGELOG_FILE = os.path.join(ROOT, CHANGELOG_FILE_NAME)


def run_process(popenargs):
    return subprocess.check_output(popenargs).decode('ascii').strip()


def git(popenargs):
    # avoid decode ascii for the commit message
    return subprocess.check_output(['git', *popenargs])


def check_exit_code(popenargs):
    return subprocess.call(
        popenargs,
        # stdin=subprocess.DEVNULL,
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL,
        shell=True,
    )


def get_project_version():
    VERSION_REGEX = re.compile(r'^version\s*=\s*\"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\"$')

    with open(PROJECT_TOML_FILE) as f:
        for line in f:
            match = VERSION_REGEX.match(line)

            if match:
                return f'{int(match.group("major"))}.{int(match.group("minor"))}.{int(match.group("patch"))}'

    return None
