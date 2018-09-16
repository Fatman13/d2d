#!/usr/bin/env python
# coding=utf-8

import click
import datetime, time
import random
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException   
from selenium.common.exceptions import ElementNotVisibleException   
from selenium.common.exceptions import StaleElementReferenceException   
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException

MAX_RETRIES = 3
usr_css_selector = ".input_tip[data-bind='textinput:fields.username,placeholder:\'账号|tip_form\'']"
usr_css_selector1 = ".input_tip[type='text']"
pwd_css_selector = ".input_tip[data-bind='textinput:fields.password,placeholder:\'密码|tip_form\'']"
pwd_css_selector1 = ".input_tip[type='password']"

num1_css_selector = 'div.sumBtn_list:nth-child(1) > div:nth-child(2) > a:nth-child(1)'
num2_css_selector = 'div.sumBtn_list:nth-child(1) > div:nth-child(2) > a:nth-child(2)'
num3_css_selector = 'div.sumBtn_list:nth-child(1) > div:nth-child(2) > a:nth-child(3)'
num4_css_selector = 'div.sumBtn_list:nth-child(1) > div:nth-child(2) > a:nth-child(4)'
num5_css_selector = 'div.sumBtn_list:nth-child(1) > div:nth-child(2) > a:nth-child(5)'

round_over_css_selector = 'div.direction:nth-child(3) > a:nth-child(1)'
round_over_css_selector1 = 'div.direction:nth-child(3)'
# div.direction:nth-child(3) > a:nth-child(1)
# div.direction:nth-child(3)
balance_css_selector = '.userName > span:nth-child(2) > label:nth-child(1)'
timeleft_css_selector = 'label.fc-white:nth-child(3)'
multiplier_css_selector = '.native-select'

r_result_css_selector = '.Result > a:nth-child(1)'
r_num_css_selector = '.Result-box > dl:nth-child(1) > dd:nth-child(2) > i:nth-child(1) > label:nth-child(1)'
r_id_css_selector = '.Result-box > dl:nth-child(1) > dt:nth-child(1) > label:nth-child(1)'
cur_r_id_css_selector = 'label.fc-white:nth-child(1)'

path_to_firefox = '/Applications/Firefox.app/Contents/MacOS/firefox'

WIN = 1
LOSE = 0

def login(driver):
	url = 'http://gf2.xun1616.com:90/login'

	driver.get(url)
	# driver.find_element_by_css_selector('.d-close').click()
	# print('Close message board..')
	print('Logging in.. ')

	username = driver.find_element_by_id('username')
	password = driver.find_element_by_id('password')
	username.clear()
	password.clear()
	username.send_keys('lengyu250')
	password.send_keys('lbb520')

	driver.find_element_by_id('login').click()
		
	# print('logged in.. ')
	return None

# def gen_bet(last_r_result, last_r_bet, last_r_num):
# 	if last_r_result == LOSE:
# 		return last_r_bet
# 	choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 	if last_r_result == WIN:
# 		choices.remove(int(last_r_num))


# def gen_multi(last_r_result, last_r_multiplier):
# 	if last_r_result == LOSE:
# 		last_r_multiplier = last_r_multiplier * 3
# 	if last_r_result == WIN:
# 		last_r_multiplier = 1


