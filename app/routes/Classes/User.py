from mongoengine import Document, StringField

class User(Document):
    name = StringField()
    email = StringField()
    student_id = StringField()
    wallet = StringField()
    image = StringField()
