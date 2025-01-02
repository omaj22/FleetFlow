from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)