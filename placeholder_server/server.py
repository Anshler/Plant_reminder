from flask import Flask, render_template, jsonify, request
import paypalrestsdk
from ENV import CLIENT_ID, CLIENT_SECRET
app = Flask(__name__)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox mode for development
  "client_id": CLIENT_ID,
  "client_secret": CLIENT_SECRET})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment', methods=['POST'])
def payment():
    amount = request.form.get('amount')
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://127.0.0.1:5000/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "testitem",
                    "sku": "12345",
                    "price": amount,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": amount,
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id, 'redirect_url': redirect_url})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])
    print(payment['payer']['payer_info']['payer_id'])
    if payment.execute({'payer_id' : payment['payer']['payer_info']['payer_id']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})

if __name__ == '__main__':
    app.run(debug=True)
