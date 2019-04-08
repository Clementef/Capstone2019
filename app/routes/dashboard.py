from app.routes import app
from flask import render_template, session, request, redirect, flash
from .Forms import GiveForm
from .Classes import Transaction, User
import requests


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = GiveForm(request.form)

    if request.method == 'POST' and form.validate():
        validTransaction = False
        # check transaction validity
        for giver in User.objects:
            if giver.name == session["displayName"]:

                # check that the amount is an integer
                try:
                    data = int(form.amount.data)
                    if data >= 0:
                        validTransaction = True
                except ValueError:
                    flash("Please enter a number as the amount")
                    return redirect("/dashboard")

                # check that all fields are filled
                if form.amount.data != '' and form.recipient.data != '':
                    validTransaction = True
                else:
                    flash("Please fill all fields before submitting")
                    return redirect("/dashboard")

                # check that giver isn't giving money to themselves
                if (giver.name != form.recipient.data):
                    validTransaction = True
                else:
                    flash("You can't give it to yourself, " +
                          giver.name[0:giver.name.find(" ")])
                    return redirect("/dashboard")

                # check if giver has enough money
                if (int(giver.wallet) >= int(form.amount.data)):
                    validTransaction = True
                else:
                    flash("You can't send " + form.amount.data +
                          " when you only have " + giver.wallet)
                    return redirect("/dashboard")

        # if valid
        if validTransaction:
            # get giver data
            for user in User.objects:
                if user.name == session["displayName"]:
                    giveUser = user

            # get recipient data
            for user in User.objects:
                if user.name == form.recipient.data:
                    recipientUser = user

            # create the transaction
            newTransaction = Transaction()
            newTransaction.giver = giveUser
            newTransaction.recipient = recipientUser
            newTransaction.amount = form.amount.data
            newTransaction.save()

            # transfer currency between users and give reputation
            for recipient in User.objects:
                if recipient.name == newTransaction.recipient.name:
                    recipient.update(wallet=str(
                        int(recipient.wallet) + int(newTransaction.amount)))
                    recipient.update(reputation=str(
                        int(recipient.reputation) + int(newTransaction.amount)))
            for giver in User.objects:
                if giver.name == newTransaction.giver.name:
                    giver.update(wallet=str(int(giver.wallet) -
                                            int(newTransaction.amount)))
                    giver.update(reputation=str(
                        int(giver.reputation) + int(newTransaction.amount)))

            flash("You successfully sent " + form.amount.data +
                  " currency to " + form.recipient.data)
            return redirect("/dashboard")

    # Update Wallet
    for user in User.objects:
        if user.name == session["displayName"]:
            session["wallet"] = user.wallet
            session["reputation"] = user.reputation

    totalMoney = 0
    totalTransactions = 0
    for transaction in list(Transaction.objects):
        if (transaction.giver.name == session["displayName"] or transaction.recipient.name == session["displayName"]):
            totalMoney += int(transaction.amount)
            totalTransactions += 1
    totalRep = totalMoney * 2

    return render_template('dashboard.html', name=session["displayName"], image=session["image"], wallet=session["wallet"], reputation=session["reputation"], form=form,
                                             totalMoney = totalMoney, totalRep = totalRep, totalTransactions = totalTransactions)
