from flask import Flask, render_template, request, json, redirect, url_for, session, Markup, make_response
from flask_bcrypt import Bcrypt
import os.path
import sys
import subprocess
import pytest
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect, CSRFError
import sqlite3
from flask import g

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def create_app():
    app = Flask(__name__, template_folder="templates/static")
    app.url_map.strict_slashes = False
    app.secret_key = "temp"
    app._static_folder = os.path.abspath("templates/static/")

    csrf = CSRFProtect(app)
    bcrypt = Bcrypt(app)
    

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()



    
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('/layouts/csrf_error.html', reason=e.description), 400


    @app.route('/home', methods=['GET', 'POST'])
    def home():
        return render_template('layouts/home.html')


    @app.route("/register", methods=['GET'])
    def regget():
        resp = make_response(render_template('/layouts/register.html', result="none"))
        print(resp.data)
        resp.headers['X-XSS-Protection'] = '1; mode=block'
        return resp



    @app.route("/register", methods=['POST'])
    def reg():
        _name = request.form['username']
        _pword = request.form['password']
        _2fa = request.form['2fa']

        
        
        if _name and _pword:

            pw_hash = bcrypt.generate_password_hash(_pword)
            stored_pw = pw_hash.decode('utf-8')
            cur = get_db().cursor()
            cur.execute("INSERT INTO user_info(username, password, twofactor) VALUES (?,?,?)", (_name, stored_pw,_2fa))
            
            get_db().commit()


            return render_template("/layouts/register.html", result=Markup("success"))
            # with open('userList.json', mode='a+', encoding='utf-8') as userJSON:
            #     userJSON.seek(0, os.SEEK_END)
            #     userJSON.seek(userJSON.tell() - 1, os.SEEK_SET)
            #     userJSON.truncate()
            #     pw_hash = bcrypt.generate_password_hash(_pword)
            #     userJSON.write(',')
            #     if _2fa:
            #         entry = {'username': _name,
            #                 'password': pw_hash.decode('utf-8'), '2fa': _2fa}
            #         json.dump(entry, userJSON)
            #     else:
            #         entry = {'username': _name, 'password': pw_hash, '2fa': ''}
            #         json.dump(entry, userJSON)
            #     userJSON.write(']')
            
        else:
            return render_template("/layouts/register.html", result=Markup("failure"))


    @app.route("/login", methods=['GET'])
    def loginget():
        return render_template("layouts/login.html", result=Markup('<p id="result" hidden>none</p>'))


    @app.route("/login", methods=['POST'])
    def loginpost():
        _name = request.form['username']
        _pword = request.form['password']
        print(_pword)
        _2fa = request.form['2fa']
        
        if _name and _pword:
            cur = get_db().cursor()
            cur.execute("INSERT INTO user_access_log(username, login_time) VALUES (?,?)", (_name,datetime.now()))
            get_db().commit()
            cur = get_db().cursor()
            cur.execute("select username, password, twofactor from user_info where username =?", (_name,))
            res = cur.fetchone()

            print(res)

            if res:
                uname = res[0]
                password = res[1]
                twofactor = res[2]
                if uname == _name and bcrypt.check_password_hash(password, _pword) and twofactor == _2fa:
                    session['username'] = request.form['username']
                    print("true")
                    return render_template("layouts/login.html", result=Markup('<p id="result" hidden>success</p>'))
                return render_template("layouts/login.html", result=Markup('<p id="result" hidden>failure</p>'))
            return render_template("layouts/login.html", result=Markup('<p id="result" hidden>failure</p>'))

            # with open('userList.json') as userJSON:
            #     data = json.load(userJSON)
            #     for i in data:
            #         print("data in file:"+i['password'])
            #         if i['username'] == _name and bcrypt.check_password_hash(i['password'], _pword) and i['2fa'] == _2fa:
            #             session['username'] = request.form['username']
            #             print("true")
            #             return render_template("layouts/login.html", result=Markup('<p id="result" hidden>success</p>'))
            #     return render_template("layouts/login.html", result=Markup('<p id="result" hidden>failure</p>'))
        else:
            return render_template("layouts/login.html", result=Markup('<p id="result" hidden>failure</p>'))

    
    
    @app.route("/history", methods=['GET'])
    def getHistory():
        if 'username' in session:
            username = session['username']
            if username:
                if username =='admin':
                    print("ADMIN")
                else:
                    cur = get_db().cursor()
                    cur.execute("select count(1) from user_query where user_name=?", (username,))
                    res = cur.fetchone()
                    counts = res[0]
                    print(res[0])

                    cur.execute("select queryid from user_query where user_name=?", (username,))
                    queries = cur.fetchall()
                return render_template('layouts/history.html', numqueries=counts, query=queries)
            return redirect(url_for('loginget'))
        return redirect(url_for('loginget'))

    @app.route("/history/review/<query>", methods=['GET'])
    def getReview(query):
        print(query)
        queryid = query.strip("query")
        print(queryid)
        if 'username' in session:
            username = session['username']
            if username:
                cur = get_db().cursor()
                cur.execute("select count(1) from user_query where user_name=?", (username,))
                res = cur.fetchone()
                counts = res[0]
                print(res[0])
                cur.execute("select queryid, user_name, input_text, result from user_query where user_name=? and queryid=?", (username,queryid,))
                queries = cur.fetchall()
                return render_template('layouts/review.html', numqueries=counts, query=queries)
            return redirect(url_for('loginget'))
        return redirect(url_for('loginget'))



    @app.route("/spell_check", methods=['GET'])
    def spellCheck():
        if 'username' in session:
            username = session['username']
            if username:
                return render_template('layouts/spellCheck.html', misspelled="")
        return redirect(url_for('loginget'))


    @app.route("/spell_check", methods=['POST'])
    def spellCheckPost():
        if 'username' in session:
            username = session['username']
            print(username)
            print("inside spell post")
            text = request.form['text']


            f = open('tmp.txt', 'w+')
            f.write(text)
            f.close()

            fr = open('tmp.txt', 'r')
            misspelled = None
            outFile = open('Output.txt', 'ab+')

            try:
                os.chdir(
                    '/home/nikhila/My Stuff/NYU/Fall 2019/Application Security/Assignment-2/ApplicationSecurity/Assignment-2/WebRoot/')
                cmd = ['./spell_check', 'tmp.txt', 'wordlist.txt']
                p = subprocess.check_output(cmd, stderr=subprocess.PIPE)
                misspelled = p.decode('ASCII')

                cur = get_db().cursor()
                cur.execute("INSERT INTO user_query(user_name, input_text, result) VALUES (?,?,?)", (username, text,misspelled))
                get_db().commit()

                print(misspelled)
                outFile.write(p)
                outFile.close()
                return render_template('/layouts/spellCheck.html', misspelled=misspelled)
            except OSError as e:
                print("error %s" % e.strerror)

            fr.close()
            session.pop('username', None)

        return "You are not logged in <br><a href = '/login'></b>" + "click here to log in</b></a>"


    @app.route("/logout", methods=['GET'])
    def logout():
        cur = get_db().cursor()
        username = session['username']
        cur.execute("select max(access_id) from user_access_log where logout_time is null and username=?", (username,))
        res = cur.fetchone()
        print(res[0])
        cur.execute("update user_access_log set logout_time=? where access_id = ?", (datetime.now(), res[0]))
        get_db().commit()
        session.pop('username', None)
        return url_for('loginget')
    
    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000, host="0.0.0.0")
    