@click.command()
def lottery():
	
	# binary = FirefoxBinary(path_to_firefox)
	# binary.add_command_line_options('-devtools')
	useragent = 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'
	profile = webdriver.FirefoxProfile()
	profile.set_preference("general.useragent.override", useragent)
	profile.set_preference("devtools.toolbox.host", "right")
	driver = webdriver.Firefox(profile)
	driver.set_window_position(0, 0)
	driver.set_window_size(632, 768)
	# driver.get('google.com')
	# return

	login(driver)
	time.sleep(1)

	# driver.find_element_by_tag_name("body").send_keys(Keys.COMMAND + Keys.ALT + 'c')

	for i in range(MAX_RETRIES):
		try:
			driver.find_element_by_css_selector('a.d-close').click()
		except NoSuchElementException:
			print('Waring: no such ele.. retry {}'.format(i))
			time.sleep(1)
			continue
		except ElementNotInteractableException:
			print('Waring: ele not interactable.. retry {}'.format(i))
			time.sleep(1)
			continue
		else:
			break

	driver.find_element_by_css_selector('.OFFICIAL_PKS').click()
	driver.find_element_by_css_selector('.icon-150 ').click()

	for i in range(MAX_RETRIES):
		try:
			# time_left = driver.find_element_by_css_selector('fc-white').text
			time_left = driver.find_element_by_css_selector(timeleft_css_selector).text
			print('init time left.. {}'.format(time_left))
			select = Select(driver.find_element_by_css_selector('.native-select'))
			# select by visible text
			select.select_by_visible_text('角')
		except NoSuchElementException:
			print('Waring: no such ele.. retry {}'.format(i))
			time.sleep(1)
			continue
		except ElementNotInteractableException:
			print('Waring: ele not interactable.. retry {}'.format(i))
			time.sleep(1)
			continue
		else:
			break

	r_stat = {}
	# r_stat['last_r_bet'] = [1, 2, 3, 4, 5]
	# last_r_num = 1
	# last_r_multiplier = 1
	# last_r_bet = [1, 2, 3, 4, 5]
	# last_r_num = 1
	# last_r_multiplier = 1
	# last_r_result = WIN
	r_counter = 0
	# id, bet, multiplier; num, result, to_sum

	while True:
		print('=== Start of Round ({}) ==='.format(r_counter))

		try:
			driver.find_element_by_css_selector(round_over_css_selector).click()
			# driver.find_element_by_css_selector(round_over_css_selector1).click()
		except NoSuchElementException:
			print('Warnig: no popup yet..')

		# if last_r_num in last_r_bet:
		# 	last_r_result
		for i in range(MAX_RETRIES):
			try:
				driver.find_element_by_css_selector(r_result_css_selector).click()
				time.sleep(1)
			except ElementClickInterceptedException:
				print('Waring: ele1 click intercepted.. retry {}'.format(i))
				time.sleep(1)
				continue
			else:
				break
		last_r_id = driver.find_element_by_css_selector(r_id_css_selector).text
		r_num = driver.find_element_by_css_selector(r_num_css_selector).text
		# driver.find_element_by_css_selector(r_result_css_selector).click()
		for i in range(MAX_RETRIES):
			try:
				driver.find_element_by_css_selector(r_result_css_selector).click()
				time.sleep(1)
			except ElementClickInterceptedException:
				print('Waring: ele2 click intercepted.. retry {}'.format(i))
				time.sleep(1)
				continue
			else:
				break
		print('Last round result.. id: {} num: {}'.format(last_r_id, r_num))

		cur_r_id = driver.find_element_by_css_selector(cur_r_id_css_selector).text
		print('Current round.. id {}'.format(cur_r_id))

		if last_r_id in r_stat.keys():
			r_stat[last_r_id]['num'] = int(r_num)
			if int(r_num) in r_stat[last_r_id]['bet']:
				r_stat[last_r_id]['result'] = WIN
				r_stat[last_r_id]['to_sum'] = int(r_stat[last_r_id]['multiplier'])

				# take guess when wining last round..
				choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
				choices.remove(r_stat[last_r_id]['num'])

				r_stat[cur_r_id] = {}
				r_stat[cur_r_id]['bet'] = random.sample(choices, 5)
				r_stat[cur_r_id]['multiplier'] = 1

			else:
				r_stat[last_r_id]['result'] = LOSE
				r_stat[last_r_id]['to_sum'] = int(r_stat[last_r_id]['multiplier'])*-1

				r_stat[cur_r_id] = {}
				r_stat[cur_r_id]['bet'] = r_stat[last_r_id]['bet']
				r_stat[cur_r_id]['multiplier'] = int(r_stat[last_r_id]['multiplier'])*3

			print('last r bet: {} multiplier: {} num: {} result {}'.format(
														r_stat[last_r_id]['bet'], 
														r_stat[last_r_id]['multiplier'],
														r_stat[last_r_id]['num'], 
														r_stat[last_r_id]['result']
														))

			# log to csv
			ent = {}
			ent['id'] = last_r_id
			ent['bet'] = r_stat[last_r_id]['bet']
			ent['multiplier'] = r_stat[last_r_id]['multiplier']
			ent['num'] = r_stat[last_r_id]['num']
			ent['result'] = r_stat[last_r_id]['result']
			ent['to_sum'] = r_stat[last_r_id]['to_sum']
			ent['timestamp'] = str(datetime.datetime.now())
			res = []
			res.append(ent)
			with open('lottery_log.csv', 'a', newline='', encoding='utf-8') as f:
				dict_writer = csv.DictWriter(f, ent.keys())
				dict_writer.writerows(res)
		else:
			# new round
			choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
			r_stat[cur_r_id] = {}
			r_stat[cur_r_id]['bet'] = random.sample(choices, 5)
			r_stat[cur_r_id]['multiplier'] = 1

		# time_left = driver.find_element_by_css_selector('fc-white').text
		time_left = driver.find_element_by_css_selector(timeleft_css_selector).text

		print('while time left.. {}'.format(time_left))
		x = time.strptime(time_left, '%H:%M:%S')
		seconds = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
		print('Sleeping.. {} second(s)'.format(seconds+10))
		time.sleep(seconds+10)
		r_counter = r_counter + 1

if __name__ == '__main__':
	lottery()