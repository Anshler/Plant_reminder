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

def press_paypal_button(amount):
    try:
        master_url = 'http://localhost:8928/transaction'
        create_payment_url = master_url + '/payment'
        execute_payment_url = master_url + '/execute'

        # Create payment
        response = requests.post(create_payment_url, data={'amount': amount})
        if response.status_code == 200:
            print('create object successful')
            response_json = response.json()
            #payment_id = response_json.get('paymentID')
            redirect_url = response_json.get('redirect_url')
        else:
            print('Failed to create payment:', response.text)
            return

        # Open the redirect URL in a new browser window
        driver = webdriver.Chrome()  # Replace with the appropriate driver for your browser
        driver.get(redirect_url)

        # Wait for the payment completion URL
        wait = WebDriverWait(driver, 90)  # Replace with the actual completion URL
        element = wait.until(EC.url_contains(master_url))
        # Extract the URL
        try:
            completion_url = driver.current_url
            parsed_url = urlparse(completion_url)
            query_params = parse_qs(parsed_url.query)
            payer_id = query_params.get('PayerID', [''])[0]
            payment_id = query_params.get('paymentId', [''])[0]
        except Exception as e:
            print(e)
            return False

        # Send request to execute payment
        response = requests.post(execute_payment_url, data={'paymentID': payment_id, 'payerID': payer_id})
        print(response)
        if response.status_code == 200:
            success = response.json().get('success')
            if success:
                return True
            else:
                return False
        else:
            return False
    except: return False
# Call the function to initiate the PayPal payment
#press_paypal_button('4.00')


