#!/usr/bin/env python

# coding=utf-8
#
# This file is part of Hypothesis, which may be found at
# https://github.com/HypothesisWorks/hypothesis-python
#
# Most of this work is copyright (C) 2013-2017 David R. MacIver
# (david@drmaciver.com), but it contains contributions by others. See
# CONTRIBUTING.rst for a full list of people who may hold copyright, and
# consult the git log if you need to determine who owns an individual
# contribution.
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
#
# END HEADER

import os
import sys
import shutil
import subprocess

import tooling as tools

sys.path.append(os.path.dirname(__file__))  # noqa


DIST = os.path.join(tools.ROOT, 'dist')


if __name__ == '__main__':
    last_release = tools.latest_version()

    print('Current version: %s. Latest released version: %s' % (
        tools.__version__, last_release
    ))

    HEAD = tools.hash_for_name('HEAD')
    MASTER = tools.hash_for_name('origin/master')
    print('Current head:', HEAD)
    print('Current master:', MASTER)

    on_master = tools.is_ancestor(HEAD, MASTER)
    has_release = tools.has_release()

    if not on_master:
        print('Not deploying due to not being on master')
        sys.exit(0)

    if not has_release:
        print('Not deploying due to no release')
        sys.exit(0)

    if has_release:
        print('Updating changelog and version')
        tools.update_for_pending_release()

    print('Building the package...')

    if os.path.exists(DIST):
        shutil.rmtree(DIST)

    subprocess.check_call([
        'poetry', 'build'
    ])

    print('Release seems good. Pushing to GitHub now.')

    tools.create_tag_and_push()

    print('Now uploading to pypi.')

    subprocess.check_call([
        'poetry',
        'publish',
        '--username', os.environ['PYPI_USERNAME'],
        '--password', os.environ['PYPI_PASSWORD']
    ])

    sys.exit(0)
