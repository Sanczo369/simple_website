from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import FlaskForm 
from wtforms import StringField, EmailField, TextAreaField,TelField
from flask_mail import Mail, Message
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

import logging


app = Flask(__name__) 
# konfiguracja
app.config.from_pyfile('config.cfg')
mail = Mail(app)
db = SQLAlchemy(app)

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100)) 

class NewsletterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()],render_kw={"placeholder": "Twój email", "id":"email"})
    
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = TelField('Phone', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    
@app.route('/', methods=['GET', 'POST'])
def index():
    db.create_all() 
    form = ContactForm()
    newsform = NewsletterForm()
    if newsform.validate_on_submit():
        email = newsform.email.data
        logging.info(f"Formularz wysłany przez: ({email})")
        new_email = Newsletter(email=email)
        logging.error(f"Utworzenie nowego rekordu: ({email})")
        db.session.add(new_email)
        logging.error(f"Dodanie nowego rekordu: ({email})")
        db.session.commit()
        logging.error(f"zapisanie nowego rekordu: ({email})")
        
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        text = form.text.data
    
        
        # Tworzenie wiadomości email
        subject = "Wiadomość od {} ({})".format(name, email)
        body = "Wiadomość: {}\nTelefon: {}".format(text, phone)
        message = Message(subject=subject, body=body, recipients=["test.test.test@vp.pl"])
        
        # Wysyłanie wiadomości
        mail.send(message)
        return redirect('/')
    
    return render_template('index.html', form=form , newsform=newsform)


@app.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    return render_template('newsletter.html')

if __name__ == '__main__': 
    app.run()