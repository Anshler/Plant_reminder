import webbrowser
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def donate_us(source = 'momo'):
    if source == 'momo':
        webbrowser.open("https://me.momo.vn/3GIoiAigigT8iEukCpIy")
    elif source == 'paypal':
        webbrowser.open('https://paypal.me/plantreminder')
def press_paypal_button(amount):
    create_payment_url = 'http://127.0.0.1:5000/payment'
    execute_payment_url = 'http://127.0.0.1:5000/execute'

    # Create payment
    response = requests.post(create_payment_url, data={'amount': amount})
    if response.status_code == 200:
        response_json = response.json()
        payment_id = response_json.get('paymentID')
        redirect_url = response_json.get('redirect_url')
    else:
        print('Failed to create payment:', response.text)
        return

    # Open the redirect URL in a new browser window
    driver = webdriver.Chrome()  # Replace with the appropriate driver for your browser
    driver.get(redirect_url)

    # Wait for the payment completion URL
    wait = WebDriverWait(driver, 90)
    completion_url = "http://127.0.0.1:5000"  # Replace with the actual completion URL
    element = wait.until(EC.url_contains(completion_url))
    wait = WebDriverWait(driver, 2)

    # Send POST request to execute payment
    response = requests.post(execute_payment_url, data={'paymentID': payment_id})
    if response.status_code == 200:
        success = response.json().get('success')
        if success:
            print('Payment executed successfully!')
        else:
            print('Payment execution failed.')
    else:
        print('Failed to execute payment')

# Call the function to initiate the PayPal payment
press_paypal_button('4.00')


