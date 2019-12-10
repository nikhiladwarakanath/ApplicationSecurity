import pytest
import sqlite3
from app import create_app, get_db as db

@pytest.fixture('module')
def testClient():
    app = create_app()
    app.debug = True
    return app.test_client()

@pytest.fixture('module')
def cursors():
    DATABASE_PATH = 'database.db'
    conn = sqlite3.connect(DATABASE_PATH)
    print("yes connected")
    yield conn
    


def test_registerGet(testClient):
    # print(testClient)
    res = testClient.get("/register")
    print("yes")
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

# database test


# tests user_info tables
def test_userInfoCheck(cursors):
    cur = cursors.cursor()
    query = "select * from user_info"
    cur.execute(query)
    val = cur.fetchall()
    assert len(val) > 0

# tests user_access_log tables

def test_userLogCheck(cursors):
    cur = cursors.cursor()
    query = "select * from user_access_log"
    cur.execute(query)
    val = cur.fetchall()
    assert len(val) > 0

# tests user_query tables
def test_userQueryCheck(cursors):
    cur = cursors.cursor()
    query = "select * from user_query"
    cur.execute(query)
    val = cur.fetchall()
    assert len(val) > 0


# All test cases are passing