from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from datetime import datetime
from wtforms.validators import DataRequired, Email
from wtforms import StringField, SelectField, PasswordField,IntegerField, SubmitField,StringField, DateField,HiddenField
from wtforms.validators import DataRequired, Regexp,Email, EqualTo,NumberRange,Length, ValidationError,InputRequired
from model.location import Location
from model.employee import Employee
from model.rental import Rental
from flask_wtf import FlaskForm
from model.Car import Car
from flask_mail import Mail, Message
from functools import wraps
from datetime import datetime
import datetime

class InsuranceForm(FlaskForm):
    coverage_type = SelectField('Coverage Type', choices=[('Medical_insurance', 'Medical_insurance'), ('Accident', 'Accident')], validators=[DataRequired()])
    Insurance_company = SelectField('Insurance Company', choices=[('sanlam', 'sanlam'), ('RADIANT', 'RADIANT')], validators=[DataRequired()])
    premium_amount = IntegerField('Premium Amount', validators=[DataRequired(), NumberRange(min=0)])


class RegistrationForm(FlaskForm):
    fullName = StringField('Full Name', validators=[DataRequired(), Length(max=40)])
    UserRole = SelectField('User Role', choices=[('admin', 'Admin'), ('user', 'User')])
    # UserRole = StringField('User Role', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')


# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# class UpdatePasswordForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password', 
#                                      validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
#     submit = SubmitField('Update')

class Update_password(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    Confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Update')

class CarForm(FlaskForm):
    car_ID = StringField('Car ID', validators=[DataRequired()])
    make = SelectField('Make', choices=[
        ('TOYOTA', 'Toyota'), 
        ('HONDA', 'Honda'),
        ('MERCEDES', 'Mercedes'), 
        ('VOLKSWAGEN', 'Volkswagen'),
        ('BMW', 'BMW'), 
        ('FORD', 'Ford')
    ], validators=[DataRequired()])
    model = SelectField('Model', choices=[('SEDAN', 'Sedan'), ('SUV', 'SUV'), ('TRUCK', 'Truck')], validators=[DataRequired()])
    years = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1886)]) 
    color = StringField('Color', validators=[DataRequired()])
    image = StringField('Image URL', validators=[DataRequired()])
    mileage = IntegerField('Mileage', validators=[DataRequired(), NumberRange(min=0)])
    rental_price_per_day = IntegerField('Rental Price per Day', validators=[DataRequired(), NumberRange(min=0)])
    insurance_id = IntegerField('Insurance ID', validators=[DataRequired(), NumberRange(min=1)])

    def validate_image(form, field):
        if Car.query.filter_by(image=field.data).first():
            raise ValidationError('Image URL already exists.')

# class CarForm(FlaskForm):
#     car_ID = StringField('Car ID', validators=[DataRequired()])
#     make = SelectField('Make', choices=[('TOYOTA', 'Toyota'), ('HONDA', 'Honda'),('MERCEDES', 'mercedes'), ('VOLKSWAGEN', 'Volkswagen'),('BMW', 'bmw'), ('FORD', 'Ford')], validators=[DataRequired()])
#     model = SelectField('Model', choices=[('SEDAN', 'Sedan'), ('SUV', 'SUV'), ('TRUCK', 'Truck')], validators=[DataRequired()])
#     years = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1886)])  # 1886 is the year of the first car
#     color = StringField('Color', validators=[DataRequired()])
#     image = StringField('Image URL', validators=[DataRequired()])
#     mileage = IntegerField('Mileage', validators=[DataRequired(), NumberRange(min=0)])
#     rental_price_per_day = IntegerField('Rental Price per Day', validators=[DataRequired(), NumberRange(min=0)])
#     insurance_id = IntegerField('Insurance ID', validators=[DataRequired(), NumberRange(min=1)])

