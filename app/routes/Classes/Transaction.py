from mongoengine import Document, StringField, ReferenceField
from .User import User


class Transaction(Document):
    giver = ReferenceField(User)
    recipient = ReferenceField(User)
    amount = StringField()
