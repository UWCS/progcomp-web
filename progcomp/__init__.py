from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", MAX_CONTENT_LENGTH=20 * 1000 * 1000  # 20mb
    )

    from . import routes

    app.register_blueprint(routes.bp)

    return app


app = create_app()
