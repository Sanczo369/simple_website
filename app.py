from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm 
from wtforms import StringField, EmailField, TextAreaField,TelField

app = Flask(__name__) 
# konfiguracja
app.config.from_pyfile('config.cfg')

class Contact:
    def __init__(self, name, phone, email, text):
        self.name = name
        self.phone = phone
        self.email = email
        self.text=text
        
class ContactForm(FlaskForm):
    name = StringField('Name')
    email = EmailField('Email')
    phone = TelField('Phone')
    text = TextAreaField('Text')






@app.route('/') 
def index(): 
    contact = Contact(name="Jan Nowak", email='email@email.pl', phone=111, text= 'text')
    form = ContactForm()
    return render_template('index.html', form=form)

if __name__ == '__main__': 
    app.run()