import requests
from app.routes import app
from flask import render_template, session, redirect, request
from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
from .Classes import User, Transaction

google_auth = GoogleClient(
    client_id=("570439607080-1jbsss0dpsh9uf2ho0ng4vg999ioq38d"
               ".apps.googleusercontent.com"),
    client_secret="74a6PgTOympeG-WNgrOctcD7",
    redirect_uri="http://localhost:5000/oauth2callback"
    # "http://localhost:5000/oauth2callback"
    # "https://computerinv-216303.appspot.com/oauth2callback"
)


@app.route('/', methods=['GET', 'POST'])
def index():
    ledgerTransactions = list(Transaction.objects[:9])[::-1]

    totalMoney = 0
    for transaction in list(Transaction.objects):
        totalMoney += int(transaction.amount)
    totalTransactions = len(list(Transaction.objects))

    leaderboardUsers = list(User.objects.order_by('-reputation')[:9])

    return render_template('index.html', ledgerTransactions=ledgerTransactions, leaderboardUsers=leaderboardUsers, totalMoney = str(totalMoney), totalRep = str(totalMoney*2), totalTransactions = str(totalTransactions))


@app.route('/login')
def login():
    if not session.get("access_token"):
        return redirect("/oauth2callback")
    with requests.Session() as s:
        s.auth = OAuth2BearerToken(session["access_token"])
        r = s.get("https://www.googleapis.com/plus/v1/people/me?access_token={}".format(
            session.get("access_token")))
    r.raise_for_status()
    data = r.json()

    if data["domain"] != "ousd.org":
        return "Please Sign in with your OUSD account"

    # Save Necessary variables
    session["displayName"] = data["displayName"]
    session["image"] = data["image"]["url"]

    user = User()

    for i in User.objects:
        if i.name == session["displayName"]:
            session["wallet"] = i.wallet
            session["reputation"] = i.reputation
            return redirect("/")
    user.name = session["displayName"]
    user.image = session["image"]
    user.wallet = "10"
    user.reputation = "0"
    session["wallet"] = user.wallet
    session["reputation"] = user.reputation
    user.save()

    return redirect("/")


@app.route("/oauth2callback")
def google_oauth2callback():
    code = request.args.get("code")
    error = request.args.get("error")
    if error:
        return "error :( {!r}".format(error)
    if not code:
        return redirect(google_auth.authorize_url(
            scope=["profile", "email"],
            response_type="code",
        ))
    data = google_auth.get_token(
        code=code,
        grant_type="authorization_code",
    )
    session["access_token"] = data.get("access_token")
    return redirect("/login")


@app.route("/logout")
def logout():
    [session.pop(key) for key in list(session.keys()) if key != '_flashes']

    return redirect("/")
