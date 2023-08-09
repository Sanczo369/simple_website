from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import FlaskForm 
from wtforms import StringField, EmailField, TextAreaField, TelField, PasswordField, BooleanField
from flask_mail import Mail, Message
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
import logging


app = Flask(__name__) 
# konfiguracja
app.config.from_pyfile('config.cfg')

# inicjalizacji rozszerzenia
mail = Mail(app) 
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# konfiguracja logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# klasy
class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100)) 
    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100)) 
    email = db.Column(db.String(100))     

class NewsletterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()],render_kw={"placeholder": "Twój email", "id":"email"})
    
class ContactForm(FlaskForm):
    name = StringField('Nazwa', validators=[DataRequired()],render_kw={"placeholder": "Jan Nowak"})
    email = EmailField('Email', validators=[DataRequired()],render_kw={"placeholder": "jannowak@nowak.pl"})
    phone = TelField('Numer', validators=[DataRequired()],render_kw={"placeholder": "0123456789"})
    text = TextAreaField('Tekst', validators=[DataRequired()],render_kw={"placeholder": "text"})
    
@app.route('/', methods=['GET', 'POST'])
def index():
    db.create_all() 
    form = ContactForm()
    newsform = NewsletterForm()
    if request.method == 'POST':
        if newsform.validate_on_submit():
            
            # Tworzenie nowego rekordu w bazie Newsletter
            email = newsform.email.data
            new_email = Newsletter(email=email)
            db.session.add(new_email)
            db.session.commit()
            
        elif form.validate_on_submit():
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

@app.route('/logout')
def logout():
    return "<h1>You are logged out</h1>"


if __name__ == '__main__': 
    app.run()