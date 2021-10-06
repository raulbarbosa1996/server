from flask import Flask


def create_server(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/sr')

    from models import db
    db.init_app(app)

    return app


if __name__ == "__main__":
    app = create_server("config")
    app.run(host='0.0.0.0', port=5550,debug=True)
