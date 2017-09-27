# -*- coding: utf-8 -*-
from fabric.api import env, run, cd
from fabric.operations import sudo

GIT_REPO = "https://github.com/guoweikuang/django_cms.git"

env.user = 'root'
env.password = 'GUOweikuang2017!'

env.hosts = ['demo.guoweikuang.com']
env.port = '22'


def deploy():
    source_folder = '/home/guoweikuang/project/django_cms'

    run('cd %s && git pull ' % source_folder)
    run("""
        cd {} &&
        /home/guoweikuang/project/venv/bin/pip install -r requirements.txt &&
        /home/guoweikuang/project/venv/bin/python3 manage.py collectstatic --noinput &&
        /home/guoweikuang/project/venv/bin/python3 manage.py migrate
        """.format(source_folder))
    with cd(source_folder):
        sudo('/home/guoweikuang/project/venv/bin/python3 manage.py runserver 0.0.0.0:8009')
    
