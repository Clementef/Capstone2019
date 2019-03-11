from mongoengine import Document, StringField

class Transaction(Document):
    giver = StringField()
    recipient = StringField()
    amount = StringField()
