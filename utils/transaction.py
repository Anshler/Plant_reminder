import webbrowser
import requests
import time
def donate_us(source = 'momo'):
    if source == 'momo':
        webbrowser.open("https://me.momo.vn/YOUR_MOMO_WALLET")
    elif source == 'paypal':
        webbrowser.open('https://paypal.me/YOUR_PAYPAL_WALLET')

def press_paypal_button(username, energy, seed, subscription_status, amount):
    try:
        master_url = 'http://localhost:8948/transaction'
        create_payment_url = master_url + '/payment'
        execute_payment_url = master_url + '/execute'

        # Create payment
        response = requests.post(create_payment_url, data={'amount': amount})
        if response.status_code == 200:
            print('create object successful')
            response_json = response.json()
            payment_id = response_json.get('paymentID')
            redirect_url = response_json.get('redirect_url')
        else:
            print('Failed to create payment:', response.text)
            return

        # Open the redirect URL in a new browser window
        webbrowser.open_new(redirect_url)
        # Time interval to check the current URL (in seconds)
        check_interval = 5
        # Time limit to wait for the desired URL to appear (in seconds)
        timeout = 60
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Send request to execute payment
            response = requests.post(execute_payment_url, data={'paymentID': payment_id,
                                                                'userID': username, 'energy': energy, 'seed': seed,
                                                                'subscription_status': subscription_status,
                                                                'amount': amount})
            if response.status_code == 200:
                success = response.json().get('success')
                if success:
                    return True
                else:
                    return False
            time.sleep(check_interval)
        return False
    except: return False

def get_payer_id(payment_id):
    payment_url = f"https://api.paypal.com/v1/payments/payment/{payment_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'YOUR_ACCESS_TOKEN'  # Replace with your PayPal access token
    }

    try:
        response = requests.get(payment_url, headers=headers)
        if response.status_code == 200:
            payment_data = response.json()
            payer_id = payment_data['payer']['payer_info']['payer_id']
            return payer_id
        else:
            return None
    except Exception as e:
        print(e)
        return None
# Call the function to initiate the PayPal payment
#press_paypal_button('yoyo',5,5,'','4.00')

