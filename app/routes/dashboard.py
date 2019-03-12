from app.routes import app
from flask import render_template, session, request, redirect, flash
from .Forms import GiveForm
from .Classes import Transaction, User
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

        for recipient in User.objects:
            if recipient.name == newTransaction.recipient:
                recipient.update(wallet = str(int(recipient.wallet) + int(newTransaction.amount)))
        for giver in User.objects:
            if giver.name == newTransaction.giver:
                giver.update(wallet = str(int(giver.wallet) - int(newTransaction.amount)))


        flash("You successfully sent " + form.amount.data + " currency to " + form.recipient.data)
        return redirect("/dashboard")

    # Update Wallet
    for user in User.objects:
        if user.name == session["displayName"]:
            session["wallet"] = user.wallet
    return render_template('dashboard.html', name=session["displayName"], image=session["image"], wallet=session["wallet"], form=form)
