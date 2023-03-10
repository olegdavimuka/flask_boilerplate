"""
This module contains the Flask application factory function create_app(),
which initializes and configures the Flask app and its extensions. It also
defines the API resources and their endpoints.

Dependencies:
    - Flask
    - Flask-Migrate
    - Flask-RESTful
    - Flask-SQLAlchemy
    - app.config.Config (module)
    - app.utils.logging.setup_logging (function)

Exported Functions:
    - create_app(config_class=Config): Creates and configures the Flask app.

"""

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.config import Config
from app.utils.logging import setup_logging

db = SQLAlchemy()
migrate = Migrate(db)


def create_app(config_class=Config):  # pylint: disable=too-many-locals
    """
    The create_app() function initializes and configures the Flask app
    by setting the configuration, initializing the database, and registering
    the REST API endpoints. It then sets up logging and returns the Flask app instance.

    Args:
        - config_class (Config, optional): A configuration class to use.
        Defaults to app.config.Config.

    Returns:
        - app (Flask): A Flask application instance.

    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.rest.purses import (  # pylint: disable=import-outside-toplevel, cyclic-import
        PursesAPI,
        PursesListAPI,
    )
    from app.rest.transactions import (  # pylint: disable=import-outside-toplevel, cyclic-import
        TransactionsAPI,
        TransactionsListAPI,
    )
    from app.rest.users import (  # pylint: disable=import-outside-toplevel, cyclic-import
        UsersAPI,
        UsersListAPI,
    )

    api = Api(prefix="/api")
    api.add_resource(UsersListAPI, "/users/")
    api.add_resource(UsersAPI, "/users/<int:_id>")
    api.add_resource(PursesListAPI, "/purses/")
    api.add_resource(PursesAPI, "/purses/<int:_id>")
    api.add_resource(TransactionsListAPI, "/transactions/")
    api.add_resource(TransactionsAPI, "/transactions/<int:_id>")

    api.init_app(app)

    from app.views.home import (  # pylint: disable=import-outside-toplevel, cyclic-import
        HomeView,
    )
    from app.views.purses import (  # pylint: disable=import-outside-toplevel, cyclic-import
        PurseBlueprint,
    )
    from app.views.transactions import (  # pylint: disable=import-outside-toplevel, cyclic-import
        TransactionBlueprint,
    )
    from app.views.users import (  # pylint: disable=import-outside-toplevel, cyclic-import
        UserBlueprint,
    )

    app.add_url_rule("/", view_func=HomeView.as_view("home"))
    user_bp = UserBlueprint("user_bp", __name__, url_prefix="/users")
    purse_bp = PurseBlueprint("purse_bp", __name__, url_prefix="/purses")
    transaction_bp = TransactionBlueprint(
        "transaction_bp", __name__, url_prefix="/transactions"
    )
    app.register_blueprint(user_bp)
    app.register_blueprint(purse_bp)
    app.register_blueprint(transaction_bp)

    setup_logging()

    return app
