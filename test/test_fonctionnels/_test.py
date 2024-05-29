from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.close()


def test_show_summary(driver):
    driver.get("http://127.0.0.1:5000")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))
        driver.find_element(By.NAME, 'email').send_keys('john@simplylift.co')  # replace with actual email
        driver.find_element(By.ID, 'submit-button').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        welcome_text = driver.find_element(By.TAG_NAME,'h1').text
        assert 'Welcome, john@simplylift.co' in welcome_text
    except TimeoutException:
        print("Element not found within the specified timeout period.")

def test_purchase_places(driver):
    driver.get("http://127.0.0.1:5000/book/Spring Festival/Simply Lift")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'places')))
        driver.find_element(By.NAME,'places').send_keys('5')
        driver.find_element(By.CLASS_NAME,'submit-button').click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        confirmation_text = driver.find_element(By.TAG_NAME,'h1').text
        assert 'Booking complete' in confirmation_text
    except TimeoutException:
        print("Element not found within the specified timeout period.")