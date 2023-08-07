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

# inicjalizacji rozszerzenia
mail = Mail(app) 
db = SQLAlchemy(app)

# konfiguracja logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# klasy
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
    if request.method == 'POST':
        if newsform.validate_on_submit():
            
            # Tworzenie nowego rekordu w bazie Newsletter
            email = newsform.email.data
            logging.info(f"Formularz wysłany przez: ({email})")
            new_email = Newsletter(email=email)
            logging.error(f"Utworzenie nowego rekordu: ({email})")
            db.session.add(new_email)
            logging.error(f"Dodanie nowego rekordu: ({email})")
            db.session.commit()
            logging.error(f"zapisanie nowego rekordu: ({email})")
            
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            phone = form.phone.data
            text = form.text.data
        
            # Tworzenie wiadomości email
            subject = "Wiadomość od {} ({})".format(name, email)
            body = "Wiadomość: {}\nTelefon: {}".format(text, phone)
            message = Message(subject=subject, body=body, recipients=app.config.get("MAIL_RECIPIENTS", []))
            
            # Wysyłanie wiadomości
            mail.send(message)
            return redirect('/')
    
    return render_template('index.html', form=form , newsform=newsform)

# wyświetlanie rekordów newslettera
@app.route('/newsletter')
def newsletter():
    email_addresses = Newsletter.query.all()
    return render_template('newsletter.html', email_addresses=email_addresses)

# usuwanie rekordu
@app.route('/remove_email/<int:email_addresses_id>')
def remove_email(email_addresses_id):
    del_email= Newsletter.query.filter(Newsletter.id==email_addresses_id).first()
    db.session.delete(del_email)
    db.session.commit()
    return redirect(url_for('newsletter'))

if __name__ == '__main__': 
    app.run()