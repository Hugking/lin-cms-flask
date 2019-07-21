import sys
import os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))
from app.app import create_app

app = create_app()


def test_new_cate():
    with app.test_client() as c:
        rv = c.post('/wx/goods/', json={
            'category_id':'3',
            'name':'仙人掌',
            'brand_id':'3',
            'goods_num':'100',
            'goods_desc':'盆栽必备',
            'attribute_category':'3',
            'goods_unit':'盆',
            'primary_pic_url':'主图',
            'unit_price':'9.90',
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200


def test_update_cate():
    with app.test_client() as c:
        rv = c.put('/wx/goods/7', json={
            'category_id':'3',
            'name':'仙人球',
            'brand_id':'3',
            'goods_num':'100',
            'goods_desc':'盆栽必备',
            'attribute_category':'3',
            'goods_unit':'盆',
            'primary_pic_url':'主图',
            'unit_price':'9.90',
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200

