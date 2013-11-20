import contextlib
from fabric.api import env, run, cd, sudo, put, require, settings, hide, puts
from fabric.contrib import project, files
from fabric.contrib.files import upload_template


env.user = "ubuntu"
env.hosts = ['ec2-23-21-150-134.compute-1.amazonaws.com']
env.key_filename = ["demo.pem"]
env.repo_url = 'git@github.com:joashxu/django-tesseract.git'

env.root = "/home/ubuntu/webapps/tesseract"
env.virtualenv = "%s/tesseractenv" % env.root
env.project = "%s/django-tesseract" % env.root
env.servicename = "setarisocr"


def deploy():
    "Full deploy: push, buildout, and reload."
    push()
    update_dependencies()
    update_services()
    reload()


def push():
    "Push out new code to the server."
    with cd("%(project)s" % env):
        run("git pull origin master")


def update_services():
    upload_template('./deployment/nginx.conf',
        '/etc/nginx/sites-enabled/default', use_sudo=True)
    upload_template('./deployment/service.conf',
        '/etc/init/setarisocr.conf', use_sudo=True)


def update_dependencies():
    run("%(virtualenv)s/bin/pip install -r %(project)s/requirements.txt" % env)


def reload():
    with settings(warn_only=True):
        sudo("stop setarisocr")
    sudo("start setarisocr")
    sudo('/etc/init.d/nginx reload')


def setup():
    run("mkdir -p %(root)s" % env)
    sudo("aptitude update")
    sudo("aptitude -y install git-core python-dev python-setuptools "
        "build-essential subversion mercurial nginx"
        "libjpeg62 libjpeg62-dev zlib1g-dev libfreetype6 libfreetype6-dev "
        "ghostscript imagemagick "
        "libtesseract-dev")

    sudo("easy_install virtualenv")
    run("virtualenv %(virtualenv)s" % env)
    run("%(virtualenv)s/bin/pip install -U pip" % env)

    with cd("~/webapps/tesseract"):
       run("git clone %(repo_url)s" % env)
       run("touch %(project)s/djangotesseract/localsettings.py")

    sudo('nginx')

    deploy()
