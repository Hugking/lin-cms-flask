from flask import jsonify
from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint
from lin.exception import NotFound

from app.validators.forms import ThirdClientForm,WxClientForm
from app.models.third_client.third_bind import ThirdBind
from app.models.goods.goods import Goods

from flask import current_app as app

from app.models.shop.category import Category
from app.models.shop.attribute_category import Attribute_category
from app.validators.forms import CreateCategoryForm,SearchAllForm,CreateAttributeCategoryForm,CreateAttrForm,SearchNameForm,CreateKeywordsForm,CreateBrandForm

from app.models.shop.attribute import Attribute
from app.models.shop.keywords import Keywords
from app.models.shop.brand import Brand

shop_api = Redprint('shop')

"""
****************************
cate 首页分类
****************************
"""
@shop_api.route('/cate/<id>', methods=['GET'])
def get_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    category = Category.get_detail(id)
    if category is None:
        resp['code'] = -1
        resp['msg'] = "暂无此分类，请稍后重试"
        return jsonify(resp)
    resp['data']['category'] = category
    return jsonify(resp)
    
@shop_api.route('/cate/', methods=['GET'])
def get_cates():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    category = Category.get_all()
    if category is None:
        resp['code'] = -1
        resp['msg'] = "暂无此分类，请先创建"
        return jsonify(resp)
    resp['data']['category'] = category
    return jsonify(resp)

@shop_api.route('/cate/search',methods=['POST'])
def search_cate():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchNameForm().validate_for_api()
    category = Category.search_by_name(form.name.data)
    if category is None:
        resp['code'] = -1
        resp['msg'] = "未查询到相关分类"
        return jsonify(resp)
    resp['data']['category'] = category
    return jsonify(resp)

@shop_api.route('/cate/',methods=['POST'])
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

@shop_api.route('/cate/<id>',methods=['PUT'])
def update_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateCategoryForm().validate_for_api()
    category =  Category.edit(id,form)
    if category is False:
        resp['code'] = -1
        resp['msg'] = "此分类不存在或名称重复"
        return jsonify(resp)
    resp['data']['category'] = category
    return jsonify(resp)

@shop_api.route('/cate/<id>',methods=['DELETE'])
def delete_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    category =  Category.remove(id)
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
@shop_api.route('/attr_cate/<id>', methods=['GET'])
def get_attr_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    attr_cate = Attribute_category.get_detail(id)
    if attr_cate is None:
        resp['code'] = -1
        resp['msg'] = "暂无此属性类，请稍后重试"
        return jsonify(resp)
    resp['data']['attr_cate'] = attr_cate
    return jsonify(resp)
    
@shop_api.route('/attr_cate/', methods=['GET'])
def get_attr_cates():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchAllForm().validate_for_api()
    attr_cate = Attribute_category.get_all({'page':int(form.page.data),'size':int(form.size.data)})
    if attr_cate is None:
        resp['code'] = -1
        resp['msg'] = "暂无属性类，请先创建"
        return jsonify(resp)
    resp['data']['attr_cate'] = attr_cate
    return jsonify(resp)

@shop_api.route('/attr_cate/search',methods=['POST'])
def search_attr_cate():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchNameForm().validate_for_api()
    attr_cate = Attribute_category.search_by_name(form.name.data)
    if attr_cate is None:
        resp['code'] = -1
        resp['msg'] = "未查询到相关信息"
        return jsonify(resp)
    resp['data']['attr_cate'] = attr_cate
    return jsonify(resp)

@shop_api.route('/attr_cate/',methods=['POST'])
def new_attr_cate():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateAttributeCategoryForm().validate_for_api()
    attr_cate = Attribute_category.new(form)
    if attr_cate is False:
        resp['code'] = -1
        resp['msg'] = "已存在，请勿重复创建"
        return jsonify(resp)
    resp['data']['attr_cate'] = attr_cate
    return jsonify(resp)

@shop_api.route('/attr_cate/<id>',methods=['PUT'])
def update_attr_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateAttributeCategoryForm().validate_for_api()
    attr_cate =  Attribute_category.edit(id,form)
    if attr_cate is False:
        resp['code'] = -1
        resp['msg'] = "该类别不存在或名称重复"
        return jsonify(resp)
    resp['data']['attr_cate'] = attr_cate
    return jsonify(resp)

