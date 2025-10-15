from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Map known actions for certain requirements
def map_step_to_action(step):
    """
    Maps generic step text to actual Selenium actions if known.
    """
    actions = []
    if "upload image" in step.lower():
        actions.append("driver.find_element(By.ID, 'upload').send_keys('path/to/image.jpg')")
    elif "login" in step.lower():
        actions.append("driver.find_element(By.NAME, 'email').send_keys('test@example.com')")
        actions.append("driver.find_element(By.NAME, 'password').send_keys('password123')")
        actions.append("driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()")
        actions.append("assert 'Dashboard' in driver.title")
    else:
        actions.append(f"# Placeholder: {step}")
    return actions

def generate_selenium_script(test_cases, output_file="selenium_test_cases.py"):
    """
    Generates a Selenium Python script from structured test cases.
    """
    script_lines = [
        "from selenium import webdriver",
        "from selenium.webdriver.common.by import By",
        "import time",
        "",
        "options = webdriver.ChromeOptions()",
        "options.add_argument('--headless=new')",
        "driver = webdriver.Chrome(options=options)",
        "driver.maximize_window()",
        ""
    ]

    for i, test in enumerate(test_cases, 1):
        script_lines.append(f"# === Test Case {i}: {test['title']} ===")
        script_lines.append(f"print('Running test case: {test['title']}')")
        script_lines.append("driver.get('http://localhost:8000')  # Update to your app URL")
        script_lines.append("time.sleep(1)")

        # Convert each step to Selenium action if possible
        for step in test["steps"]:
            actions = map_step_to_action(step)
            for a in actions:
                script_lines.append(a)
            script_lines.append("time.sleep(1)")

        script_lines.append(f"print('✅ Test case completed: {test['title']}')\n")

    script_lines.append("driver.quit()")

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(script_lines))

    return output_file
