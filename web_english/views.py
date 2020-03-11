from web_english import app

@app.route("/")
def index():
    return "Это стартовая страница"
