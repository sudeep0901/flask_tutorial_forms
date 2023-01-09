from flask import Flask, url_for, flash, redirect
from flask import Flask, render_template, request
from flask_bootstrap import *
import pymysql.cursors
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = "abc"

connection = pymysql.connect(host='localhost', user='admin', password='admin',
                             db='test', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def create_customer(fname, lname):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `customer` (`fname`, `lname`) VALUES (%s, %s)"
            cursor.execute(sql, (fname, lname))
            print('created customer id:', connection.insert_id())
        connection.commit()
        return connection.insert_id()
    finally:
        pass


def get_all_customers():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `customer`"
            cursor.execute(sql)
            result = cursor.fetchall()
        return result
    finally:
        pass


def get_customer(customer_id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `customer` WHERE `id` = %s"
            cursor.execute(sql, str(customer_id))
            result = cursor.fetchone()
        return result
    finally:
        pass


def delete_customer(customer_id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `customer` WHERE `id` = %s"
            cursor.execute(sql, str(customer_id))
            connection.commit()
        return 1
    finally:
        pass


def update_customer(customer_id, fname, lname):
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE `customer` SET `fname` = %s, `lname` = %s WHERE `id` = %s"
            cursor.execute(sql, (fname, lname, str(customer_id)))
            connection.commit()
        return 1
    finally:
        pass


@app.route('/')
def home():
    if len(request.args) >= 2:
        if request.args.get('fname') == "" or request.args.get('lname') == "":
            print('invalid data')
            flash('first name or last name cannot be empty')
            customers = get_all_customers()

            return render_template("customer.html", customers=customers)
        elif request.args.get('fname') != "" and request.args.get('lname') != "":
            name = request.args.get('fname') + " " + request.args.get('lname')
            create_customer(request.args.get('fname'),
                            request.args.get('lname'))
            flash('Customer created successfully!')
            customers = get_all_customers()
            return redirect(request.path, code=302)
            # return render_template("customer.html", customers=customers)

    # if request.method == 'GET':
    #     customer = get_customer()
    #     return render_template("index.html", name=customer.get('fname') + " " + customer.get('lname'))
    # if request.method == 'POST':
    #     create_customer(request.form['fname'], request.form['lname'])
    #     flash('Customer created successfully!')
    #     return render_template("index.html")
    customers = get_all_customers()
    return render_template("customer.html", customers=customers)


@app.route('/customer/<int:customer_id>')
def customer_details(customer_id):
    customer = get_customer(customer_id)
    return render_template("details.html", customer=customer)


@app.route('/customer/delete/<int:customer_id>')
def remove(customer_id):
    customer = delete_customer(customer_id)
    print(customer)
    if customer:
        flash('Customer deleted successfully!')
    else:
        flash('Customer not found!')
    return redirect(url_for('home', customer=customer))


@app.route('/customer/edit/<int:customer_id>', methods=['GET', 'POST'])
def update(customer_id):
    if request.method == 'POST':
        if request.form['fname'] == "" or request.form['lname'] == "":
            print('invalid data')
            flash('first name or last name cannot be empty')
            customer = get_customer(customer_id)
            return render_template("update.html", customer=customer)

        success = update_customer(
            customer_id, request.form['fname'], request.form['lname'])
        if success:
            flash('Customer updated successfully!')
        else:
            flash('Customer not found!')
        return redirect(url_for('home'))
    customer = get_customer(customer_id)
    return render_template("update.html", customer=customer)


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template("404.html", e=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
