from app.routes import app
from flask import render_template, session, request, redirect, flash
from .Forms import GiveForm
from.Classes import Transaction
import requests

@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    form = GiveForm(request.form)

    if request.method == 'POST' and form.validate():

        newTransaction = Transaction()
        newTransaction.giver = session['displayName']
        newTransaction.recipient = form.recipient.data
        newTransaction.amount = form.amount.data
        newTransaction.save()

        flash("You successfully sent " + form.amount.data + " currency to " + form.recipient.data)
        return redirect("/dashboard")


    return render_template('dashboard.html', name=session["displayName"], image=session["image"], wallet=10, form=form)
