import webbrowser
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
def donate_us(source = 'momo'):
    if source == 'momo':
        webbrowser.open("https://me.momo.vn/3GIoiAigigT8iEukCpIy")
    elif source == 'paypal':
        webbrowser.open('https://paypal.me/plantreminder')

def press_paypal_button(username, energy, seed, subscription_status, amount):
    try:
        master_url = 'http://123.21.72.140:8948/transaction'
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
        options = webdriver.ChromeOptions()
        options.add_experimental_option('androidPackage', 'com.android.chrome')
        driver = webdriver.Chrome('./chromedriver', options=options)  # Replace with the appropriate driver for your browser
        driver.get(redirect_url)

        # Wait for the payment completion URL
        wait = WebDriverWait(driver, 90)  # Replace with the actual completion URL
        element = wait.until(EC.url_contains(master_url))

        # Send request to execute payment
        response = requests.post(execute_payment_url, data={'paymentID': payment_id,
                                                            'userID': username, 'energy': energy, 'seed': seed,
                                                            'subscription_status': subscription_status,'amount':amount})
        if response.status_code == 200:
            success = response.json().get('success')
            if success:
                return True
            else:
                return False
        else:
            return False
    except: return False

def get_payer_id(payment_id):
    payment_url = f"https://api.paypal.com/v1/payments/payment/{payment_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Replace with your PayPal access token
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
#press_paypal_button('4.00')


