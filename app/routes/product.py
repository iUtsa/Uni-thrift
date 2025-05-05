from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import uuid
from app import db
from app.models.product import Product, ProductImage, ProductCategory
from app.forms.product import ProductForm

product = Blueprint('product', __name__)

@product.route('/product/<int:id>')
def detail(id):
    product = Product.query.get_or_404(id)
    product.increment_views()
    
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_available == True
    ).order_by(Product.views.desc()).limit(4).all()
    
    return render_template('products/detail.html', 
                          title=product.title,
                          product=product,
                          related_products=related_products)

@product.route('/product/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProductForm()
    form.category.choices = [(c.id, c.name) for c in ProductCategory.query.all()]
    
    if form.validate_on_submit():
        product = Product(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            condition=form.condition.data,
            location=form.location.data,
            category_id=form.category.data,
            seller_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        
        # Handle uploaded images
        for image_file in form.images.data:
            if image_file:
                filename = secure_filename(f"{uuid.uuid4()}_{image_file.filename}")
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', filename))
                
                image = ProductImage(
                    file_name=filename,
                    is_primary=(form.images.data.index(image_file) == 0),  # First image is primary
                    product_id=product.id
                )
                db.session.add(image)
        
        db.session.commit()
        flash('Your product has been listed!', 'success')
        return redirect(url_for('product.detail', id=product.id))
    
    return render_template('products/create.html', 
                          title='List a Product',
                          form=form)

@product.route('/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = Product.query.get_or_404(id)
    
    if product.seller_id != current_user.id:
        flash('You do not have permission to edit this product.', 'danger')
        return redirect(url_for('product.detail', id=id))
    
    form = ProductForm()
    form.category.choices = [(c.id, c.name) for c in ProductCategory.query.all()]
    
    if form.validate_on_submit():
        product.title = form.title.data
        product.description = form.description.data
        product.price = form.price.data
        product.condition = form.condition.data
        product.location = form.location.data
        product.category_id = form.category.data
        
        # Handle uploaded images
        for image_file in form.images.data:
            if image_file:
                filename = secure_filename(f"{uuid.uuid4()}_{image_file.filename}")
                image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', filename))
                
                image = ProductImage(
                    file_name=filename,
                    is_primary=(not product.images),  # First image is primary if no images exist
                    product_id=product.id
                )
                db.session.add(image)
        
        db.session.commit()
        flash('Your product has been updated!', 'success')
        return redirect(url_for('product.detail', id=product.id))
    elif request.method == 'GET':
        form.title.data = product.title
        form.description.data = product.description
        form.price.data = product.price
        form.condition.data = product.condition
        form.location.data = product.location
        form.category.data = product.category_id
    
    return render_template('products/edit.html', 
                          title='Edit Product',
                          form=form,
                          product=product)

@product.route('/product/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    product = Product.query.get_or_404(id)
    
    if product.seller_id != current_user.id:
        flash('You do not have permission to delete this product.', 'danger')
        return redirect(url_for('product.detail', id=id))
    
    # Delete associated images from storage
    for image in product.images:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', image.file_name))
        except:
            pass
    
    db.session.delete(product)
    db.session.commit()
    flash('Your product has been deleted!', 'success')
    return redirect(url_for('main.index'))