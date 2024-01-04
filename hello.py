from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"

# from class
class Namerform(FlaskForm):
    name = StringField("Votre nom svp", validators=[DataRequired()])
    submit = SubmitField("Soumettre")
@app.route('/')
# def index():
#     return "<h1>Hello World</h1>"

def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', user_name=name)

#invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

