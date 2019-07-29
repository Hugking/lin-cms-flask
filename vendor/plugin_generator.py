"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
import argparse
import os

banner = """
\"""
    :copyright: © 2019 by the wkaanig.
    :license: MIT, see LICENSE for more details.
\"""
"""

controller = """
from lin.redprint import Redprint

{0}_api = Redprint("{0}")


@{0}_api.route("/", methods=["GET"])
def test():
    return "hi, guy!"
"""

init = """
from .controller import {0}_api
from .model import *


def initial_data():
    from app.app import create_app
    from lin.db import db

    app = create_app()
    return app
"""

info = """
__name__ = '{0}'
__version__ = '0.1.0'
__author__ = 'wkaanig'
"""

readme = """# {0}"""

interInfo = """
from ..model import *


class {0}():
    def test_{0}():
        pass
"""

formInfo = """
from lin import manager
from wtforms import DateTimeField, PasswordField, FieldList, IntegerField, StringField, FloatField, DecimalField, TextField
from wtforms.validators import DataRequired, Regexp, EqualTo, length, Optional, NumberRange
import time

from lin.forms import Form
"""


def create_plugin(name: str):
    cmd = os.getcwd()
    plugins_path = os.path.join(cmd, "app/plugins")
    plugindir = os.path.join(plugins_path, name)
    os.mkdir(plugindir)

    open(os.path.join(plugindir, "config.py"), mode="x", encoding="utf-8")
    open(os.path.join(plugindir, "requirements.txt"), mode="x", encoding="utf-8")

    with open(os.path.join(plugindir, "info.py"), mode="x", encoding="utf-8") as f:
        f.write(banner + info.format(name))

    with open(os.path.join(plugindir, "README.md"), mode="x", encoding="utf-8") as f:
        f.write(readme.format(name))

    appdir = os.path.join(plugindir, "app")
    os.mkdir(appdir)

    with open(os.path.join(appdir, "__init__.py"), mode="x", encoding="utf-8") as f:
        f.write(banner + init.format(name))

    with open(os.path.join(appdir, "controller.py"), mode="x", encoding="utf-8") as f:
        f.write(banner + controller.format(name))

    open(os.path.join(appdir, "model.py"), mode="x", encoding="utf-8")

    with open(os.path.join(appdir, "form.py"), mode="x", encoding="utf-8") as f:
        f.write(banner + formInfo)

    interfacedir = os.path.join(appdir, "interface")
    os.mkdir(interfacedir)

    with open(os.path.join(interfacedir, name + ".py"), mode="x", encoding="utf-8") as f:
        f.write(banner + interInfo.format(name.capitalize()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("-n", "--name", default="tpl", help="the name of plugin", dest="name")
    args = parser.parse_args()
    name = args.name
    create_plugin(name)
