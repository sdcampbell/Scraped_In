import sys
import re
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import argparse

parser = argparse.ArgumentParser(description='Return a list of formatted usernames from a LinkedIn Search')
parser.add_argument("username", help="Enter your username")
parser.add_argument("password", help="Enter your password")
parser.add_argument("company_number", help="Company number. You can find this in the URL when looking at a company's employees.")
parser.add_argument("name_format", help="Username format: flast or first.last")
parser.add_argument("-d", "--domain",
                    help="Optional domain name to append to username and output email addresses.")
args = parser.parse_args()

def format_username(name):
    first_name = name.split()[0].lower()
    last_name = name.split()[1].lower()
    if args.name_format == "flast":
        if args.domain:
            return first_name[:1] + last_name + '@' + args.domain
        else:
            return first_name[:1] + last_name
    elif args.name_format == "first.last":
        if args.domain:
            return first_name + "." + last_name + '@' + args.domain
        else:
            return first_name + "." + last_name

def main():
    RESULTS_LOCATOR = "//*[contains(@class, 'name actor-name')]"
    results = set()
    names = set()
    counter = 1
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    login_url = "https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin"
    company_url = "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22{0}%22%5D&page=".format(args.company_number)
    driver.get(login_url)
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(args.username)
    password.send_keys(args.password)
    #driver.find_element_by_id("#app__container > main > div > form > div.login__form_action_container > button").click()
    driver.find_element(By.XPATH,"//button[contains(.,'Sign in')]").click()
    driver.get(company_url + str(counter))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        while driver.find_element(By.XPATH, "//button[contains(.,'Next')]"):
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))

            page_results = driver.find_elements(By.XPATH, RESULTS_LOCATOR)

            for item in page_results:
                results.add(item.text)

            sleep(randint(4,8))
            counter += 1
            driver.get(company_url + str(counter))
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except:
        pass

    for line in results:
        name_title = line.split()
        full_name = name_title[0] + " " + name_title[1].rstrip(",")
        names.add(full_name)

    for name in names:
        print(format_username(name))

    driver.quit()

if __name__ == "__main__":
    main()
