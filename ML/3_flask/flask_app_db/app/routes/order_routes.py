from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Order
from app import db

bp = Blueprint('order_routes', __name__)


@bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return render_template('order.html', orders=orders)


@bp.route('/orders', methods=['POST'])
def add_order():
    user_id = request.form['user_id']
    product_name = request.form['product_name']
    price = request.form['price']
    quantity = request.form['quantity']
    order_date = request.form['order_date']

    new_order = Order(user_id=user_id, product_name=product_name, price=price, quantity=quantity, order_date=order_date)
    db.session.add(new_order)
    db.session.commit()

    return redirect(url_for('order_routes.get_orders'))
