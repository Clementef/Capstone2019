from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

"""
CSV VERSION
"""
# import pandas as pd
# import os
# def getNames():
#     cd = os.getcwd()
#     table = pd.read_csv(cd.replace('\\','/')+'/app/routes/Forms/data.csv')
#     student_names = table['Full Name'].unique()
#     data = list(zip(student_names, student_names))
#     return data

"""
DATABASE VERSION
"""
from flask import session
from app.routes.Classes import User

# full_name = session["displayName"]

def getNames():
    student_names = []
    for i in User.objects:
        student_names.append(i.name)
    # student_names = []
    # for i in User.objects:
    #     if i.name != full_name:
    #         student_names.append(i.name)
    data = list(zip(student_names, student_names))
    return data

class GiveForm(FlaskForm):
    amount = StringField("Amount")
    recipient = SelectField(label="To", choices=getNames())
    submit = SubmitField("Submit")
