# coding: utf-8

from __future__ import with_statement

from fabric.api import local, settings, abort
from fabric.contrib.console import confirm

__all__ = [
    'prepare_deploy',
    'test'
]


def test():
    with settings(warn_only=True):
        unit_test = local("make test", capture=True)
        func_test = local("make selenium", capture=True)
        results = [
            unit_test,
            func_test
        ]
    for result in results:
        if result.failed and not confirm("Test failed. Continue anyway?"):
            abort("Aborting at user request.")


def commit(ticket, msg):
    result = local(
        "git add --all && git commit -m 'ticket:%d tests %s'" %
        (int(ticket), msg)
    )
    if result.failed:
        abort("Invalid commit.")


def push(branch):
    local("git push origin %s" % branch)


def pull(branch):
    local("git pull origin %s" % branch)


def prepare_deploy(ticket=None, msg=None, branch=None):
    """Deploy with pass/failed tests.
    """
    test()
    commit(ticket, msg)
    push(branch)
    pull(branch)
