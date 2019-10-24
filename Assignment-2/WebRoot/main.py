from flask import Flask, render_template, request, json, redirect, url_for, session
import os.path
import sys
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__,template_folder="templates/static")

app.url_map.strict_slashes = False
app.secret_key = "temp"  
app._static_folder = os.path.abspath("templates/static/")





@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('layouts/home.html')


@app.route("/register", methods=['GET'])
def regget():
    return render_template('/layouts/register.html', result="")


@app.route("/register", methods=['POST'])
def reg():
    _name = request.form['username']
    _pword = request.form['password']
    _2fa = request.form['2fa']
    print(_pword)
    print(_name)
    if _name and _pword:
        with open('userList.json', mode='a+', encoding='utf-8') as feedsjson:
            feedsjson.seek(0, os.SEEK_END)
            feedsjson.seek(feedsjson.tell() - 1, os.SEEK_SET)
            feedsjson.truncate()
            feedsjson.write(',')
            if _2fa:
                entry = {'username': _name, 'password': _pword, '2fa': _2fa}
                json.dump(entry, feedsjson)
            else:
                entry = {'username': _name, 'password': _pword, '2fa': ''}
                json.dump(entry, feedsjson)
            feedsjson.write(']')
        return render_template("/layouts/register.html", result="success")
    else:
        return render_template("/layouts/register.html", result="failure")


@app.route("/login", methods=['GET'])
def loginget():
    return render_template("layouts/login.html", result="")


@app.route("/login", methods=['POST'])
def loginpost():
    _name = request.form['username']
    _pword = request.form['password']
    _2fa = request.form['2fa']
    result=""
    if _name and _pword:
        with open('userList.json') as json_file:
            data = json.load(json_file)
            # print(len(data))
            for i in data:
                if i['username'] == _name and i['password'] == _pword and i['2fa'] == _2fa:
                    session['username'] = request.form['username']
                    result ="success"
                    return redirect(url_for('spellCheck'))
                    # return "logged"
                else:
                    result ="failure"
                    return render_template("layouts/login.html", result=result)    
    else:
        result ="failure"
        return render_template("layouts/login.html", result=result)


@app.route("/spellcheck", methods=['GET'])
def spellCheck():
    if 'username' in session:
        username = session['username']
        if username:
            return render_template('layouts/spellCheck.html')
    return redirect(url_for('loginget'))


@app.route("/spellcheck", methods=['POST'])
def spellCheckPost():
    if 'username' in session:
        username = session['username']
        print(username)
        print("inside spell post")
        text = request.form['text']
        # print(text)

        f = open('tmp.txt', 'w+')
        f.write(text)
        f.close()

        fr = open('tmp.txt', 'r')
        misspelled = None
        outFile = open('Output.txt', 'ab+')

        try:
            os.chdir(
            '/home/nikhila/My Stuff/AppSec/ApplicationSecurity/Assignment-2/WebRoot/')
            cmd = ['./spell_check', 'tmp.txt', 'wordlist.txt']
            p = subprocess.check_output(cmd, stderr=subprocess.PIPE)
            misspelled = p
            print(misspelled)
            outFile.write(misspelled)
            outFile.close()
        except OSError as e:
            print("error %s" % e.strerror)

        fr.close()
        session.pop('username', None)
        return misspelled

    return "You are not logged in <br><a href = '/login'></b>" + "click here to log in</b></a>"
    

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('username', None)
    # return "logged out"
    return url_for('loginget')

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
