from flask import jsonify
from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint
from lin.exception import NotFound
from app.validators.forms import ThirdClientForm,WxClientForm
from app.models.third_client.third_bind import ThirdBind
from app.models.goods.goods import Goods

goods_api = Redprint('goods')

@goods_api.route('/<id>', methods=['GET'])
def getGoods(id):
    goods = Goods.query.filter_by(id=id).first() # 通过Book模型在数据库中查询id=`id`的书籍
    if goods is None:
        raise NotFound(msg='没有找到相关书籍') # 如果书籍不存在，返回一个异常给前端
    return jsonify(goods)

@goods_api.route('/create',methods=['POST'])
def create():
    goods = Goods.create(
        name = '爱情',
        commit= True
    )
    print(goods)
    return jsonify(goods.name)
