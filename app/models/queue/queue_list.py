from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer
from lin.db import db
import json,requests

from app.models.third_client.third_bind import ThirdBind
from app.libs.wx_pay import WxPay

class QueueList(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    queue_name = Column(String(30), nullable=False, default=' ')
    data = Column(String(500), nullable=False, default = '')
    status = Column(Integer, nullable=False, default = '-1')

    @classmethod
    def add_queue(cls, queue_name, data=None):
        model_queue = QueueList()
        model_queue.queue_name = queue_name
        if data:
            model_queue.data = json.dumps(data)
        db.session.add(model_queue)
        db.session.commit()
        return True
    
    



