from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import bs4
import time
import sys
import os
import winsound

def getSlot( target_url ):
	# date settings
	localtime = time.localtime(time.time())
	month = localtime[1]
	date = localtime[2]
	
	# webdriver
	headers = {            
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
	}  
	driver = webdriver.Chrome('D:\chromedriver\chromedriver.exe')  # Optional argument, if not specified will search path.	
	
	loginState = autoInputLogin(driver)
	if not loginState:
		print('Login Failed!')
		return 
		
	#driver.get(target_url);
	if not checkPage(driver):
		print('Wrong Page Reached!')
		return
	print(driver.get_cookies())

	countDown(10, "Init and Login");
	today = date
	
	# loop
	no_open_slots = True
	#search_unattended_slot = True 
	while no_open_slots:   # refresh page every 2 seconds 
		html = driver.page_source              # fetch html of the target page 
		soup = bs4.BeautifulSoup(html, 'html.parser')          # break down the html
		
		# search next 3 days
		while date - today < 3:
			try:	
				button_id = 'date-button-2020-'+('%02d' % month)+'-'+('%02d' % date)+'-announce'
				date_button = driver.find_element_by_id(button_id)
				# print(date_button)
				if date != today:
					date_button.click()
			except:
				print('No such button! ' + button_id)

			date_slot_container_id = 'slot-container-2020-'+('%02d' % month)+'-'+('%02d' % date)
			date_slot_container = driver.find_element_by_id(date_slot_container_id)
			# print(slot_container_id, slot_container)
			
			#if search_unattended_slot:
			
			unattended_slot_container = date_slot_container.find_element_by_id('slot-container-UNATTENDED')
			no_slot_statement_unattended = 'No doorstep delivery windows are available for'
		
			
			# attended_slot_container = date_slot_container.find_element_by_id('slot-container-ATTENDED')
			# no_slot_statement_attended = 'No attended delivery windows are available for'

			
			print('Checking unattended delivery for 2020-'+('%02d' % month)+'-'+('%02d' % date))
			searchContainer(unattended_slot_container, no_slot_statement_unattended)  #unattended slot
			# searchContainer(attended_slot_container, no_slot_statement_attended)   #attended slot 
			
			date += 1  # next date 
			time.sleep(0.2)
		
		date = today   # reset date
		
		time.sleep(2)
		driver.refresh()
		print('\n\n\n\nPage refreshd')

def searchContainer(container, no_slot_statement):
	try:
		#print(container)
		alert_content = container.find_element_by_class_name('a-alert-content')
		#print('alert_content:', alert_content)
		span = alert_content.find_element_by_class_name('a-size-base-plus')
		#print('span:',span)
		page_slot_statement = span.text 
		#print('statement:', page_slot_statement)
		
		if no_slot_statement in page_slot_statement:
			pass
		else:
			print('SLOTS OPEN! No such (no slots) statement text')
			winsound.MessageBeep()
			os.system('msg %username%  "Slots for delivery opened!"')
			# no_open_slots = False
			time.sleep(3000)
		
	except NoSuchElementException:
		print('No such alert element')
		

def autoInputLogin(webdriver) :
	login_name = ''
	login_pass = ''

	login_url = 'https://www.amazon.com/ap/signin?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fcart%2Fview.html%3Fie%3DUTF8%26app-nav-type%3Dnone%26dc%3Ddf%26dc%3Ddf%26path%3D%252Fgp%252Fcart%252Fview.html%253Fapp-nav-type%253Dnone%26ref_%3Dcart_empty_sign_in%26useRedirectOnSuccess%3D1'
	

	try:
		# login 
		webdriver.get(login_url)
		time.sleep(3)
		email_inputbox = webdriver.find_element_by_id('ap_email')
		email_inputbox.send_keys(login_name)
		email_inputbox.submit()
		
		time.sleep(3)
		
		pass_inputbox = email_inputbox = webdriver.find_element_by_id('ap_password')
		pass_inputbox.send_keys(login_pass)
		pass_inputbox.submit()
		
		time.sleep(3)
		
		# direct to checkout (reserve time slot) page
		checkout_button = webdriver.find_element_by_class_name('a-button-input')
		print("proceeded")
		checkout_button.click()
		
		time.sleep(3)
		proceed_button = webdriver.find_element_by_name('proceedToCheckout')
		print("go to slot reservation page")
		proceed_button.click()
			
	except:
		return False 
		
	return True

def checkPage(webdriver):
	target_url = "www.amazon.com/gp/buy/shipoptionselect"
	if target_url not in webdriver.current_url:
		return False 
	return True



def countDown( seconds = 30, name = '' ):
	counter = seconds
	while counter>0:
		print(name+' countdown:'+str(counter))
		counter -= 1
		time.sleep(1) # Let the user actually see something!



getSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')









