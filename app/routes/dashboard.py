from app.routes import app
from flask import render_template, session, request
from .Forms import GiveForm
import requests

@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    form = GiveForm(request.form)
    return render_template('dashboard.html', name=session["displayName"], image=session["image"], form=form)
