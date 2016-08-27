#coding:utf-8

import os   
import time
from selenium import webdriver
from aes_cipher import AESCipher
from getpass import getpass

class aeon_card_scraping:
	url = "http://www.aeon.co.jp/creditcard/"
	DRIVER_PATH = os.path.join(os.path.dirname(__file__),"chromedriver")

	def start(self):
		# read id-pass file
		cipher = AESCipher(getpass())
		try:
			id,ps = cipher.read_pass()
		except:
			print "Cannot read id-pass.txt"
			exit()

		browser = webdriver.Chrome(self.DRIVER_PATH)
		browser.get(self.url)
		try:
			# top page block
			browser.find_element_by_css_selector("a.btn-03.str-03.str-cv").click()
			
			# login page block
			browser.find_element_by_name("netMemberId").send_keys(id)
			browser.find_element_by_name("password").send_keys(ps)
			browser.find_element_by_css_selector("button.btn-03.str-03.center").click()

			# needs otp process

			# displaying charge page block
			print browser.find_element_by_css_selector("span.num").text

			# for debug(pause browser)
			raw_input()
		finally:
			browser.quit()

			"""
			ワンタイムPWを要求する画面

			ワンタイムPWを入力する画面
			browser.find_element_by_name("otpwd").send_keys(id)
			terminalRegist2

			端末の登録をする画面
			"""

if __name__ == "__main__":
	acs = aeon_card_scraping();
	acs.start()
