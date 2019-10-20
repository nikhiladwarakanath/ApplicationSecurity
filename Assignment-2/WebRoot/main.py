from flask import Flask, render_template, request, json, redirect, url_for
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.url_map.strict_slashes = False

UPLOAD_FOLDER = '/home/nikhila/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 


@app.route('/home',methods = ['GET', 'POST'])
def home(): 
    return render_template('home.html')

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
            #print(len(data))
            for i in data:
                if i['username'] == _name and i['password'] == _pword and i['2fa'] == _2fa:
                    return url_for('spellCheck')
                    #return "logged"
        return "incorrect"
    else:
        return "FFF"


@app.route("/spellcheck", methods=['GET'])
def spellCheck():
    return render_template('spellCheck.html')


@app.route("/spellcheck", methods=['POST'])
def spellCheckPost():
    print("inside spell post")
    file = request.files['file']
    print(file)
    if file:
            #filename = secure_filename(file.filename)
            print("exist")
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # paths = os.path.join(UPLOAD_FOLDER, filename)
                # try:
                #     fp = open(paths)
                # except IOError and FileNotFoundError:
                # # If not exists, create the file
                #     fileUpload = open(paths, "w")
                #     fileUpload.write(file.read())
    return "yes"



if __name__ == "__main__":
    app.run(debug=True,port=5000, host="0.0.0.0")
