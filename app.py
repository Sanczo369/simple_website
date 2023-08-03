from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import FlaskForm 
from wtforms import StringField, EmailField, TextAreaField,TelField
from flask_mail import Mail, Message
from wtforms.validators import DataRequired

app = Flask(__name__) 
# konfiguracja
app.config.from_pyfile('config.cfg')
mail = Mail(app)

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone = TelField('Phone', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    
@app.route('/', methods=['GET', 'POST'])
def index(): 
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        return render_template('success.html', )  # Przekierowanie na nowy widok dla sukcesu
    else:    
        return render_template('index.html', form=form)


if __name__ == '__main__': 
    app.run()