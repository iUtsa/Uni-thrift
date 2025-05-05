from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
import uuid
from app import db
from app.models.product import Product
from app.models.order import Order, OrderItem

order = Blueprint('order', __name__)

@order.route('/cart', methods=['GET'])
@login_required
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    
    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product and product.is_available:
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
            total += item_total
    
    return render_template('orders/cart.html', 
                          title='Shopping Cart',
                          cart_items=cart_items,
                          total=total)

@order.route('/cart/add/<int:id>', methods=['POST'])
@login_required
def add_to_cart(id):
    product = Product.query.get_or_404(id)
    
    if not product.is_available:
        flash('This product is no longer available.', 'warning')
        return redirect(url_for('product.detail', id=id))
    
    if product.seller_id == current_user.id:
        flash('You cannot buy your own product.', 'warning')
        return redirect(url_for('product.detail', id=id))
    
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    product_id = str(id)
    
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity
    
    session['cart'] = cart
    flash(f'{product.title} added to your cart!', 'success')
    return redirect(url_for('order.view_cart'))

@order.route('/cart/update/<int:id>', methods=['POST'])
@login_required
def update_cart(id):
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' in session:
        cart = session['cart']
        product_id = str(id)
        
        if product_id in cart:
            if quantity > 0:
                cart[product_id] = quantity
            else:
                del cart[product_id]
            
            session['cart'] = cart
    
    return redirect(url_for('order.view_cart'))

@order.route('/cart/remove/<int:id>', methods=['POST'])
@login_required
def remove_from_cart(id):
    if 'cart' in session:
        cart = session['cart']
        product_id = str(id)
        
        if product_id in cart:
            del cart[product_id]
            session['cart'] = cart
    
    return redirect(url_for('order.view_cart'))

@order.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        cart = session.get('cart', {})
        
        if not cart:
            flash('Your cart is empty.', 'warning')
            return redirect(url_for('order.view_cart'))
        
        # Create new order
        order = Order(
            order_number=str(uuid.uuid4())[:8].upper(),
            status='Pending',
            buyer_id=current_user.id,
            total_amount=0  # Will be calculated below
        )
        db.session.add(order)
        
        # Add order items
        total_amount = 0
        for product_id, quantity in cart.items():
            product = Product.query.get(int(product_id))
            
            if product and product.is_available:
                item = OrderItem(
                    order=order,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price
                )
                db.session.add(item)
                
                # Update total amount
                total_amount += product.price * quantity
                
                # Mark product as unavailable
                product.is_available = False
        
        order.total_amount = total_amount
        db.session.commit()
        
        # Clear cart
        session.pop('cart', None)
        
        flash('Your order has been placed successfully!', 'success')
        return redirect(url_for('order.history'))
    
    return render_template('orders/checkout.html', title='Checkout')

@order.route('/orders', methods=['GET'])
@login_required
def history():
    orders = Order.query.filter_by(buyer_id=current_user.id).order_by(Order.created_date.desc()).all()
    return render_template('orders/history.html', title='Order History', orders=orders)

@order.route('/orders/<order_number>', methods=['GET'])
@login_required
def detail(order_number):
    order = Order.query.filter_by(order_number=order_number, buyer_id=current_user.id).first_or_404()
    return render_template('orders/detail.html', title=f'Order #{order_number}', order=order)