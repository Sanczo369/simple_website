from flask import Flask, render_template
from flask_wtf import FlaskForm 
from wtforms import StringField, EmailField, TextAreaField,TelField

app = Flask(__name__) 


class ContactForm(FlaskForm):
    name = StringField('Name')
    email = EmailField('Email')
    phone = TelField('Phone')
    text = TextAreaField('Text')






@app.route('/') 
def index(): 
    return render_template('index.html')

if __name__ == '__main__': 
    app.run()