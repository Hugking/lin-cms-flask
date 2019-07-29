
"""
    :copyright: © 2019 by the wkaanig.
    :license: MIT, see LICENSE for more details.
"""

from .controller import wx_api
from .model import Pay, PayAccessToken, PayCallbackData, PayRefund, ThirdBind


def initial_data():
    from app.app import create_app
    from lin.db import db

    app = create_app()
    return app
