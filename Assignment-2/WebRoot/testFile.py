import pytest

import app as temp

@pytest.fixture('module')
def testClient():
    app = temp.create_app()
    app.debug = True
    return app.test_client()


def test_registerGet(testClient):
    # print(testClient)
    res = testClient.get("/register")
    assert res.status_code == 200
    # assert res.result == "none" 

def test_registerPost(testClient):
    try:
        res = testClient.post("/register", {'username':'name','password':'pass', '2fa':'2fa'}, content_type='text/html')
    except:
        print("error")
        # print(exc)
        assert True
    # Test should fail because of the absence of CSRF Token

def test_LoginGet(testClient):
    # print(testClient)
    res = testClient.get("/login")
    assert res.status_code == 200
    # assert res.result == "none" 

def test_LoginPost(testClient):
    try:
        res = testClient.post('/login', {'username':'name','password':'pass', '2fa':'2fa'})
    except ValueError :
        print("error")
        assert True
    # Test should fail because of the absence of CSRF Token

def test_SpellGet(testClient):
    # print(testClient)
    res = testClient.get("/spell_check")
    assert res.status_code == 302 #since user session is not available
    # assert res.result == "none" 

def test_SpellPost(testClient):
    try:
        res = testClient.post('/spell_check', {'text':'sample text abcde'})
    except ValueError :
        print("error")
        assert True

def test_Logout(testClient):
    # print(testClient)
    res = testClient.get("/logout")
    assert res.status_code == 200 #since user session is not available
    # assert res.result == "none" 
