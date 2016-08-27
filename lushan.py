#coding:utf-8

import os   
import time
from selenium import webdriver
import aes_cipher

class aeon_card_scraping:
	url = "http://www.aeon.co.jp/creditcard/"
	DRIVER_PATH = os.path.join(os.path.dirname(__file__),"chromedriver")
	cipher = aes_cipher("test")

	def start(self):
		browser = webdriver.Chrome(self.DRIVER_PATH)
		browser.get(self.url)
		try:
			# top page block
			login_page_button = browser.find_element_by_css_selector("a.btn-03.str-03.str-cv")
			login_page_button.click()
			
			# login page block

		finally:
			browser.quit()


if __name__ == "__main__":
	acs = aeon_card_scraping();
	acs.start()
