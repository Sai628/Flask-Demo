# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask import render_template
from flask import session
from flask import url_for
from flask import redirect
from flask import flash

from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy

from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Required

import os
from datetime import datetime


baseDir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(baseDir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(Form):
    name = StringField('你的名字?', validators=[Required()])
    submit = SubmitField('提交')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    name_form = NameForm()
    if name_form.validate_on_submit():
        new_name = name_form.name.data
        old_name = session.get('name')
        if old_name is None or old_name == new_name:
            session['name'] = new_name
            name_form.name.data = ''
        else:
            flash('名字输入错误!')
        return redirect(url_for('index'))
    return render_template('index.html', form=name_form, name=session.get('name'), current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


db.create_all()
role_admin = Role(name='Admin')
user_tom = User(username='tom', role=role_admin)
user_jim = User(username='jim', role=role_admin)
user_tim = User(username='tim', role=role_admin)
user_sam = User(username='sam', role=role_admin)
db.session.add(role_admin)
db.session.add(user_tom)
db.session.add(user_jim)
db.session.commit()

print User.query.all()


if __name__ == '__main__':
    manager.run()
