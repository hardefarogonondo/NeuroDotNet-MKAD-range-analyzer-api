from blueprint import mkad_blueprint
from flask import Flask

app = Flask(__name__)
app.register_blueprint(mkad_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
