set(
    projects = 'dali',
    fab_hosts = ['web41.webfaction.com'],
    webapp = '~/webapps/dali',
    repo = 'dali',
)


def git_pull():
    """Updates the repository."""
    run('cd $(webapp)/$(repo); git pull')

def git_reset():
    """Resets the repository to specified version."""
    run('cd $(webapp)/$(repo); git reset --head $(hash)') 

def reboot():
    """Reboot Apache2 server."""
    run('$(webapp)/apache2ctl/bin/restart')
    
def test():
    """Run tests on local server."""
    local('python manage.py test', fail='abort')

def update():
    """
    Update the production server.

    Runs the unit tests locally and if they pass, pulls the latest from
    git on the production server.    
    """
    test()
    git_pull()