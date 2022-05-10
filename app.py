from flask import Flask, render_template, session, request, jsonify
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = b'S\xc5\xf5\xf4!\x9d=S\t\xb4\xb8\xcb\xb5\x16\x1cfXj\xde\x85\xe7\xf5\xe4\xe2'
SESSION_TYPE = 'redis'


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="db"
)
cursor = db.cursor()


@app.route('/')
def hello():
    session.pop('uid')
    return render_template('index.html')


@app.route('/main')
def main():
    uid = session.get('uid')
    userData = None
    if uid is not None:
        cursor.execute("select shopname, shoptype, latitude, longitude from shop where uid = %s", (uid, ))
        tmp = cursor.fetchone()
        userData = {
            'shopName': tmp[0],
            'shopType': tmp[1],
            'latitude': tmp[2],
            'longitude': tmp[3]
        }
    return render_template('nav.html', userData=userData)


@app.route('/shopRegister')
def shopRegister():
    return 'Not implemented'


@app.route('/validateShopName', methods=['POST'])
def validateShopName():
    name = request.form.get('name')
    cursor.execute("select * from shop where shopname = %s", (name, ))
    res = cursor.fetchall()
    if len(res) > 0:
        return jsonify({'result': 'This Name is used!'})
    return jsonify({'result': ''})


if __name__ == "__main__":
    app.run(debug=True)
