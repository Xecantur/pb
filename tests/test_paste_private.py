from time import time
from hashlib import sha1
from yaml import load

from flask import url_for

from pb.pb import create_app

def test_insert_private():
    app = create_app()

    c = str(time())
    rv = app.test_client().post('/', data=dict(
        c = c,
        p = 1
    ))
    location = rv.headers.get('Location')
    data = load(rv.get_data())
    assert sha1(c.encode('utf-8')).hexdigest() in location

    rv = app.test_client().get(location)
    assert rv.status_code == 200

    with app.test_request_context():
        url = url_for('paste.put', uuid=data.get('uuid'))
    
    f = lambda c: app.test_client().put(url, data=dict(
        c = c
    ))

    rv = f(c)
    assert rv.status_code == 409

    rv = f(str(time()))
    assert rv.status_code == 200

    rv = app.test_client().delete(url)
    assert rv.status_code == 200
    