class CustomerForm(FlaskForm):
    customer_ID = StringField('Customer ID', validators=[DataRequired()])
    First_name = StringField('First Name', validators=[DataRequired()])
    Last_name = StringField('Last Name', validators=[DataRequired()])
    contact_information = StringField('Contact Information', validators=[DataRequired()])
    Email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    driving_license_number = StringField('Driving License Number', validators=[DataRequired()])  

class LocationForm(FlaskForm):
    location_ID = StringField('Location ID', validators=[DataRequired(), Length(max=10)])
    address = StringField('Address', validators=[DataRequired(), Length(max=50)])
    contact_information = StringField('Contact Information', validators=[DataRequired(), Length(max=20)])
    operating_hours = StringField('Operating Hours', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Add Location')

    def validate_location_ID(self, location_ID):
        location = Location.query.filter_by(location_ID=location_ID.data).first()
        if location:
            raise ValidationError('Location ID already exists.')

    def validate_contact_information(self, contact_information):
        location = Location.query.filter_by(contact_information=contact_information.data).first()
        if location:
            raise ValidationError('Contact information already exists.')
  
class EmployeeForm(FlaskForm):
    employee_ID = StringField('Employee ID', validators=[InputRequired(), Length(max=10)])
    First_name = StringField('First Name', validators=[InputRequired(), Length(max=250)])
    Last_name = StringField('Last Name', validators=[InputRequired(), Length(max=200)])
    country_code = SelectField('Country Code', choices=[
        ('+1', '+1 (USA)'),
        ('+33', '+33 (France)'),
        ('+49', '+49 (Germany)'),
        ('+39', '+39 (Italy)'),
        ('+250', '+250 (RW)'),
        ('+44', '+44 (UK)')
    ], validators=[InputRequired()])
    TelephoneNumber = StringField('Telephone Number', validators=[InputRequired(), Length(max=20)])
    position = SelectField('Position', choices=[
        ('MANAGER', 'Manager'),
        ('STAFF', 'Staff')
    ], validators=[InputRequired()])
    location_id = StringField('Location ID', validators=[InputRequired(), Length(max=10)])

    def validate_employee_ID(self, field):
        if Employee.query.filter_by(employee_ID=field.data).first():
            raise ValidationError('Employee ID already exists. Please use a different ID.')

    def get_full_telephone_number(self):
        return f"{self.country_code.data}{self.TelephoneNumber.data}"

# class RentalForm(FlaskForm):
#     rental_start_date = DateField('Rental Start Date', format='%Y-%m-%d', validators=[DataRequired()])
#     return_date = DateField('Return Date', format='%Y-%m-%d', validators=[DataRequired()])
#     total_rental_cost = IntegerField('Total Rental Cost', validators=[DataRequired(), NumberRange(min=0)])
#     payment_status = StringField('Payment Status', validators=[DataRequired(), Length(max=255)])
#     employee_ID = StringField('Employee ID', validators=[DataRequired(), Length(max=10)])
#     car_ID = StringField('Car ID', validators=[DataRequired(), Length(max=10)])
#     customer_id = StringField('Customer ID', validators=[DataRequired(), Length(max=10)])


# class RentalForm(FlaskForm):
#     rental_start_date = DateField('Rental Start Date', format='%Y-%m-%d', validators=[DataRequired()])
#     return_date = DateField('Return Date', format='%Y-%m-%d', validators=[DataRequired()])
#     total_rental_cost = IntegerField('Total Rental Cost', validators=[NumberRange(min=0)])
#     payment_status = StringField('Payment Status', validators=[DataRequired(), Length(max=255)])
#     employee_ID = StringField('Employee ID', validators=[DataRequired(), Length(max=10)])
#     car_ID = StringField('Car ID', validators=[DataRequired(), Length(max=10)])
#     customer_id = StringField('Customer ID', validators=[DataRequired(), Length(max=10)])



# class RentalForm(FlaskForm):
#     rental_start_date = DateField('Rental Start Date', format='%Y-%m-%d', validators=[DataRequired()])
#     return_date = DateField('Return Date', format='%Y-%m-%d', validators=[DataRequired()])
#     total_rental_cost = IntegerField('Total Rental Cost', validators=[NumberRange(min=0)])
#     payment_status = StringField('Payment Status', validators=[DataRequired(), Length(max=255)])
#     employee_ID = StringField('Employee ID', validators=[DataRequired(), Length(max=10)])
#     car_ID = StringField('Car ID', validators=[DataRequired(), Length(max=10)])
#     customer_id = StringField('Customer ID', validators=[DataRequired(), Length(max=10)])

#     def validate_rental_start_date(form, field):
#         if field.data < datetime.today().date():
#             raise ValidationError('Rental start date cannot be in the past.')

#     def validate_return_date(form, field):
#         if field.data < form.rental_start_date.data:
#             raise ValidationError('Return date cannot be before the rental start date.')

#     def validate_car_ID(form, field):
#         existing_rental = Rental.query.filter(
#             Rental.car_ID == field.data,
#             Rental.rental_start_date <= form.return_date.data,
#             Rental.return_date >= form.rental_start_date.data
#         ).first()
#         if existing_rental:
#             raise ValidationError('This car is already rented for the selected dates.')   





class RentalForm(FlaskForm):
    rental_ID = HiddenField('ID')
    rental_start_date = DateField('Rental Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    return_date = DateField('Return Date', format='%Y-%m-%d', validators=[DataRequired()])
    total_rental_cost = IntegerField('Total Rental Cost', validators=[NumberRange(min=0)])
    payment_status = StringField('Payment Status', validators=[DataRequired(), Length(max=255)])
    employee_ID = SelectField('Employee ID', validators=[DataRequired()])
    car_ID = StringField('Car ID', validators=[DataRequired(), Length(max=10)])
    customer_id = StringField('Customer ID', validators=[DataRequired(), Length(max=10)])

    def validate_rental_start_date(self, field):
        if field.data < datetime.today().date():
            raise ValidationError('Rental start date cannot be in the past.')

    def validate_return_date(self, field):
        if field.data < self.rental_start_date.data:
            raise ValidationError('Return date cannot be before the rental start date.')

    def validate_car_ID(self, field):
        existing_rental = Rental.query.filter(
            Rental.car_ID == field.data,
            Rental.rental_start_date <= self.return_date.data,
            Rental.return_date >= self.rental_start_date.data
        ).first()
        if existing_rental and existing_rental.rental_ID != self.rental_ID.data:
            raise ValidationError('This car is already rented for the selected dates.')



# class RentalForm(FlaskForm):
#     rental_ID = HiddenField('ID')
#     rental_start_date = DateField('Rental Start Date', format='%Y-%m-%d', validators=[DataRequired()])
#     return_date = DateField('Return Date', format='%Y-%m-%d', validators=[DataRequired()])
#     total_rental_cost = IntegerField('Total Rental Cost', validators=[NumberRange(min=0)])
#     payment_status = StringField('Payment Status', validators=[DataRequired(), Length(max=255)])
#     employee_ID = SelectField('Employee ID', validators=[DataRequired()])
#     car_ID = StringField('Car ID', validators=[DataRequired(), Length(max=10)])
#     customer_id = StringField('Customer ID', validators=[DataRequired(), Length(max=10)])

#     def validate_rental_start_date(self, field):
#         if field.data < datetime.today().date():
#             raise ValidationError('Rental start date cannot be in the past.')

#     def validate_return_date(self, field):
#         if field.data < self.rental_start_date.data:
#             raise ValidationError('Return date cannot be before the rental start date.')

#     def validate_car_ID(self, field):
#         existing_rental = Rental.query.filter(
#             Rental.car_ID == field.data,
#             Rental.rental_start_date <= self.return_date.data,
#             Rental.return_date >= self.rental_start_date.data
#         ).first()
#         if existing_rental and existing_rental.rental_ID != self.rental_ID.data:
#             raise ValidationError('This car is already rented for the selected dates.')
        
        
#     # Your form fields here

#     def validate_rental_start_date(form, field):
#         if field.data < datetime.today().date():
#             raise ValidationError("Rental start date cannot be in the past.")
        
class PaymentForm(FlaskForm):
    payment_date = DateField('Payment Date', format='%Y-%m-%d', validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[('CASH', 'Cash'), ('CREDIT', 'Credit'), ('DEBIT', 'Debit'), ('VISA', 'Visa')], validators=[DataRequired()])
    rental_id = IntegerField('Rental ID', validators=[DataRequired(), NumberRange(min=1)])
    amount_paid = IntegerField('Amount Paid', validators=[DataRequired(), NumberRange(min=0)], render_kw={'readonly': True})
    card_number = StringField('Card Number', validators=[Length(min=16, max=16, message="Card number must be 16 digits"), Regexp('^[0-9]*$', message="Card number must be numeric")])
    cvv = StringField('CVV', validators=[Length(min=3, max=4, message="CVV must be 3 or 4 digits"), Regexp('^[0-9]*$', message="CVV must be numeric")])
    expiry_date = DateField('Expiry Date', format='%Y-%m-%d', validators=[DataRequired()])

    def validate_expiry_date(form, field):
        if field.data < datetime.now().date():
            raise ValidationError('Expiry date must be in the future')

    def validate_payment_date(self, field):
        if field.data < datetime.now().date():
            raise ValidationError('You can not make Payment the past')
        
    # def validate_rental_id(self, rental_id):
    #     Rental1 = Rental.query.filter_by(rental_ID = rental_id.data).first()
    #     if Rental1:
    #         raise ValidationError('you can not make payment twice ! you have been already paid you rent')




class MaintenanceForm(FlaskForm):
    maintenance_type = StringField('Maintenance Type', validators=[DataRequired(), Length(max=200)])
    maintenance_date = DateField('Maintenance Date', format='%Y-%m-%d', validators=[DataRequired()])
    car_id = SelectField('Car', coerce=str, validators=[DataRequired()])
    maintenance_cost = IntegerField('Maintenance Cost', validators=[DataRequired(), NumberRange(min=0)])
    employee_id = SelectField('Employee', coerce=str, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(MaintenanceForm, self).__init__(*args, **kwargs)
        self.car_id.choices = [(car.car_ID, car.car_ID) for car in Car.query.all()]
        self.employee_id.choices = [(employee.employee_ID, employee.employee_ID) for employee in Employee.query.all()]



# class PaymentForm(FlaskForm):
#     payment_date = DateField('Payment Date', format='%Y-%m-%d', validators=[DataRequired()])
#     payment_method = SelectField('Payment Method', choices=[('CASH', 'Cash'), ('CREDIT', 'Credit'), ('DEBIT', 'Debit'), ('VISA', 'Visa')], validators=[DataRequired()])
#     rental_id = IntegerField('Rental ID', validators=[DataRequired(), NumberRange(min=1)])
#     amount_paid = IntegerField('Amount Paid', validators=[DataRequired(), NumberRange(min=0)], render_kw={'readonly': True})
#     card_number = StringField('Card Number', validators=[Length(min=16, max=16, message="Card number must be 16 digits"), Regexp('^[0-9]*$', message="Card number must be numeric")])
#     cvv = StringField('CVV', validators=[Length(min=3, max=4, message="CVV must be 3 or 4 digits"), Regexp('^[0-9]*$', message="CVV must be numeric")])
#     expiry_date = DateField('Expiry Date', format='%Y-%m-%d', validators=[DataRequired()])

#     def validate_expiry_date(form, field):
#         if field.data < datetime.now().date():
#             raise ValidationError('Expiry date must be in the future')