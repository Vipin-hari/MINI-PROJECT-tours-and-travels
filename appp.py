from flask import Flask, render_template, request
import ibm_db
import os
import random
import string

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=nhf72040;PWD=ASeXRRXEnG1CpGfD" , ",",",")
print(conn)
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    # Prepare the SQL statement with parameter markers
    sql = "INSERT INTO details (name, email, phone) VALUES (?, ?, ?)"

    # Execute the SQL statement with the form data
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, name)
    ibm_db.bind_param(stmt, 2, email)
    ibm_db.bind_param(stmt, 3, phone)
    ibm_db.execute(stmt)

    # Commit the transaction
    ibm_db.commit(conn)

    return render_template('places.html', name=name, email=email, phone=phone)


@app.route('/tour1')
def tour1():
    return render_template('tour1.html')



@app.route('/tour2')
def tour2():
    return render_template('tour2.html')


@app.route('/tour3')
def tour3():
    return render_template('tour3.html')

@app.route('/payment')
def payment():
    return render_template("payment.html")


@app.route('/invoice', methods=['POST'])
def invoice():
    card_number = request.form.get('card-number')
    card_name = request.form.get('card-name')
    expiry_date = request.form.get('expiry-date')
    cvv = request.form.get('cvv')
    invoice_number = generateInvoiceNumber()

    # Prepare the SQL statement with parameter markers
    sql = "INSERT INTO payment (card_number, card_name, expiry_date, cvv, invoice_number) VALUES (?, ?, ?, ?, ?)"

    # Execute the SQL statement with the form data
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, card_number)
    ibm_db.bind_param(stmt, 2, card_name)
    ibm_db.bind_param(stmt, 3, expiry_date)
    ibm_db.bind_param(stmt, 4, cvv)
    ibm_db.bind_param(stmt, 5, invoice_number)
    ibm_db.execute(stmt)

    # Commit the transaction
    ibm_db.commit(conn)

    return render_template('invoice.html', card_number=card_number, card_name=card_name, expiry_date=expiry_date, cvv=cvv, invoice_number=invoice_number)
    
def generateInvoiceNumber():
    characters = string.ascii_uppercase + string.digits
    invoice_number = ''.join(random.choice(characters) for _ in range(8))
    return invoice_number

if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')
  

