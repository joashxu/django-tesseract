import contextlib
from fabric.api import env, run, cd, sudo, put, require, settings, hide, puts
from fabric.contrib import project, files

env.user = "ubuntu"
env.hosts = ['ec2-23-21-150-134.compute-1.amazonaws.com']
env.key_filename = ["demo.pem"]
env.repo_url = 'git@github.com:setaris/django-tesseract.git'

env.root = "~/webapps/tesseract"
env.virtualenv = "%s/tesseractenv" % env.root
env.project = "%s/django-tesseract" % env.root


def deploy():
    "Full deploy: push, buildout, and reload."
    push()
    update_dependencies()
    reload()


def push():
    "Push out new code to the server."
    with cd("%(project)s" % env):
        sudo("git pull origin master")


def update_dependencies():
    sudo("%(virtualenv)s/bin/pip install -r %(project)s/requirements.txt" % env)


def reload():
    sudo("invoke-rc.d apache2 reload")


def setup():
    sudo("mkdir -p %(root)s" % env)
    sudo("aptitude update")
    sudo("aptitude -y install git-core python-dev python-setuptools "
        "build-essential subversion mercurial apache2 "
        "libapache2-mod-wsgi")

    sudo("easy_install virtualenv")
    sudo("virtualenv %(virtualenv)s" % env)
    sudo("%(virtualenv)s/bin/pip install -U pip" % env)

    with cd("~/webapps/tesseract"):
        sudo("git clone %(repo_url)s" % env)

    with cd("/etc/apache2"):
        sudo("rm -rf apache2.conf conf.d/ httpd.conf magic mods-* sites-* ports.conf")
        sudo("ln -s %(project)s/apache2.conf ." % env)
        sudo("mkdir -m777 -p /var/www/.python-eggs")

    deploy()
