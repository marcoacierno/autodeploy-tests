import sys
import os
import re
sys.path.append(os.path.dirname(__file__))  # noqa

from datetime import datetime

from base import run_process, get_release_info, RELEASE_FILE, CHANGELOG_FILE


if __name__ == '__main__':
    POETRY_DUMP_VERSION_OUTPUT = re.compile(r'Bumping version from \d+\.\d+\.\d+ to (?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)')
    CHANGELOG_HEADER_SEPARATOR = '========='

    type_, release_changelog = get_release_info()

    output = run_process(['poetry', 'version', type_])
    version_match = POETRY_DUMP_VERSION_OUTPUT.match(output)

    if not version_match:
        print('Unable to bump the project version using poetry')
        sys.exit(1)

    new_version = f"{version_match.group('major')}.{version_match.group('minor')}.{version_match.group('patch')}"
    current_date = datetime.utcnow().strftime('%Y-%m-%d')

    old_changelog_data = ''
    header = ''

    with open(CHANGELOG_FILE, 'r') as f:
        lines = f.readlines()

    for index, line in enumerate(lines):
        if CHANGELOG_HEADER_SEPARATOR != line.strip():
            continue

        old_changelog_data = lines[index + 1:]
        header = lines[:index + 1]
        break

    with open(CHANGELOG_FILE, 'w') as f:
        f.write(''.join(header))

        new_version_header = f'{new_version} - {current_date}'

        f.write(f"\n{'-' * len(new_version_header)}\n")
        f.write(f'{new_version_header}\n')
        f.write(f"{'-' * len(new_version_header)}\n\n")

        f.write('\n'.join(release_changelog))
        f.write('\n')

        f.write(''.join(old_changelog_data))
