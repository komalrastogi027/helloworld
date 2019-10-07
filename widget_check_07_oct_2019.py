# -*- coding: utf-8 -*-
# import pymysql as MySQLdb
import MySQLdb
import json,time,sys 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import simplejson as sjson
from selenium.common.exceptions import TimeoutException
import random
from datetime import datetime,date
import time
import os
import sys



class widget_testing(object):
	def __init__(self):
		self.dbname='cartwire'
		self.dbuser='cartwire'
		self.dbpass='&yHn3jTRfn_a'
		self.dbhost='192.200.12.13'
		self.table_name= 'domain_status'
		self.num_try=1
		self.num_try1=1
		self.click_count=2
		self.chromedriver='/home/komal/Downloads/chromedriver'
		# self.chromedriver='/home/prince/Documents/python/selenium_all_code/drivers/chromedriver_linux64/chromedriver'
		# self.chromedriver=r'C:\Users\STPL\Downloads\chromedriver_win32\chromedriver.exe'
		# self.chromedriver='/home/prince/Documents/python/selenium all code/download image/chromedriver_linux64/chromedriver'
		self.options = webdriver.ChromeOptions()
		self.options.add_argument('headless')
		self.options.add_argument('--start-maximized')
		self.options.add_argument("--disable-infobars")
		self.options.add_argument("--disable-extensions")
		self.options.add_argument("--disable-notifications")
		self.options.add_argument("--disable-popup-blocking")

	def dbase_connect(self):
		self.db=MySQLdb.connect( host=self.dbhost, user=self.dbuser, password=self.dbpass,database=self.dbname, use_unicode=True, charset="utf8")
		self.cursor=self.db.cursor()

	def create_json_file(self,id=-1,start_date=-1,end_date=-1):
		self.dbase_connect()
		try:
			if(id==-1):
				sql="select json_xpath from domain_xpath dx inner join domain_master_rev dm on dx.domain_id=dm.id where dm.widget_delivery_date between '%s' and '%s' " %(start_date , end_date)
				self.cursor.execute(sql)
				data=self.cursor.fetchall()
				dict={}
				for i in data:
					data1=sjson.loads(i[0])
					c=data1['domain_name'].split('-')
					name=(c[1]+' - '+c[0]).strip()
					dict[name]=data1
				self.widget_test(dict)
			else:
				list_id = id.split (",")
				for i in list_id:
					sql="select json_xpath from domain_xpath where domain_id=%s" % (i)
					self.cursor.execute(sql)
					data=self.cursor.fetchall()
					dict={}
					for j in data:
						data1=sjson.loads(j[0])
						c=data1['domain_name'].split('-')
						name=(c[1]+' - '+c[0]).strip()
						dict[name]=data1
					self.widget_test(dict)
		except Exception as e:
			print('error',e)
 
	def widget_test(self,brand_data):
		self.dbase_connect()
		key_list=sorted(list(brand_data.keys()))
		if(len(key_list)==1):
			start_index=0
		else:
			try:
				if del_check=='1':
					self.delete_checkpoint('widget_')

				start_brand=self.checkpoint_read('widget_')
				start_index=int(key_list.index(start_brand))+1
			except:
				start_index=0
		self.driver = webdriver.Chrome(executable_path=self.chromedriver, chrome_options=self.options)
		for brands in key_list[start_index:]:
			is_live = brand_data[brands]['is_live']
			# if is_live=='0':
			# 	self.db_create(brand_data[brands]['domain_id'],brand_data[brands]['domain_website'],"","",2)
			# else:
			main_prod=0
			self.flag=0
			self.indx=0
			self.indx1=0
			self.product_title=" "
			self.product_list=['']
			self.tried=0
			self.click_trying =0
			print("Total no. of brands : ",len(brand_data))
			print("completed no. of brands : ",int(len(brand_data)) - (int(len(brand_data)) - int(key_list.index(brands))))
			print("remaining no. of brands : ",int(len(brand_data)) - int(key_list.index(brands)))
			print("*"*50)
			print("*"*50)
			print("For :",brands)
			print("-"*50)
			print("-"*50)
			self.website_status='0'
			self.product_list_status='0'
			self.button_status='0'
			self.popup_status='0'
			self.product_title_status='0'
			self.popup_opt_status='0'
			self.loader_status='0'
			self.load='0'
			self.get_title='0'
			while self.site_checker(brand_data,brands) and self.tried < self.num_try:
				if self.tried < self.num_try:
					self.tried=self.tried+1
					print("No. of tries...",self.tried)
				else:
					print("Max No. of tries...")
					print("Not found...")

			if self.load == '0' :
				self.driver.close()
				self.driver = webdriver.Chrome(executable_path=self.chromedriver, chrome_options=self.options)

			if self.website_status !=1 or self.product_list_status !=1 or self.product_title_status !=1 or self.button_status !=1 or self.loader_status != 1 or (self.popup_status != 1 or self.popup_status !=2) :
				self.result_file(brands,'result.rst')

			print('popup_opt_status',self.popup_opt_status)
			print('website_status',self.website_status)
			print('product_list_status',self.product_list_status)
			print('product_title_status',self.product_title_status)
			print('button_status',self.button_status)
			print('popup_status',self.popup_status)
			print('loader_status',self.loader_status)
			print("-"*50)
			print("-"*50)
			print("\n")
			print("="*50)
			print("="*50)

			try:
				self.product_title=self.product_title.text
			except:
				self.product_title=self.product_title

			if self.flag==1:
				main_prod=self.indx
				self.website_status='1'
				self.product_list_status='1'
				self.button_status='1'
				self.popup_status='1'
				self.product_title_status='1'

			else:
				main_prod=self.indx1

			try:
				if self.product_list[0]=='':
					self.final_check(brand_data[brands]['domain_id'],brand_data[brands]['domain_website'],self.product_title,brand_data[brands]['is_live'],brand_data[brands]['domain_website'])
				else:
					print(1,main_prod)
					self.final_check(brand_data[brands]['domain_id'],main_prod,self.product_title,brand_data[brands]['is_live'],brand_data[brands]['domain_website'])
			except:
				self.final_check(brand_data[brands]['domain_id'],brand_data[brands]['domain_website'],self.product_title,brand_data[brands]['is_live'],brand_data[brands]['domain_website'])
			
			if(len(key_list)>1):
				self.checkpoint_create(brands,'widget_')

		self.driver.close()

	def check_load(self,x_path,check):
		load_try=0
		universal='0'
		while universal !='1' and load_try < self.num_try1:
			try:
				if check=='get':
					self.driver.get(x_path)
					return '1','1'
				elif check=='element':
					element_data = self.driver.find_element_by_xpath(x_path)
					if x_path==("//span[@class='ietxtDesc']"):
						return element_data,'2'
					else:
						return element_data,'1'
				elif check=='elements':
					element_data = self.driver.find_elements_by_xpath(x_path)
					return element_data,'1'
				universal ='1'
			except Exception as p:
				universal ='2'
			load_try=load_try+1
		return '0','0'


	def site_checker(self,brand_data,brands):
		try: 
			self.driver.set_page_load_timeout(60)
			temp_var,self.load=self.check_load(brand_data[brands]['product_list_url'],'get')
			time.sleep(3)
			self.driver.implicitly_wait(5)

			if brand_data[brands]['cookie_json'] != '0':
				self.add_cookie_jsons(brand_data[brands]['product_list_url'],brand_data[brands]['cookie_json'])
			try:
				if brand_data[brands]['popup_xpath'] != '0' :
					popup_opt_xpath,self.popup_opt_status =self.check_load(brand_data[brands]['popup_xpath'],'element')
					popup_opt_xpath.click()
			except:
				pass
			self.driver.implicitly_wait(2)
			self.website_status='1'
			product_xpath,self.product_list_status =self.check_load(brand_data[brands]['products_xpath'],'elements')

			self.product_list=[link.get_attribute('href') for link in product_xpath]
			if len(self.product_list) > 3 :
				random_items= random.sample(self.product_list, 3)
			elif len(self.product_list) <= 3:
				random_items= random.sample(self.product_list, 1)
			print(random_items)
			for item in random_items:
				print(item)
				try:
					self.driver.get(item)	
				except:
					return False
				self.driver.implicitly_wait(4)
				time.sleep(3)

				self.product_title,self.product_title_status=self.check_load(brand_data[brands]['title_xpath'],'element')
				try:
					print("title : ",self.product_title.text,"(",brands,")")
				except:
					print("title : ",self.product_title,"(",brands,")")

				time.sleep(2)
				button_xpath,self.button_status = self.check_load(brand_data[brands]['button_xpath'],'element')
				try:
					self.driver.execute_script("arguments[0].click();", button_xpath)
					self.driver.execute_script("arguments[0].click();", button_xpath)
				except:
					self.indx1=brand_data[brands]['domain_website']
					button_xpath.click()
				time.sleep(3)
				self.driver.implicitly_wait(4)
				loader_xpath,self.loader_status = self.check_load('//div[@id="siteLoader_cw"]/div/span','element')
				time.sleep(3)
				self.driver.implicitly_wait(4)
				brand_data[brands]['widget_xpath'] = brand_data[brands]['widget_xpath'].replace('/text()','')
				popup_text,self.popup_status=self.check_load(brand_data[brands]['widget_xpath'],'element')
				if self.popup_status !='1': 
					popup_text,self.popup_status=self.check_load("//span[@class='ietxtDesc']",'element')
					print(popup_text)
					self.driver.implicitly_wait(3)
				if self.popup_status =='0':
					if(self.loader_status=='0'):
						self.popup_status='3'

				if self.website_status ==1 and self.product_list_status ==1 and self.product_title_status ==1 and self.button_status ==1 and self.loader_status == 1 and self.popup_status == 1:
					self.flag=1
					self.indx=item
				else:
					self.indx1=item

			return False
		except Exception as s:
			print("&"*50)
			print("Main Error",s)
			print("&"*50)
			print("\n")
			return True

	def add_cookie_jsons(self,url,cookie_json_data):
		self.driver.get(url)
		self.driver.delete_all_cookie_jsons()
		try:
			print ("Injecting cookie_jsons")
			for cookie_json_attr in cookie_json_data:
				self.driver.add_cookie_json(cookie_json_attr)
			print( "cookie_jsons Injected Successfully")
		except:
			print( "Error While Adding cookie_jsons")

	def final_check(self,id,url,title,is_live,domain_url):
		if is_live=='0':
			if self.website_status=='0':
				self.db_create(id,domain_url,title,"Brand website not available",2)
			else:
				if self.button_status=='0':
					self.db_create(id,domain_url,title,"BIN Widget not implemented",2)
				else:
					if self.popup_status=='0':
						self.db_create(id,url,title,"Wrong BIN Implementation",2)
					elif self.popup_status=='1':
						self.db_create(id,url,title,"",2)
					elif self.popup_status=='2':
						self.db_create(id,url,title,"Wrong BIN Implementation",2)
					elif self.popup_status=='3':
						self.db_create(id,url,title,"Different BIN solution implemented",2)
		elif is_live=='1':
			if self.website_status=='0':
				self.db_create(id,url,title,"Brand site not working",3)
				self.product_list_last(id,url)
			else:
				if self.button_status=='0':
					self.db_create(id,url,title,"Brand site renewed",3)
					self.product_list_last(id,url)
				else:
					if self.popup_status=='0':
						self.db_create(id,url,title,"Wrong BIN Implementation",3)
						self.product_list_last(id,url)
					elif self.popup_status=='1':
						self.db_create(id,url,title,"",1)
						self.db_update(id,"last_click_date")
					elif self.popup_status=='2':
						self.db_create(id,url,title,"Wrong BIN Implementation",3)
						self.product_list_last(id,url)
					elif self.popup_status=='3':
						self.db_create(id,url,title,"Brand moved to different BIN solution",3)
						self.product_list_last(id,url)


	def db_update(self,domain_id,field_name):
		self.dbase_connect()
		sql2="UPDATE `domain_master_rev` SET `%s` = '' WHERE `domain_master_rev`.`id` = %s"%(field_name,domain_id)
		self.cursor.execute(sql2)
		self.db.commit()


	def db_create(self,domain_id,url,title,error,status):
		self.dbase_connect()
		sql1="select id from domain_status where domain_id=%s and verify_date >=CURDATE()" %(domain_id)
		self.cursor.execute(sql1)
		date_check=self.cursor.fetchall()

		if date_check:
			title = title.replace("'","\\'")
			title = title.replace('"','\\"')

			sql2="""update domain_status set domain_id="%s",brand_product_URL="%s", widget_product="%s", brand_error="%s", brand_live_status="%s", verify_date=CURRENT_TIMESTAMP where id =%s"""%(domain_id,url,title,error,status,date_check[0][0])
		else:
			sql2="""INSERT INTO domain_status(domain_id, brand_product_URL, widget_product, brand_error, brand_live_status, verify_date) VALUES (""" +str(domain_id)+ """, " """+str(url)+ """ "," """ +str(title)+ """ "," """ +str(error)+ """ ", """ +str(status)+ """,CURRENT_TIMESTAMP)"""
		self.cursor.execute(sql2)
		self.db.commit()	
	
	def product_list_last(self,id,url):
		try:
			self.dbase_connect()
			sql="SELECT created_date FROM widget_source_view where source_url LIKE '%s%%' and report_status != 'cw_test' order by modified_date ASC limit 1" %(url)
			self.cursor.execute(sql)
			created_date=(self.cursor.fetchone())
			click_date=(created_date[0].strftime("%Y-%m-%d"))
			self.last_click_update(id,click_date)
		except:
			print('Url not found')

	def last_click_update(self,d_id,created_on):
		self.dbase_connect()
		sql3="UPDATE `domain_master_rev` SET `last_click_date` = '%s' WHERE `domain_master_rev`.`id` = %s" %(created_on,d_id)
		self.cursor.execute(sql3)
		self.db.commit()

	def checkpoint_create(self,i,filename):
		dirName = 'checkpoint'
		if not os.path.exists(dirName):
			os.mkdir(dirName)
		else:
			name=dirName+'/'+ filename + str(date.today().strftime('%Y_%m_%d'))+".ckpt"
			f = open(name, "w")
			f.write(str(i))
			f.close()

	def delete_checkpoint(self,filename):
		try :
			name='checkpoint/'+ filename +str(date.today().strftime('%Y_%m_%d'))+".ckpt"
			os.remove(name)
		except:
			print("Error while deleting file ")

	def checkpoint_read(self,filename):
		try:
			name='checkpoint/' + filename + str(date.today().strftime('%Y_%m_%d'))+".ckpt"
			f = open(name, "r")
			check=f.read()
			return check
		except:
			return 0

	def result_file(self,i,filename):
		f = open(filename, "a+")
		f.write(str(i))
		f.write('\n')
		f.close()

widget_obj=widget_testing()
input=sys.argv

try:
	if input[3]:
		del_check=input[3]
except:
	del_check=0

try:
	if(len(input[1])==10 and len(input[2])==10):
		widget_obj.create_json_file(-1,input[1],input[2])
	elif(len(input[1])<10 or len(input[1])>10):
		widget_obj.create_json_file(input[1])
except Exception as e:
	print("start error",e)





