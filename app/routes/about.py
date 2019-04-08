from app.routes import app
from flask import render_template, session

@app.route("/about")
def about():
    return render_template('about.html')
