import os

from flask import Flask, jsonify, render_template, request

from db import init_db, query_products


def create_app(test_config=None):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

    if test_config:
        app.config.update(test_config)

    # Set up SQLite (creates + seeds products.db on first run)
    init_db(app)

    FEATURES = [
        {"icon": "⚡", "title": "Lightning Fast", "desc": "Optimized performance that keeps your workflow smooth and snappy."},
        {"icon": "🎨", "title": "Beautiful by Default", "desc": "Modern UI with thoughtful spacing, typography, and color."},
        {"icon": "🔐", "title": "Secure & Reliable", "desc": "Built-in best practices so your data stays safe, day and night."},
        {"icon": "📱", "title": "Fully Responsive", "desc": "Looks stunning on desktop, tablet, and every phone size."},
        {"icon": "🌙", "title": "Dark Mode Ready", "desc": "One-tap theme switching that remembers your preference."},
        {"icon": "🧩", "title": "Easy to Extend", "desc": "Clean, modular code that grows with your project."},
    ]

    TESTIMONIALS = [
        {"name": "Sarah Wijaya", "role": "Product Designer", "avatar": "🧑‍🎨", "text": "The cleanest template I've used. Beautiful defaults, zero fuss."},
        {"name": "Dimas Prakoso", "role": "Backend Engineer", "avatar": "🧑‍💻", "text": "Flask setup is tiny and readable — I shipped a feature in 20 minutes."},
        {"name": "Anisa Putri", "role": "Startup Founder", "avatar": "👩‍💼", "text": "Our landing page went live the same day. Users love the look."},
    ]

    @app.context_processor
    def inject_globals():
        return {"app_name": "Aurora"}

    @app.route("/")
    def index():
        return render_template(
            "index.html",
            products=query_products(),
            features=FEATURES,
            testimonials=TESTIMONIALS,
        )

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/api/products")
    def api_products():
        category = request.args.get("category")
        items = query_products(category)
        return jsonify({"count": len(items), "items": items})

    @app.route("/api/health")
    def api_health():
        return jsonify({"status": "ok", "app": app.name})

    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "not found"}), 404
        return render_template("404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="127.0.0.1", port=5000, debug=debug)
