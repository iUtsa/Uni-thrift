from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, TextAreaField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=120)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    price = DecimalField('Price ($)', validators=[DataRequired(), NumberRange(min=0.01)])
    condition = SelectField('Condition', choices=[
        ('New', 'New'),
        ('Like New', 'Like New'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor')
    ])
    location = StringField('Location', validators=[DataRequired(), Length(max=120)])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    images = MultipleFileField('Product Images', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('List Product')