import sys
import os
import re

sys.path.append(os.path.dirname(__file__))  # noqa

from base import run_process, get_project_version, git, PROJECT_TOML_FILE_NAME, CHANGELOG_FILE_NAME, RELEASE_FILE_NAME


if __name__ == '__main__':
    version = get_project_version()

    git([
        'config', 'user.name', 'Marco Acierno'
    ])

    git([
        'config', 'user.email', 'marcoaciernoemail@gmail.com'
    ])

    git([
        'add', PROJECT_TOML_FILE_NAME,
    ])

    git([
        'add', CHANGELOG_FILE_NAME,
    ])

    run_process([
        'rm', RELEASE_FILE_NAME,
    ])

    git([
        'add', RELEASE_FILE_NAME,
    ])

    git([
        'commit', '-m', f'Release 🍓 {version}'
    ])

    git([
        'push'
    ])
