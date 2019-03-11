from mongoengine import Document, StringField

class Give(Document):
    amount = StringField()
    recipient = StringField()
