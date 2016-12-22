from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from django.core.management.base import BaseCommand

# firefox_capabilities = DesiredCapabilities.FIREFOX
# firefox_capabilities['marionette'] = True
# driver = webdriver.Firefox(capabilities=firefox_capabilities)


driver = webdriver.Firefox()
driver.get("http://www.toolkiit.com")


# home page
login = driver.find_element_by_css_selector("#bs-example-navbar-collapse-1 li:nth-child(1) a")
login.send_keys(Keys.RETURN)


# login page
username = driver.find_element_by_css_selector("#id_username")
username.send_keys("mike")
password = driver.find_element_by_css_selector("#id_password")
password.send_keys("player13")
login_button = driver.find_element_by_css_selector(".btn")
login_button.send_keys(Keys.RETURN)


# home page, logged in
add_tool = driver.find_element_by_css_selector("#bs-example-navbar-collapse-1 li:nth-child(1) a")
add_tool.send_keys(Keys.RETURN)


# post new tool page
to_field = driver.find_element_by_css_selector("#id_to_field")
to_field.send_keys("machine")
do_field = driver.find_element_by_css_selector("#id_do_field")
do_field.send_keys("testing")
person = driver.find_element_by_css_selector("#id_person")
person.send_keys("is")
source_url = driver.find_element_by_css_selector("#id_source_url")
source_url.send_keys("www.toolkit.com")
summary = driver.find_element_by_css_selector("#id_summary")
summary.send_keys("on")
save_button = driver.find_element_by_css_selector(".btn")
save_button.send_keys(Keys.RETURN)

driver.close()