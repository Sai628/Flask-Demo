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

from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Required

from datetime import datetime


class NameForm(Form):
    name = StringField('你的名字?', validators=[Required()])
    submit = SubmitField('提交')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_test'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


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


if __name__ == '__main__':
    manager.run()
