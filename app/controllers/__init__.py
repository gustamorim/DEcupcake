def register_controllers(app):
    from app.controllers.home_controller import home_bp
    from app.controllers.catalog_controller import catalog_bp
    from app.controllers.cart_controller import cart_bp
    from app.controllers.checkout_controller import checkout_bp
    from app.controllers.order_controller import order_bp
    from app.controllers.account_controller import account_bp

    for blueprint in (home_bp, catalog_bp, cart_bp, checkout_bp, order_bp, account_bp):
        app.register_blueprint(blueprint)
