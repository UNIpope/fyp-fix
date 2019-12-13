from selenium import webdriver
from pprint import pprint

# get website
DRIVER = 'chromedriver'
driver = webdriver.Chrome(DRIVER)
driver.get('https://www.tensorflow.org/install/gpu')

# get height of website 
html = driver.execute_script("return document.documentElement")
h, w = html.size.values()
driver.set_window_size(w+200, h+200)

# get screenshot
driver.save_screenshot('out.png')
driver.quit()