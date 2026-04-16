from flask import Flask
from src.partidos.routes import partidos_bp
from src.usuarios.routes import usuarios_bp

app = Flask(__name__)
app.register_blueprint(partidos_bp)
app.register_blueprint(usuarios_bp)

if __name__ == "__main__":
    app.run(debug=True)
