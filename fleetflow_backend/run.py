from flask import Flask, Blueprint
from logic import logic_bp

app = Flask('__name__')
app.register_blueprint(logic_bp)
app.secret_key = 'my_secrete_key'

if __name__ == '__main__':
    app.run(port=3000, debug=True)