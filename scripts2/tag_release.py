import sys
import os
import re

sys.path.append(os.path.dirname(__file__))  # noqa

from base import run_process, check_exit_code, get_project_version, configure_git


if __name__ == '__main__':
    configure_git()
    version = get_project_version()

    if not version:
        print('Unable to get the current version')
        sys.exit(1)

    tag_exists = check_exit_code([
        f'git show-ref --tags --quiet --verify -- "refs/tags/{version}"'
    ]) == 0

    if not tag_exists:
        run_process([
            'git', 'tag', version
        ])

        run_process([
            'git', 'push', '--tags'
        ])
