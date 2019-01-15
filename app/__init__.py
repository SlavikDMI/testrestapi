from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Rest api"


@app.route('/v1/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    acc = list()
    for account in accounts:
        acc.append({'id' : account.id, 'username': account.username} )
    return jsonify(acc)


@app.route('/v1/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    pay = list()
    print(len(payments))
    for payment in payments:
        #pay.append({'payment_id' : payment.id, 'from': payment.user_from, 'amount': payment.amount, 'to': payment.user_to} )
        pay.append({'payment_id' : payment.id, 'amount': payment.amount, 'from': payment.user_from})
    return jsonify(pay)

@app.route('/v1/payments', methods=['POST'])
def make_payments():
    from_account = request.form['from_account']
    amount = request.form['amount']
    to_account = request.form['to_account']
    newPayment = Payment(user_from=from_account, user_to=to_account, amount=amount )
    db.session.add(newPayment)
    db.session.commit()
    return jsonify({'status': 'ok'})



class Account(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Account: ' + self.username + '(id: ' + self.id + ')'

class Payment(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_from = db.Column(db.String(100), db.ForeignKey('account.id'))
    user_to = db.Column(db.String(100), db.ForeignKey('account.id'))
    amount = db.Column(db.Float(10),  nullable=False)

    def __repr__(self):
        return '<Payment: id: %r>' % self.id





if __name__ == '__main__':
    app.run(debug=True)
