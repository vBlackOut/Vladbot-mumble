import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
import sys


navigateur = webdriver.Firefox()
navigateur.get('http://www.google.com')

search = navigateur.find_element_by_id('lst-ib')
search.send_keys(sys.argv[1])
search.send_keys(Keys.RETURN) # hit return after you enter search text
time.sleep(3) # sleep for 5 seconds so you can see the results
compteur = 0
for venue in navigateur.find_elements_by_xpath('//a[@class="q qs"]'):
	compteur = compteur + 1
	if venue.text == "Images":
		venue.click()
		break

time.sleep(3)
print(navigateur.page_source.encode('utf-8'))
navigateur.quit()