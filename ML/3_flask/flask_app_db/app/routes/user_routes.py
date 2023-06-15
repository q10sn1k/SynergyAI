from flask import Blueprint, render_template, request, redirect, url_for
from app.models import User
from app import db

bp = Blueprint('user_routes', __name__)


@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('user.html', users=users)


@bp.route('/users', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    country = request.form['country']
    balance = request.form['balance']

    new_user = User(name=name, email=email, age=age, country=country, balance=balance)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('user_routes.get_users'))
