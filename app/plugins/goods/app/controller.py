"""
    :copyright: Â© 2019 by the wkaanig.
    :license: MIT, see LICENSE for more details.
"""

from lin.redprint import Redprint
from flask import jsonify, request
from ..app.interface.goods import *
from .form import *

goods_api = Redprint("goods")


@goods_api.route('/<id>', methods=['GET'])
def get_goods(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    mini = True if 'mini' in request.values else False
    goods = Goods.get_detail(id, mini)
    if goods is None:
        resp['code'] = -1
        resp['msg'] = "暂无此商品，请稍后重试"
        return jsonify(resp)
    resp['data']['goods'] = goods
    return jsonify(resp)


@goods_api.route('/', methods=['GET'])
def get_goodss():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    mini = True if 'mini' in request.values else False
    form = SearchAllForm().validate_for_api()
    goods = Goods.get_all({'page': int(form.page.data), 'size': int(form.size.data)}, mini)
    if goods is None:
        resp['code'] = -1
        resp['msg'] = "暂无商品，请先创建"
        return jsonify(resp)
    resp['data']['goods'] = goods
    return jsonify(resp)


@goods_api.route('/search', methods=['POST'])
def search_goods():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    mini = True if 'mini' in request.values else False
    form = SearchGoodsForm().validate_for_api()
    goods = Goods.search_by_keywords(form, mini)
    if goods is None:
        resp['code'] = -1
        resp['msg'] = "未查询到相关信息"
        return jsonify(resp)
    resp['data']['goods'] = goods
    return jsonify(resp)


@goods_api.route('/', methods=['POST'])
def new_goods():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateGoodsForm().validate_for_api()
    goods = Goods.new(form)
    if goods is False:
        resp['code'] = -1
        resp['msg'] = "已存在商品或商品分类不存在"
        return jsonify(resp)
    resp['data']['goods'] = goods
    return jsonify(resp)


@goods_api.route('/<id>', methods=['PUT'])
def update_goods(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateGoodsForm().validate_for_api()
    goods = Goods.edit(id, form)
    if goods is False:
        resp['code'] = -1
        resp['msg'] = "该商品不存在或名称重复"
        return jsonify(resp)
    resp['data']['goods'] = goods
    return jsonify(resp)


@goods_api.route('/<id>', methods=['DELETE'])
def delete_goods(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    goods = Goods.remove(id)
    if goods is False:
        resp['code'] = -1
        resp['msg'] = "该商品不存在或已删除"
        return jsonify(resp)
    return jsonify(resp)


@goods_api.route('/count', methods=['GET'])
def count_goods():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    goods = Goods.get_count()
    if not goods:
        resp['code'] = -1
        resp['msg'] = "暂无商品"
        return jsonify(resp)
    resp['data']['count'] = goods
    return jsonify(resp)


"""
************************************
goods_attr 单个商品属性
************************************
"""


@goods_api.route('/goods_attr/<id>', methods=['GET'])
def get_goods_attr(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    mini = True if 'mini' in request.values else False
    goods_attr = GoodsAttribute.get_detail(id, mini)
    if goods_attr is None:
        resp['code'] = -1
        resp['msg'] = "暂无此商品属性，请稍后重试"
        return jsonify(resp)
    resp['data']['goods_attr'] = goods_attr
    return jsonify(resp)


@goods_api.route('/goods_attr/', methods=['GET'])
def get_goods_attrs():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    mini = True if 'mini' in request.values else False
    form = SearchAllForm().validate_for_api()
    goods_attr = GoodsAttribute.get_all({'page': int(form.page.data), 'size': int(form.size.data)},
                                        mini)
    if goods_attr is None:
        resp['code'] = -1
        resp['msg'] = "暂无商品属性，请先创建"
        return jsonify(resp)
    resp['data']['goods_attr'] = goods_attr
    return jsonify(resp)


@goods_api.route('/goods_attr/search', methods=['POST'])
def search_goods_attr():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchGoodsAttrForm().validate_for_api()
    mini = True if form.mini.data else False
    goods_attr = GoodsAttribute.search_by_keywords(form, mini)
    if goods_attr is None:
        resp['code'] = -1
        resp['msg'] = "未查询到相关信息"
        return jsonify(resp)
    resp['data']['goods_attr'] = goods_attr
    return jsonify(resp)


@goods_api.route('/goods_attr/', methods=['POST'])
def new_goods_attr():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateGoodsAttrForm().validate_for_api()
    goods_attr = GoodsAttribute.new(form)
    if goods_attr is False:
        resp['code'] = -1
        resp['msg'] = "商品不存在或属性不存在"
        return jsonify(resp)
    if goods_attr is -1:
        resp['code'] = -1
        resp['msg'] = "此商品属性已存在，请重试"
        return jsonify(resp)
    resp['data']['goods_attr'] = goods_attr
    return jsonify(resp)


@goods_api.route('/goods_attr/<id>', methods=['PUT'])
def update_goods_attr(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateGoodsAttrForm().validate_for_api()
    goods_attr = GoodsAttribute.edit(id, form)
    if goods_attr is False:
        resp['code'] = -1
        resp['msg'] = "商品不存在或属性不存在"
        return jsonify(resp)
    if goods_attr is -1:
        resp['code'] = -1
        resp['msg'] = "此商品属性已存在，请重试"
        return jsonify(resp)
    resp['data']['goods_attr'] = goods_attr
    return jsonify(resp)


@goods_api.route('/goods_attr/<id>', methods=['DELETE'])
def delete_goods_attr(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    goods_attr = GoodsAttribute.remove(id)
    if goods_attr is False:
        resp['code'] = -1
        resp['msg'] = "该商品属性不存在或已删除"
        return jsonify(resp)
    return jsonify(resp)


"""
****************************
cate 首页分类
****************************
"""


@goods_api.route('/cate/<id>', methods=['GET'])
def get_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    category = Category.get_detail(id)
    if category is None:
        resp['code'] = -1
        resp['msg'] = "暂无此分类，请稍后重试"
        return jsonify(resp)
    resp['data']['category'] = category
    return jsonify(resp)


@goods_api.route('/cate/', methods=['GET'])
def get_cates():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchCategoryForm().validate_for_api()
    category = Category.get_all(form)
    if category is None:
        resp['code'] = -1
        resp['msg'] = "暂无此分类，请先创建"
        return jsonify(resp)
    resp['data']['category'] = category
    return jsonify(resp)


@goods_api.route('/cate/search', methods=['POST'])
def search_cate():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchCategoryForm().validate_for_api()
    category = Category.search_by_keywords(form)
    if category is None:
        resp['code'] = -1
        resp['msg'] = "未查询到相关分类"
        return jsonify(resp)
    resp['data']['category'] = category
    return jsonify(resp)


@goods_api.route('/cate/', methods=['POST'])
def new_cate():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateCategoryForm().validate_for_api()
    category = Category.new(form)
    if category is False:
        resp['code'] = -1
        resp['msg'] = "已存在此分类，请勿重复创建"
        return jsonify(resp)
    resp['data']['category'] = category
    return jsonify(resp)


@goods_api.route('/cate/<id>', methods=['PUT'])
def update_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateCategoryForm().validate_for_api()
    category = Category.edit(id, form)
    if category is False:
        resp['code'] = -1
        resp['msg'] = "此分类不存在或名称重复"
        return jsonify(resp)
    resp['data']['category'] = category
    return jsonify(resp)


@goods_api.route('/cate/<id>', methods=['DELETE'])
def delete_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    category = Category.remove(id)
    if category is False:
        resp['code'] = -1
        resp['msg'] = "此分类不存在或已删除"
        return jsonify(resp)
    return jsonify(resp)


"""
****************************
attr_cate 细节分类
****************************
"""


@goods_api.route('/attr_cate/<id>', methods=['GET'])
def get_attr_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    attr_cate = AttributeCategory.get_detail(id)
    if attr_cate is None:
        resp['code'] = -1
        resp['msg'] = "暂无此属性类，请稍后重试"
        return jsonify(resp)
    resp['data']['attr_cate'] = attr_cate
    return jsonify(resp)


@goods_api.route('/attr_cate/', methods=['GET'])
def get_attr_cates():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchAllForm().validate_for_api()
    attr_cate = AttributeCategory.get_all(
        {'page': int(form.page.data), 'size': int(form.size.data)})
    if attr_cate is None:
        resp['code'] = -1
        resp['msg'] = "暂无属性类，请先创建"
        return jsonify(resp)
    resp['data']['attr_cate'] = attr_cate
    return jsonify(resp)


@goods_api.route('/attr_cate/search', methods=['POST'])
def search_attr_cate():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchNameForm().validate_for_api()
    attr_cate = AttributeCategory.search_by_name(form.name.data)
    if attr_cate is None:
        resp['code'] = -1
        resp['msg'] = "未查询到相关信息"
        return jsonify(resp)
    resp['data']['attr_cate'] = attr_cate
    return jsonify(resp)


@goods_api.route('/attr_cate/', methods=['POST'])
def new_attr_cate():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateAttributeCategoryForm().validate_for_api()
    attr_cate = AttributeCategory.new(form)
    if attr_cate is False:
        resp['code'] = -1
        resp['msg'] = "已存在，请勿重复创建"
        return jsonify(resp)
    resp['data']['attr_cate'] = attr_cate
    return jsonify(resp)


@goods_api.route('/attr_cate/<id>', methods=['PUT'])
def update_attr_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateAttributeCategoryForm().validate_for_api()
    attr_cate = AttributeCategory.edit(id, form)
    if attr_cate is False:
        resp['code'] = -1
        resp['msg'] = "该类别不存在或名称重复"
        return jsonify(resp)
    resp['data']['attr_cate'] = attr_cate
    return jsonify(resp)


@goods_api.route('/attr_cate/<id>', methods=['DELETE'])
def delete_attr_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    attr_cate = AttributeCategory.remove(id)
    if attr_cate is False:
        resp['code'] = -1
        resp['msg'] = "该类别不存在或已删除"
        return jsonify(resp)
    return jsonify(resp)


"""
****************************
attr 总属性
****************************
"""


@goods_api.route('/attr/<id>', methods=['GET'])
def get_attr(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    mini = True if 'mini' in request.values else False
    attr = Attribute.get_detail(id, mini)
    if attr is None:
        resp['code'] = -1
        resp['msg'] = "暂无此属性，请稍后重试"
        return jsonify(resp)
    resp['data']['attr'] = attr
    return jsonify(resp)


@goods_api.route('/attr/', methods=['GET'])
def get_attrs():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    mini = True if 'mini' in request.values else False
    form = SearchAllForm().validate_for_api()
    attr = Attribute.get_all({'page': int(form.page.data), 'size': int(form.size.data)}, mini)
    if attr is None:
        resp['code'] = -1
        resp['msg'] = "暂无属性，请先创建"
        return jsonify(resp)
    resp['data']['attr'] = attr
    return jsonify(resp)


@goods_api.route('/attr/search', methods=['POST'])
def search_attr():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    mini = True if 'mini' in request.values else False
    params = request.values
    attr = Attribute.search_by_keywords(params, type=mini)
    if attr is None:
        resp['code'] = -1
        resp['msg'] = "未查询到相关信息"
        return jsonify(resp)
    resp['data']['attr'] = attr
    return jsonify(resp)


@goods_api.route('/attr/', methods=['POST'])
def new_attr():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateAttrForm().validate_for_api()
    attr = Attribute.new(form)
    if attr is False:
        resp['code'] = -1
        resp['msg'] = "已存在属性或属性类不存在"
        return jsonify(resp)
    resp['data']['attr'] = attr
    return jsonify(resp)


@goods_api.route('/attr/<id>', methods=['PUT'])
def update_attr(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateAttrForm().validate_for_api()
    attr = Attribute.edit(id, form)
    if attr is False:
        resp['code'] = -1
        resp['msg'] = "该属性不存在或名称重复"
        return jsonify(resp)
    resp['data']['attr'] = attr
    return jsonify(resp)


@goods_api.route('/attr/<id>', methods=['DELETE'])
def delete_attr(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    attr = Attribute.remove(id)
    if attr is False:
        resp['code'] = -1
        resp['msg'] = "该属性不存在或已删除"
        return jsonify(resp)
    return jsonify(resp)


"""
****************************
keywords 关键字
****************************
"""


@goods_api.route('/keywords/<id>', methods=['GET'])
def get_keywords(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    keywords = Keywords.get_detail(id)
    if keywords is None:
        resp['code'] = -1
        resp['msg'] = "暂无此关键词，请稍后重试"
        return jsonify(resp)
    resp['data']['keywords'] = keywords
    return jsonify(resp)


@goods_api.route('/keywords/', methods=['GET'])
def get_keywordss():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchAllForm().validate_for_api()
    keywords = Keywords.get_all({'page': int(form.page.data), 'size': int(form.size.data)})
    if keywords is None:
        resp['code'] = -1
        resp['msg'] = "暂无关键词，请先创建"
        return jsonify(resp)
    resp['data']['keywords'] = keywords
    return jsonify(resp)


@goods_api.route('/keywords/', methods=['POST'])
def new_keywords():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateKeywordsForm().validate_for_api()
    keywords = Keywords.new(form)
    if keywords is False:
        resp['code'] = -1
        resp['msg'] = "已存在属性或属性类不存在"
        return jsonify(resp)
    resp['data']['keywords'] = keywords
    return jsonify(resp)


@goods_api.route('/keywords/<id>', methods=['PUT'])
def update_keywords(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateKeywordsForm().validate_for_api()
    keywords = Keywords.edit(id, form)
    if keywords is False:
        resp['code'] = -1
        resp['msg'] = "该关键词不存在"
        return jsonify(resp)
    resp['data']['keywords'] = keywords
    return jsonify(resp)


@goods_api.route('/keywords/<id>', methods=['DELETE'])
def delete_keywords(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    keywords = Keywords.remove(id)
    if keywords is False:
        resp['code'] = -1
        resp['msg'] = "该关键词不存在或已删除"
        return jsonify(resp)
    return jsonify(resp)


"""
****************************
brand 品牌
****************************
"""


@goods_api.route('/brand/<id>', methods=['GET'])
def get_brand(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    brand = Brand.get_detail(id)
    if brand is None:
        resp['code'] = -1
        resp['msg'] = "暂无此品牌，请稍后重试"
        return jsonify(resp)
    resp['data']['brand'] = brand
    return jsonify(resp)


@goods_api.route('/brand/', methods=['GET'])
def get_brands():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchAllForm().validate_for_api()
    brand = Brand.get_all({'page': int(form.page.data), 'size': int(form.size.data)})
    if brand is None:
        resp['code'] = -1
        resp['msg'] = "暂无品牌，请先创建"
        return jsonify(resp)
    resp['data']['brand'] = brand
    return jsonify(resp)


@goods_api.route('/brand/search', methods=['POST'])
def search_brand():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchNameForm().validate_for_api()
    brand = Brand.search_by_name(form.name.data)
    if brand is None:
        resp['code'] = -1
        resp['msg'] = "未查询到相关信息"
        return jsonify(resp)
    resp['data']['brand'] = brand
    return jsonify(resp)


@goods_api.route('/brand/', methods=['POST'])
def new_brand():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateBrandForm().validate_for_api()
    brand = Brand.new(form)
    if brand is False:
        resp['code'] = -1
        resp['msg'] = "已存在品牌"
        return jsonify(resp)
    resp['data']['brand'] = brand
    return jsonify(resp)


@goods_api.route('/brand/<id>', methods=['PUT'])
def update_brand(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateBrandForm().validate_for_api()
    brand = Brand.edit(id, form)
    if brand is False:
        resp['code'] = -1
        resp['msg'] = "该品牌不存在或名称重复"
        return jsonify(resp)
    resp['data']['brand'] = brand
    return jsonify(resp)


@goods_api.route('/brand/<id>', methods=['DELETE'])
def delete_brand(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    brand = Brand.remove(id)
    if brand is False:
        resp['code'] = -1
        resp['msg'] = "该品牌不存在或已删除"
        return jsonify(resp)
    return jsonify(resp)