@shop_api.route('/attr_cate/<id>',methods=['DELETE'])
def delete_attr_cate(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    attr_cate =  Attribute_category.remove(id)
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
@shop_api.route('/attr/<id>', methods=['GET'])
def get_attr(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    attr = Attribute.get_detail(id)
    if attr is None:
        resp['code'] = -1
        resp['msg'] = "暂无此属性，请稍后重试"
        return jsonify(resp)
    resp['data']['attr'] = attr
    return jsonify(resp)
    
@shop_api.route('/attr/', methods=['GET'])
def get_attrs():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchAllForm().validate_for_api()
    attr = Attribute.get_all({'page':int(form.page.data),'size':int(form.size.data)})
    if attr is None:
        resp['code'] = -1
        resp['msg'] = "暂无属性，请先创建"
        return jsonify(resp)
    resp['data']['attr'] = attr
    return jsonify(resp)

@shop_api.route('/attr/search',methods=['POST'])
def search_attr():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchNameForm().validate_for_api()
    attr = Attribute.search_by_name(form.name.data)
    if attr is None:
        resp['code'] = -1
        resp['msg'] = "未查询到相关信息"
        return jsonify(resp)
    resp['data']['attr'] = attr
    return jsonify(resp)

@shop_api.route('/attr/',methods=['POST'])
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

@shop_api.route('/attr/<id>',methods=['PUT'])
def update_attr(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateAttrForm().validate_for_api()
    attr =  Attribute.edit(id,form)
    if attr is False:
        resp['code'] = -1
        resp['msg'] = "该属性不存在或名称重复"
        return jsonify(resp)
    resp['data']['attr'] = attr
    return jsonify(resp)

@shop_api.route('/attr/<id>',methods=['DELETE'])
def delete_attr(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    attr =  Attribute.remove(id)
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
@shop_api.route('/keywords/<id>', methods=['GET'])
def get_keywords(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    keywords = Keywords.get_detail(id)
    if keywords is None:
        resp['code'] = -1
        resp['msg'] = "暂无此关键词，请稍后重试"
        return jsonify(resp)
    resp['data']['keywords'] = keywords
    return jsonify(resp)
    
@shop_api.route('/keywords/', methods=['GET'])
def get_keywordss():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchAllForm().validate_for_api()
    keywords = Keywords.get_all({'page':int(form.page.data),'size':int(form.size.data)})
    if keywords is None:
        resp['code'] = -1
        resp['msg'] = "暂无关键词，请先创建"
        return jsonify(resp)
    resp['data']['keywords'] = keywords
    return jsonify(resp)

@shop_api.route('/keywords/',methods=['POST'])
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

@shop_api.route('/keywords/<id>',methods=['PUT'])
def update_keywords(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateKeywordsForm().validate_for_api()
    keywords =  Keywords.edit(id,form)
    if keywords is False:
        resp['code'] = -1
        resp['msg'] = "该关键词不存在"
        return jsonify(resp)
    resp['data']['keywords'] = keywords
    return jsonify(resp)

@shop_api.route('/keywords/<id>',methods=['DELETE'])
def delete_keywords(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    keywords =  Keywords.remove(id)
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
@shop_api.route('/brand/<id>', methods=['GET'])
def get_brand(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    brand = Brand.get_detail(id)
    if brand is None:
        resp['code'] = -1
        resp['msg'] = "暂无此品牌，请稍后重试"
        return jsonify(resp)
    resp['data']['brand'] = brand
    return jsonify(resp)
    
@shop_api.route('/brand/', methods=['GET'])
def get_brands():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = SearchAllForm().validate_for_api()
    brand = Brand.get_all({'page':int(form.page.data),'size':int(form.size.data)})
    if brand is None:
        resp['code'] = -1
        resp['msg'] = "暂无品牌，请先创建"
        return jsonify(resp)
    resp['data']['brand'] = brand
    return jsonify(resp)

@shop_api.route('/brand/search',methods=['POST'])
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

@shop_api.route('/brand/',methods=['POST'])
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

@shop_api.route('/brand/<id>',methods=['PUT'])
def update_brand(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    form = CreateBrandForm().validate_for_api()
    brand =  Brand.edit(id,form)
    if brand is False:
        resp['code'] = -1
        resp['msg'] = "该品牌不存在或名称重复"
        return jsonify(resp)
    resp['data']['brand'] = brand
    return jsonify(resp)

@shop_api.route('/brand/<id>',methods=['DELETE'])
def delete_brand(id):
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    brand =  Brand.remove(id)
    if brand is False:
        resp['code'] = -1
        resp['msg'] = "该品牌不存在或已删除"
        return jsonify(resp)
    return jsonify(resp)