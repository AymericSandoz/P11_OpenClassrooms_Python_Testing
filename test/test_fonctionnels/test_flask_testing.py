from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from server import app  # import your Flask app

class TestBase(LiveServerTestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 0
        return app

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

class TestShowSummary(TestBase):
    def test_show_summary(self):
        self.driver.get(self.get_server_url())
        self.driver.find_element(By.NAME, 'email').send_keys('john@simplylift.co')
        self.driver.find_element(By.TAG_NAME, 'submit').click()
        welcome_text = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Welcome, john@simplylift.co', welcome_text)

class TestPurchasePlaces(TestBase):
    def test_purchase_places(self):
        self.driver.get(self.get_server_url() + "/purchasePlaces")
        self.driver.find_element(By.NAME, 'places').send_keys('5')
        self.driver.find_element(By.TAG_NAME, 'submit').click()
        confirmation_text = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Booking complete', confirmation_text)