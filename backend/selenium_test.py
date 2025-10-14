from selenium import webdriver
from selenium.webdriver.common.by import By

def run_login_test(url, username, password):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        driver.find_element(By.NAME, "email").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()
        assert "Dashboard" in driver.title
        return True
    finally:
        driver.quit()
