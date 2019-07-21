from flask import jsonify
from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint
from lin.exception import NotFound
from app.validators.forms import ThirdClientForm,WxClientForm,SearchAllForm,SearchNameForm,CreateGoodsForm
from app.models.third_client.third_bind import ThirdBind
from app.models.goods.goods import Goods

goods_api = Redprint('goods')

@goods_api.route('/<id>', methods=['GET'])
def get_brand(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    goods = Goods.get_detail(id)
    if goods is None:
        resp['code'] = -1
        resp['msg'] = "暂无此商品，请稍后重试"
        return jsonify(resp)
    resp['data']['goods'] = goods
    return jsonify(resp)
    
@goods_api.route('/', methods=['GET'])
def get_brands():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchAllForm().validate_for_api()
    goods = Goods.get_all({'page':int(form.page.data),'size':int(form.size.data)})
    if goods is None:
        resp['code'] = -1
        resp['msg'] = "暂无商品，请先创建"
        return jsonify(resp)
    resp['data']['goods'] = goods
    return jsonify(resp)

@goods_api.route('/search',methods=['POST'])
def search_brand():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchNameForm().validate_for_api()
    goods = Goods.search_by_name(form.name.data)
    if goods is None:
        resp['code'] = -1
        resp['msg'] = "未查询到相关信息"
        return jsonify(resp)
    resp['data']['goods'] = goods
    return jsonify(resp)

@goods_api.route('/',methods=['POST'])
def new_brand():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateGoodsForm().validate_for_api()
    goods = Goods.new(form)
    if goods is False:
        resp['code'] = -1
        resp['msg'] = "已存在商品或商品分类不存在"
        return jsonify(resp)
    resp['data']['goods'] = goods
    return jsonify(resp)

@goods_api.route('/<id>',methods=['PUT'])
def update_brand(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateGoodsForm().validate_for_api()
    goods =  Goods.edit(id,form)
    if goods is False:
        resp['code'] = -1
        resp['msg'] = "该商品不存在或名称重复"
        return jsonify(resp)
    resp['data']['goods'] = goods
    return jsonify(resp)

@goods_api.route('/<id>',methods=['DELETE'])
def delete_brand(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    goods =  Goods.remove(id)
    if goods is False:
        resp['code'] = -1
        resp['msg'] = "该商品不存在或已删除"
        return jsonify(resp)
    return jsonify(resp)