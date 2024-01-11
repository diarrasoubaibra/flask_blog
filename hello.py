from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:@localhost/our_users'
app.config['SECRET_KEY'] = "my super secret key"
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

# from class
class Userform(FlaskForm):
    name = StringField("Votre nom svp", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Soumettre")


# from class
class Namerform(FlaskForm):
    name = StringField("Votre nom svp", validators=[DataRequired()])
    submit = SubmitField("Soumettre")


@app.route('/user/add', methods=['GET','POST'])
def add_user():
    name = None
    form = Userform()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            with app.app_context():
                db.session.add(user)
                db.session.commit()  
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("Utilisateur ajouté avec succès")
    our_users = Users.query.order_by(Users.date_added)

    return render_template('add_user.html',
                           form=form,
                           name=name,
                           our_users=our_users,)

@app.route('/')
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


# Create a name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name=None
    form = Namerform()
    #validate form
    if form.validate_on_submit():
        name=form.name.data
        form.name.data=''
        flash("Form Submitted Successfully!")
    return render_template('name.html',
                           name=name,
                           form=form)

if __name__ =='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# if __name__ =='__main__':
#     app.run(debug=True)
