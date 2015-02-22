# -*- coding: utf-8 -*-
'''
Directly manage the Salt fileserver plugins
'''

# Import Salt libs
import salt.fileserver


def dir_list(saltenv='base', outputter='nested'):
    '''
    List all directories in the given environment

    CLI Example:

    .. code-block:: bash

        salt-run fileserver.dir_list
        salt-run fileserver.dir_list saltenv=prod
    '''
    fileserver = salt.fileserver.Fileserver(__opts__)
    load = {'saltenv': saltenv}
    output = fileserver.dir_list(load=load)

    if outputter:
        salt.output.display_output(output, outputter, opts=__opts__)
    return output


def envs(backend=None, sources=False, outputter='nested'):
    '''
    Return the available fileserver environments. If no backend is provided,
    then the environments for all configured backends will be returned.

    CLI Example:

    .. code-block:: bash

        salt-run fileserver.envs
        salt-run fileserver.envs outputter=nested
        salt-run fileserver.envs backend=roots,git
    '''
    fileserver = salt.fileserver.Fileserver(__opts__)
    output = fileserver.envs(back=backend, sources=sources)

    if outputter:
        salt.output.display_output(output, outputter, opts=__opts__)
    return output


def file_list(saltenv='base', outputter='nested'):
    '''
    Return a list of files from the dominant environment

    CLI Example:

    .. code-block:: bash

        salt-run fileserver.file_list
        salt-run fileserver.file_list saltenv=prod
    '''
    fileserver = salt.fileserver.Fileserver(__opts__)
    load = {'saltenv': saltenv}
    output = fileserver.file_list(load=load)

    if outputter:
        salt.output.display_output(output, outputter, opts=__opts__)
    return output


def symlink_list(saltenv='base', outputter='nested'):
    '''
    Return a list of symlinked files and dirs

    CLI Example:

    .. code-block:: bash

        salt-run fileserver.symlink_list
        salt-run fileserver.symlink_list saltenv=prod
    '''
    fileserver = salt.fileserver.Fileserver(__opts__)
    load = {'saltenv': saltenv}
    output = fileserver.symlink_list(load=load)

    if outputter:
        salt.output.display_output(output, outputter, opts=__opts__)
    return output


def update(backend=None):
    '''
    Update the fileserver cache. If no backend is provided, then the cache for
    all configured backends will be updated.

    CLI Example:

    .. code-block:: bash

        salt-run fileserver.update
        salt-run fileserver.update backend=roots,git
    '''
    fileserver = salt.fileserver.Fileserver(__opts__)
    fileserver.update(back=backend)

    return True


def clear_cache(backend=None):
    '''
    .. versionadded:: 2015.2.0

    Clear the fileserver cache from VCS fileserver backends (:mod:`git
    <salt.fileserver.gitfs>`, :mod:`hg <salt.fileserver.hgfs>`, :mod:`svn
    <salt.fileserver.svnfs>`). Executing this runner with no arguments will
    clear the cache for all enabled VCS fileserver backends, but this
    can be narrowed using the ``backend`` argument.

    backend
        Only clear the update lock for the specified backend(s).

    CLI Example:

    .. code-block:: bash

        salt-run fileserver.update
        salt-run fileserver.update backend=git,hg
        salt-run fileserver.update backend=hg
    '''
    fileserver = salt.fileserver.Fileserver(__opts__)
    cleared, errors = fileserver.clear_cache(back=backend)
    ret = {}
    if cleared:
        ret['cleared'] = cleared
    if errors:
        ret['errors'] = errors
    if not ret:
        ret = 'No cache was cleared'
    salt.output.display_output(ret, 'nested', opts=__opts__)


def clear_lock(backend=None, remote=None):
    '''
    .. versionadded:: 2015.2.0

    Clear the fileserver update lock from VCS fileserver backends (:mod:`git
    <salt.fileserver.gitfs>`, :mod:`hg <salt.fileserver.hgfs>`, :mod:`svn
    <salt.fileserver.svnfs>`). This should only need to be done if a fileserver
    update was interrupted and a remote is not updating (generating a warning
    in the Master's log file). Executing this runner with no arguments will
    remove all update locks from all enabled VCS fileserver backends, but this
    can be narrowed by using the following arguments:

    backend
        Only clear the update lock for the specified backend(s).

    remote
        If not None, then any remotes which contain the passed string will have
        their lock cleared. For example, a ``remote`` value of **github** will
        remove the lock from all github.com remotes.

    CLI Example:

    .. code-block:: bash

        salt-run fileserver.clear_lock
        salt-run fileserver.clear_lock backend=git,hg
        salt-run fileserver.clear_lock backend=git remote=github
        salt-run fileserver.clear_lock remote=bitbucket
    '''
    fileserver = salt.fileserver.Fileserver(__opts__)
    cleared, errors = fileserver.clear_lock(back=backend, remote=remote)
    ret = {}
    if cleared:
        ret['cleared'] = cleared
    if errors:
        ret['errors'] = errors
    if not ret:
        ret = 'No locks were removed'
    salt.output.display_output(ret, 'nested', opts=__opts__)
