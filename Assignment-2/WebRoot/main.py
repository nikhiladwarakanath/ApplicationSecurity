from flask import Flask, render_template, request, json
import os

app = Flask(__name__)


@app.route("/register", methods=['GET'])
def regget():
    return render_template('register.html')


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
        return "success"
    else:
        return "FFF"


@app.route("/login", methods=['GET'])
def loginget():
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def loginpost():
    _name = request.form['username']
    _pword = request.form['password']
    _2fa = request.form['2fa']
    if _name and _pword:
        with open('userList.json') as json_file:
            data = json.load(json_file)
            print(len(data))
            for i in data:
                if i['username'] == _name and i['password'] == _pword and i['2fa'] == _2fa:
                    return "logged"
        return "incorrect"
    else:
        return "FFF"


@app.route("/spellcheck")
def spellCheck():
    return "Spell Check"


if __name__ == "__main__":
    app.run(debug=True)
