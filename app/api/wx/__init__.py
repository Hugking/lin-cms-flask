from flask import Blueprint
from app.api.wx import member


def create_wx():
    bp_wx = Blueprint('wx', __name__)
    member.member_api.register(bp_wx)
    return bp_wx