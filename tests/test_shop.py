import sys
import os

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))
from app.app import create_app

app = create_app()


def test_new_cate():
    with app.test_client() as c:
        rv = c.post('/wx/shop/cate/', json={
            'name': '干花', 'keywords': '店铺推荐'
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200


def test_update_cate():
    with app.test_client() as c:
        rv = c.put('/wx/shop/cate/2',json={
            'name': '鲜花', 'keywords': '店铺推荐',
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200

def test_new_attr_cate():
    with app.test_client() as c:
        rv = c.post('/wx/shop/attr_cate/', json={
            'name': '夏季必备', 
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200

def test_update_attr_cate():
    with app.test_client() as c:
        rv = c.put('/wx/shop/attr_cate/3',json={
            'name': '春季必备'
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200

def test_new_attr():
    with app.test_client() as c:
        rv = c.post('/wx/shop/attr/',json={
            'name': '规格',
            'attribute_category_id':'3'
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200

def test_update_attr():
    with app.test_client() as c:
        rv = c.put('/wx/shop/attr/5',json={
            'name': '尺码',
            'attribute_category_id':'2'
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200

def test_new_keywords():
    with app.test_client() as c:
        rv = c.post('/wx/shop/keywords/',json={
            'is_default': '1'
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200

def test_update_keywords():
    with app.test_client() as c:
        rv = c.put('/wx/shop/keywords/3',json={
            'is_dafault': '0',
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200

def test_new_brand():
    with app.test_client() as c:
        rv = c.post('/wx/shop/brand/',json={
            'name': 'NIICK制造商',
            "floor_price":'39.90'
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200

def test_update_brand():
    with app.test_client() as c:
        rv = c.put('/wx/shop/brand/3',json={
            'name':'LV制造商',
            'floor_price':'19.90',
        })
        json_data = rv.get_json()
        print(json_data)
        assert rv.status_code == 200