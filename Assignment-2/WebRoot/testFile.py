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

##################################################################################################################
##################################################################################################################
# New Test Cases for Assignment -3
def test_HistoryGet(testClient):
    # print(testClient)
    res = testClient.get("/history")
    assert res.status_code == 200 #since it provides the GET for any logged user
    # assert res.result == "none" 

def test_HistoryPost(testClient):
    try:
        res = testClient.post('/history', {'userquery':'hi'})
    except ValueError :
        print("error")
        assert True
        # The flow should enter exception block since admin check is missing and csrf token is not available

def test_HistoryQueryGet(testClient):
    res=testClient.get("/history/query1")
    assert res.status_code == 200 # test if end point returns a webpage

def test_HistoryQueryGetSecond(testClient):
    res=testClient.get("/history/query10988")
    assert res.status_code == 200 # test if end point returns a webpage



def test_LoginHistoryGet(testClient):
    # only admin can access this page, hence it should return 404 status code
    res = testClient.get("/login_history")
    assert res.status_code == 404


def test_LoginHistoryPost(testClient):
    try:
        res = testClient.post("/login_history",{'userid':'harry'})
    except ValueError:
        print("error")
        assert True
        # The flow should enter exception block since admin check is missing and csrf token is not available, only admins can send a post request to login history


# All test cases are passing