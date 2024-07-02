from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_paginate import Pagination, get_page_args

from app.decorator.decorator import login_required
from app.forms import CarForm
from app.models import Car, db


car_bp = Blueprint("car", __name__)


@car_bp.route("/add_car", methods=["GET", "POST"])
@login_required
def add_car():
    car_form = CarForm()

    if car_form.validate_on_submit():
        new_car = Car(
            car_id=car_form.car_id.data,
            make=car_form.make.data,
            model=car_form.model.data,
            years=car_form.years.data,
            color=car_form.color.data,
            image=car_form.image.data,
            mileage=car_form.mileage.data,
            rental_price_per_day=car_form.rental_price_per_day.data,
            insurance_id=car_form.insurance_id.data,
        )
        db.session.add(new_car)
        db.session.commit()

        flash("Car added successfully!", "success")
        return redirect(url_for("car.add_car"))

    return render_template("add_car.html", car_form=car_form)


@car_bp.route("/cars", methods=["GET"])
@login_required
def search_cars():
    search_query = request.args.get("searchQuery", "")
    sort_option = request.args.get("sortOption", "modelAZ")
    industry_option = request.args.get("industryOption", "all")

    # Pagination
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page"
    )
    per_page = 8  # Items per page
    offset = (page - 1) * per_page

    query = Car.query

    if search_query:
        query = query.filter(
            Car.make.like(f"%{search_query}%") | Car.model.like(f"%{search_query}%")
        )

    if industry_option != "all":
        query = query.filter(Car.make == industry_option)

    if sort_option == "modelAZ":
        query = query.order_by(Car.model.asc())
    elif sort_option == "priceLowHigh":
        query = query.order_by(Car.rental_price_per_day.asc())
    elif sort_option == "priceHighLow":
        query = query.order_by(Car.rental_price_per_day.desc())
    elif sort_option == "yearOldNew":
        query = query.order_by(Car.years.asc())
    elif sort_option == "yearNewOld":
        query = query.order_by(Car.years.desc())
    elif sort_option == "mileageLowHigh":
        query = query.order_by(Car.mileage.asc())
    elif sort_option == "mileageHighLow":
        query = query.order_by(Car.mileage.desc())

    total = query.count()
    cars = query.offset(offset).limit(per_page).all()
    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework="bootstrap4"
    )

    total_pages = (total + per_page - 1) // per_page  # Calculating total pages

    return render_template(
        "car_table1.html",
        cars=cars,
        page=page,
        per_page=per_page,
        pagination=pagination,
        total_pages=total_pages,
        search_query=search_query,
        sort_option=sort_option,
        industry_option=industry_option,
    )


@car_bp.route("/update_car/<car_id>", methods=["GET", "POST"])
@login_required
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    car_form = CarForm(obj=car)

    if request.method == "POST" and car_form.validate_on_submit():
        car.car_id = car_form.car_id.data
        car.make = car_form.make.data
        car.model = car_form.model.data
        car.years = car_form.years.data
        car.color = car_form.color.data
        car.image = car_form.image.data
        car.mileage = car_form.mileage.data
        car.rental_price_per_day = car_form.rental_price_per_day.data
        car.insurance_id = car_form.insurance_id.data

        db.session.commit()

        flash("Car updated successfully!", "success")
        return redirect(url_for("car.update_car", car_id=car_id))

    return render_template("update_car.html", car_form=car_form, car_id=car_id)


@car_bp.route("/cars")
@login_required
def display_cars():
    page = request.args.get("page", 1, type=int)
    per_page = 8

    cars_paginated = Car.query.paginate(page=page, per_page=per_page, error_out=False)
    cars_to_display = cars_paginated.items
    total_pages = cars_paginated.pages

    return render_template(
        "car_table1.html", cars=cars_to_display, page=page, total_pages=total_pages
    )


@car_bp.route("/delete_car/<car_id>", methods=["POST"])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash("Car record deleted successfully!", "success")
    return redirect(url_for("car.display_cars"))


@car_bp.route("/car_all")
@login_required
def displays_car():
    cars = Car.query.all()
    print(cars)  # Print the retrieved data to the console
    return render_template("car_table.html", cars=cars)
