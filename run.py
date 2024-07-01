import os
import sys
from flask import Flask, request, jsonify, session, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user, login_required, UserMixin
from flask_mail import Mail
from datetime import datetime
import bcrypt
from flask_paginate import Pagination, get_page_args

# Ensure the grandparent directory is in sys.path
grandparent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, grandparent_dir)

from model.configuration.config import Config
from model.Customer import Customer

from model.employee import Employee
from model.payment import Payment
from model.Car import Car, User
from model.rental import Rental
from model.maintenance import Maintenance
from model.location import Location
from model import db
from model.insurance import Insurance
from forms import InsuranceForm, CarForm, CustomerForm, Update_password,LocationForm, EmployeeForm, RentalForm, PaymentForm, MaintenanceForm, RegistrationForm, LoginForm
from model.utils import login_required, send_login_notification

# Initialize the Flask application
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
app = Flask(__name__, template_folder=template_dir, static_folder='./static')
app.config['SECRET_KEY'] = 'auca@2023'
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()
    
    

@app.route('/register', methods=['GET', 'POST'])
# @login_required
def register():
    """
    This route is responsible for allowing users to sign up if they don't have an account.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        new_user = User(
            fullName=form.fullName.data,
            UserRole=form.UserRole.data,
            email=form.email.data,
            password=hashed_password.decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This route is responsible for allowing users to log in.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.user_id
            session.permanent = True  # Set session as permanent
            flash('Login successful!', 'success')
            send_login_notification(user.email)
            
            if user.UserRole.lower() == 'admin':
                return redirect(url_for('dashboards'))
            elif user.UserRole.lower() == 'user':
                return redirect(url_for('display_cars'))
            else:
                flash('User role is not recognized.', 'danger')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    if session.get('was_once_logged_in'):
        del session['was_once_logged_in']
    flash('You have successfully logged yourself out.', 'success')
    return redirect(url_for('login'))



@app.route('/')
@app.route('/dashboards')
@login_required
def dashboards():
    """_summary_
    this module will displaying Admin Dashboard
    Returns:
        will return the dashboard page if the request is success
    """
    return render_template('dashboard.html')


@app.route('/update_user/<string:email>', methods=['GET', 'POST'])
@login_required
def update_user(email):
    """
    update user 's email password 
    Parameters:
    email (str): The email of the user to be updated.
    Returns:
    render_template: when make Request this page will be appear
    Redirect: will be redirect to login if email password are updated
    """
    user = User.query.filter_by(email=email).first_or_404()
    form = Update_password(obj=user)

    if form.validate_on_submit():
        user.email = form.email.data
        user.password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        send_login_notification(user.email)
        
        db.session.commit()
        flash('Password Are updated successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('update_user.html', form=form, email=email)



@app.route('/error')
@login_required
def error():
    # Intentionally raise an exception to trigger the 500 error for demonstration
    raise Exception("Intentional error to demonstrate 500 error page")

# Error handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/add_insurance', methods=['GET', 'POST'])
@login_required
def add_insurance():
    """
    add_insurance function will adding the new insurance in our system
    Returns:
    will return the add_insurance page if the Request is success
    """
    form = InsuranceForm()
    if form.validate_on_submit():
        new_insurance = Insurance(
            coverage_type=form.coverage_type.data,
            Insurance_company=form.Insurance_company.data,
            premium_amount=form.premium_amount.data
        )
        db.session.add(new_insurance)
        db.session.commit()
        flash('Insurance added successfully!', 'success')
        return redirect(url_for('add_insurance'))
    return render_template('add_insurance.html', form=form)


@app.route('/update_insurance/<int:insurance_id>', methods=['GET', 'POST'])
@login_required
def update_insurance(insurance_id):
    
    insurance = Insurance.query.get_or_404(insurance_id)
    form = InsuranceForm(obj=insurance)

    if form.validate_on_submit():
        insurance.coverage_type = form.coverage_type.data
        insurance.Insurance_company = form.Insurance_company.data
        insurance.premium_amount = form.premium_amount.data

        db.session.commit()
        flash('Insurance updated successfully!', 'success')
        return redirect(url_for('display_insurances'))

    return render_template('update_insurance.html', form=form, insurance_id=insurance_id)

@app.route('/delete_insurance/<int:insurance_id>', methods=['POST'])
@login_required
def delete_insurance(insurance_id):
    insurance = Insurance.query.get_or_404(insurance_id)
    db.session.delete(insurance)
    db.session.commit()
    flash('Insurance deleted successfully!', 'success')
    return redirect(url_for('display_insurances'))

@app.route('/insurances')
@login_required
def display_insurances():
    insurances = Insurance.query.all()
    return render_template('insurance_table.html', insurances=insurances)


@app.route('/add_car', methods=['GET', 'POST'])
@login_required
def add_car():
    car_form = CarForm()
    
    if car_form.validate_on_submit():
        new_car = Car(
            car_ID=car_form.car_ID.data,
            make=car_form.make.data,
            model=car_form.model.data,
            years=car_form.years.data,
            color=car_form.color.data,
            image=car_form.image.data,
            mileage=car_form.mileage.data,
            rental_price_per_day=car_form.rental_price_per_day.data,
            insurance_id=car_form.insurance_id.data
        )
        db.session.add(new_car)
        db.session.commit()
        
        flash('Car added successfully!', 'success')
        return redirect(url_for('add_car'))
    
    return render_template('add_car.html', car_form=car_form)


@app.route('/cars', methods=['GET'])
@login_required
def search_cars():
    search_query = request.args.get('searchQuery', '')
    sort_option = request.args.get('sortOption', 'modelAZ')
    industry_option = request.args.get('industryOption', 'all')
    
    # Pagination
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 8  # Items per page
    offset = (page - 1) * per_page

    query = Car.query

    if search_query:
        query = query.filter(Car.make.like(f'%{search_query}%') | Car.model.like(f'%{search_query}%'))
    
    if industry_option != 'all':
        query = query.filter(Car.make == industry_option)
    
    if sort_option == 'modelAZ':
        query = query.order_by(Car.model.asc())
    elif sort_option == 'priceLowHigh':
        query = query.order_by(Car.rental_price_per_day.asc())
    elif sort_option == 'priceHighLow':
        query = query.order_by(Car.rental_price_per_day.desc())
    elif sort_option == 'yearOldNew':
        query = query.order_by(Car.years.asc())
    elif sort_option == 'yearNewOld':
        query = query.order_by(Car.years.desc())
    elif sort_option == 'mileageLowHigh':
        query = query.order_by(Car.mileage.asc())
    elif sort_option == 'mileageHighLow':
        query = query.order_by(Car.mileage.desc())

    total = query.count()
    cars = query.offset(offset).limit(per_page).all()
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    total_pages = (total + per_page - 1) // per_page  # Calculating total pages
    
    return render_template('car_table1.html', cars=cars, page=page, per_page=per_page, pagination=pagination, total_pages=total_pages, search_query=search_query, sort_option=sort_option, industry_option=industry_option)





@app.route('/update_car/<car_id>', methods=['GET', 'POST'])
@login_required
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    car_form = CarForm(obj=car)

    if request.method == 'POST' and car_form.validate_on_submit():
        car.car_ID = car_form.car_ID.data
        car.make = car_form.make.data
        car.model = car_form.model.data
        car.years = car_form.years.data
        car.color = car_form.color.data
        car.image = car_form.image.data
        car.mileage = car_form.mileage.data
        car.rental_price_per_day = car_form.rental_price_per_day.data
        car.insurance_id = car_form.insurance_id.data
        
        db.session.commit()
        
        flash('Car updated successfully!', 'success')
        return redirect(url_for('update_car', car_id=car_id))

    return render_template('update_car.html', car_form=car_form, car_id=car_id)


@app.route('/cars')
@login_required
def display_cars():
    page = request.args.get('page', 1, type=int)
    per_page = 8

    cars_paginated = Car.query.paginate(page=page, per_page=per_page, error_out=False)
    cars_to_display = cars_paginated.items
    total_pages = cars_paginated.pages

    return render_template('car_table1.html', cars=cars_to_display, page=page, total_pages=total_pages)



@app.route('/About')
@login_required
def About():
    return render_template('about-us.html')

@app.route('/contact')
@login_required
def Contacts():
    return render_template('contact.html')


@app.route('/delete_car/<car_id>', methods=['POST'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('Car record deleted successfully!', 'success')
    return redirect(url_for('display_cars'))



@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        # Combine country code and telephone number
        full_telephone_number = form.get_full_telephone_number()

        # Create a new Employee object
        new_employee = Employee(
            employee_ID=form.employee_ID.data,
            First_name=form.First_name.data,
            Last_name=form.Last_name.data,
            TelephoneNumber=full_telephone_number,
            position=form.position.data,
            location_id=form.location_id.data
        )

        # Add to database and commit
        db.session.add(new_employee)
        db.session.commit()

        flash('Employee added successfully!', 'success')
        return redirect(url_for('add_employee'))

    return render_template('add_employee.html', form=form)


@app.route('/update_employee/<employee_id>', methods=['GET', 'POST'])
@login_required
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm(obj=employee)

    if request.method == 'POST' and form.validate_on_submit():
        # Combine country code and telephone number
        full_telephone_number = form.get_full_telephone_number()

        employee.employee_ID = form.employee_ID.data
        employee.First_name = form.First_name.data
        employee.Last_name = form.Last_name.data
        employee.TelephoneNumber = full_telephone_number
        employee.position = form.position.data
        employee.location_id = form.location_id.data
        
        db.session.commit()

        flash('Employee updated successfully!', 'success')
        return redirect(url_for('display_employees'))

    return render_template('update_employee.html', form=form, employee_id=employee_id)

@app.route('/delete_employee/<employee_id>', methods=['POST'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee record deleted successfully!', 'success')
    return redirect(url_for('display_employees'))

@app.route('/employees')
@login_required
def display_employees():
    employees = Employee.query.all()  
    return render_template('employee_table.html', employees=employees)


@app.route('/car_all')
@login_required
def displays_car():
    cars = Car.query.all()
    print(cars)  # Print the retrieved data to the console
    return render_template('car_table.html', cars=cars)


@app.route('/add_rental', methods=['GET', 'POST'])
@login_required
def add_rental():
    form = RentalForm()
    employees = Employee.query.all()
    cars = Car.query.all()

    form.employee_ID.choices = [(emp.employee_ID, f"{emp.First_name} {emp.Last_name}") for emp in employees]

    total_rental_cost = 0

    if request.method == 'POST':
        if form.validate_on_submit():
            rental_start_date = form.rental_start_date.data
            return_date = form.return_date.data
            car_ID = form.car_ID.data

            rental_duration = (return_date - rental_start_date).days

            car = Car.query.filter_by(car_ID=car_ID).first()
            if not car:
                flash('Car not found!', 'danger')
                return redirect(url_for('add_rental'))

            employee = Employee.query.filter_by(employee_ID=form.employee_ID.data).first()
            if not employee:
                flash('Employee not found!', 'danger')
                return redirect(url_for('add_rental'))

            print(f"Employee Position: {employee.position}")

            if employee.position.upper() != 'MANAGER':
                flash('Only managers are authorized to give out cars!', 'danger')
                return redirect(url_for('add_rental'))

            total_rental_cost = rental_duration * car.rental_price_per_day

            new_rental = Rental(
                rental_start_date=rental_start_date,
                return_date=return_date,
                total_rental_cost=total_rental_cost,
                payment_status=form.payment_status.data,
                employee_ID=form.employee_ID.data,
                car_ID=form.car_ID.data,
                customer_id=form.customer_id.data
            )
            db.session.add(new_rental)
            db.session.commit()
            flash('Rental added successfully!', 'success')
            return redirect(url_for('add_payment'))
        else:
            flash('Form validation failed. Please check your inputs.', 'danger')

    return render_template('add_rental.html', form=form, total_rental_cost=total_rental_cost, employees=employees, cars=cars)
    # return render_template('add_payment.html', form=form, total_rental_cost=total_rental_cost, employees=employees, cars=cars)




@app.route('/rental_table')
@login_required
def rental_table():
    rentals = Rental.query.all()  # Fetch all rentals from database

    return render_template('rental_table.html', rentals=rentals)



@app.route('/update_rental/<int:rental_id>', methods=['GET', 'POST'])
@login_required
def update_rental(rental_id):
    rental = Rental.query.get_or_404(rental_id)
    form = RentalForm(obj=rental)
    employees = Employee.query.all()
    form.employee_ID.choices = [(e.employee_ID, f"{e.First_name} {e.Last_name} ({e.position})") for e in employees]

    if request.method == 'POST' and form.validate_on_submit():
        rental.rental_start_date = form.rental_start_date.data
        rental.return_date = form.return_date.data

        # Calculate rental duration in days
        rental_duration = (rental.return_date - rental.rental_start_date).days

        # Fetch car's rental price per day
        car = Car.query.filter_by(car_ID=form.car_ID.data).first()
        if not car:
            flash('Car not found!', 'danger')
            return redirect(url_for('update_rental', rental_id=rental_id))

        # Debugging info: Check rental dates and duration
        print(f"Rental Start Date: {rental.rental_start_date}")
        print(f"Return Date: {rental.return_date}")
        print(f"Rental Duration: {rental_duration} days")

        # Debugging info: Check car details
        print(f"Car ID: {form.car_ID.data}")
        print(f"Car Rental Price per Day: {car.rental_price_per_day}")

        # Calculate total rental cost
        rental.total_rental_cost = rental_duration * car.rental_price_per_day

        rental.payment_status = form.payment_status.data
        rental.employee_ID = form.employee_ID.data
        rental.customer_id = form.customer_id.data
        rental.car_ID = form.car_ID.data
        
        db.session.commit()
        flash('Rental updated successfully!', 'success')
        return redirect(url_for('update_rental', rental_id=rental.rental_ID))

    return render_template('rental_update.html', form=form, rental=rental)



@app.route('/get_rental_cost/<int:rental_id>', methods=['GET'])
@login_required
def get_rental_cost(rental_id):
    rental = Rental.query.filter_by(rental_ID=rental_id).first()
    if rental:
        return jsonify(success=True, total_rental_cost=rental.total_rental_cost)
    else:
        return jsonify(success=False, error="Rental not found"), 404



@app.route('/add_payment', methods=['GET', 'POST'])
@login_required
def add_payment():
    form = PaymentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            rental_id = form.rental_id.data
            rental = Rental.query.filter_by(rental_ID=rental_id).first()
            
            if not rental:
                flash('Rental not found!', 'danger')
                return redirect(url_for('add_payment'))
            
            payment_date = form.payment_date.data
            payment_method = form.payment_method.data
            amount_paid = rental.total_rental_cost  # Get the total rental cost
            
            # Check if card details should be included
            if payment_method in ['VISA', 'CREDIT', 'DEBIT']:
                card_number = form.card_number.data
                cvv = form.cvv.data
                expiry_date = form.expiry_date.data
            else:
                card_number = None
                cvv = None
                expiry_date = None
            
            new_payment = Payment(
                payment_date=payment_date,
                payment_method=payment_method,
                rental_id=rental_id,
                amount_paid=amount_paid,
                card_number=card_number,
                cvv=cvv,
                expiry_date=expiry_date
            )
            db.session.add(new_payment)
            
            # Update car status
            car = Car.query.filter_by(car_ID=rental.car_ID).first()
            if car:
                car.car_status = 'Borrowed'
            
            # Update rental payment status
            rental.payment_status = 'Success your payment Rent'
            
            db.session.commit()
            flash('Payment added successfully!', 'success')
            return redirect(url_for('add_payment'))
        else:
            flash('Form validation failed. Please check your inputs.', 'danger')
    return render_template('add_payment.html', form=form)



@app.route('/update_payment/<int:payment_id>', methods=['GET', 'POST'])
@login_required
def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    form = PaymentForm(obj=payment)

    if form.validate_on_submit():
        payment.payment_date = form.payment_date.data
        payment.payment_method = form.payment_method.data
        payment.rental_id = form.rental_id.data
        payment.amount_paid = form.amount_paid.data
        
        if payment.payment_method in ['VISA', 'CREDIT', 'DEBIT']:
            payment.card_number = form.card_number.data
            payment.cvv = form.cvv.data
            payment.expiry_date = form.expiry_date.data
        else:
            payment.card_number = None
            payment.cvv = None
            payment.expiry_date = None

        db.session.commit()
        flash('Payment updated successfully!', 'success')
        return redirect(url_for('display_payments'))

    return render_template('update_payment.html', form=form, payment_id=payment_id)

@app.route('/delete_payment/<int:payment_id>', methods=['POST'])
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    flash('Payment deleted successfully!', 'success')
    return redirect(url_for('display_payments'))


@app.route('/payments')
@login_required
def display_payments():
    payments = Payment.query.all()
    return render_template('payment_table.html', payments=payments)


@app.route('/delete_rental/<int:rental_id>', methods=['POST'])
def delete_rental(rental_id):
    # Fetch the rental record by ID
    rental = Rental.query.get(rental_id)
    
    if rental:
        try:
            # Delete the rental record
            db.session.delete(rental)
            db.session.commit()
            flash('Rental record deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting rental record: {e}', 'danger')
    else:
        flash('Rental record not found!', 'danger')

    return redirect(url_for('rental_table'))  # Adjust the redirection as per your application's flow


@app.route('/add_customer', methods=['GET', 'POST'])
@login_required
def add_customer():
    customer_form = CustomerForm()
    
    if customer_form.validate_on_submit():
        new_customer = Customer(
            customer_ID=customer_form.customer_ID.data,
            First_name=customer_form.First_name.data,
            Last_name=customer_form.Last_name.data,
            contact_information=customer_form.contact_information.data,
            Email=customer_form.Email.data,
            address=customer_form.address.data,
            driving_license_number=customer_form.driving_license_number.data
        )
        db.session.add(new_customer)
        db.session.commit()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('add_customer'))
    
    return render_template('add_customer.html', customer_form=customer_form)


@app.route('/update_customer/<customer_id>', methods=['GET', 'POST'])
@login_required
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_form = CustomerForm(obj=customer)

    if request.method == 'POST' and customer_form.validate_on_submit():
        customer.customer_ID = customer_form.customer_ID.data
        customer.First_name = customer_form.First_name.data
        customer.Last_name = customer_form.Last_name.data
        customer.contact_information = customer_form.contact_information.data
        customer.Email = customer_form.Email.data
        customer.address = customer_form.address.data
        customer.driving_license_number = customer_form.driving_license_number.data
        
        db.session.commit()

        flash('Customer updated successfully!', 'success')
        return redirect(url_for('display_customers'))

    return render_template('update_customer.html', customer_form=customer_form, customer_id=customer_id)

@app.route('/delete_customer/<customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer record deleted successfully!', 'success')
    return redirect(url_for('display_customers'))


@app.route('/customers')
@login_required
def display_customers():
    customers = Customer.query.all()  # Fetch all customer records from the database
    return render_template('customer_table.html', customers=customers)


@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    form = LocationForm()

    if form.validate_on_submit():
        existing_location = Location.query.filter_by(location_ID=form.location_ID.data).first()
        if existing_location:
            flash('Location ID already exists in the database. Please use a different ID.', 'danger')
        else:
            new_location = Location(
                location_ID=form.location_ID.data,
                address=form.address.data,
                contact_information=form.contact_information.data,
                operating_hours=form.operating_hours.data
            )
            db.session.add(new_location)
            db.session.commit()
            flash('Location added successfully!', 'success')
            return redirect(url_for('add_location'))

    return render_template('add_location.html', form=form)


@app.route('/update_location/<location_id>', methods=['GET', 'POST'])
@login_required
def update_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)

    if form.validate_on_submit():
        location.location_ID = form.location_ID.data
        location.address = form.address.data
        location.contact_information = form.contact_information.data
        location.operating_hours = form.operating_hours.data

        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('display_locations'))

    return render_template('update_location.html', form=form, location_id=location_id)


@app.route('/locations')
@login_required
def display_locations():
    locations = Location.query.all()
    return render_template('location_table.html', locations=locations)


@app.route('/delete_location/<location_id>', methods=['POST'])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash('Location deleted successfully!', 'success')
    return redirect(url_for('display_locations'))   


@app.route('/maintenance')
@login_required
def display_maintenance():
    maintenances = Maintenance.query.all()
    return render_template('maintenance_table.html', maintenances=maintenances)

# Add a new maintenance record
@app.route('/add_maintenance', methods=['GET', 'POST'])
@login_required
def add_maintenance():
    form = MaintenanceForm()
    if form.validate_on_submit():
        new_maintenance = Maintenance(
            maintenance_type=form.maintenance_type.data,
            maintenance_date=form.maintenance_date.data,
            car_ID=form.car_id.data,  # Ensure this matches the correct field in your form
            maintenance_cost=form.maintenance_cost.data,
            employee_id=form.employee_id.data  # Ensure this matches the correct field in your form
        )
        db.session.add(new_maintenance)
        db.session.commit()
        flash('Maintenance added successfully!', 'success')
        return redirect(url_for('display_maintenance'))
    return render_template('add_maintenance.html', form=form)


# Update an existing maintenance record
@app.route('/update_maintenance/<int:maintenance_id>', methods=['GET', 'POST'])
@login_required
def update_maintenance(maintenance_id):
    maintenance = Maintenance.query.get_or_404(maintenance_id)
    form = MaintenanceForm(obj=maintenance)

    if form.validate_on_submit():
        maintenance.maintenance_type = form.maintenance_type.data
        maintenance.maintenance_date = form.maintenance_date.data
        maintenance.car_ID = form.car_id.data
        maintenance.maintenance_cost = form.maintenance_cost.data
        maintenance.employee_id = form.employee_id.data

        db.session.commit()
        flash('Maintenance updated successfully!', 'success')
        return redirect(url_for('display_maintenance'))

    return render_template('update_maintenance.html', form=form, maintenance_id=maintenance_id)

# Delete a maintenance record
@app.route('/delete_maintenance/<int:maintenance_id>', methods=['POST'])
def delete_maintenance(maintenance_id):
    maintenance = Maintenance.query.get_or_404(maintenance_id)
    db.session.delete(maintenance)
    db.session.commit()
    flash('Maintenance deleted successfully!', 'success')
    return redirect(url_for('display_maintenance'))


if __name__ == '__main__':
    print("Template folder:", template_dir)
    app.run(debug=True)
