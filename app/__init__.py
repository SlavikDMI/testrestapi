from flask import Flask, jsonify, request
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
        acc.append({'id': account.id, 'username': account.username, 'balance': account.balance})
    return jsonify(acc)


@app.route('/v1/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    pay = list()
    print(len(payments))
    for payment in payments:
        pay.append({'payment_id': payment.id, 'amount': payment.amount, 'from': payment.user_from})
    return jsonify(pay)


@app.route('/v1/payments', methods=['POST'])
def make_payments():
    from_account = request.form['from_account']
    password = request.form['password']
    amount = float(request.form['amount'])
    to_account = request.form['to_account']
    account = Account.query.filter_by(id=from_account).first()
    recipient = Account.query.filter_by(id=to_account).first()
    if account is not None and password == account.password and recipient is not None:
        if (float(account.balance) - amount) >= 0:
            newPayment = Payment(user_from=from_account, user_to=to_account, amount=amount)
            account.balance -= amount
            recipient.balance += amount
            db.session.add(newPayment)
            db.session.commit()
            return jsonify({'status': 'ok'})
        else:
            return jsonify({'error': 'Insufficient funds'})
    else:
        return "{'error': 'wrong username/password or wrong recipient'}"


class Account(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    balance = db.Column(db.Float(2),  nullable=False)

    def __repr__(self):
        return '<Account: ' + self.username + '(id: ' + self.id + ') balance: ' + self.balance


class Payment(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_from = db.Column(db.String(100), db.ForeignKey('account.id'))
    user_to = db.Column(db.String(100), db.ForeignKey('account.id'))
    amount = db.Column(db.Float(2),  nullable=False)

    def __repr__(self):
        return '<Payment: id: %r>' % self.id


if __name__ == '__main__':
    app.run(debug=True)
