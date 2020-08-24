from selenium import webdriver
import time
import download
from selenium.webdriver.chrome.options import Options
import subprocess

def get_link_from_xtreamcdn(url, name, path):
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--log-level=3")
	driver = webdriver.Chrome('./chromedriver.exe', options=options)

	driver.get(url)

	print("\n\n[+] Wait. We're getting the episode for you....")
	for i in range(0,5):
		time.sleep(1)
		
	iframe = driver.find_elements_by_tag_name('iframe')
	driver.find_elements_by_xpath('//*[@id="wrapper_bg"]/section/section[1]/div[1]/div[2]/div[9]/ul/li[5]/a')[0].click()
	time.sleep(5)
	driver.switch_to.frame(iframe[1])
	driver.find_elements_by_tag_name('a')[-1].click()
	driver.switch_to.window(driver.window_handles[0])
	driver.switch_to.frame(iframe[1])
	#time.sleep(2)
	driver.find_elements_by_xpath('//*[@id="loading"]/div')[0].click()
	driver.switch_to.window(driver.window_handles[0])
	driver.switch_to.frame(iframe[1])
	time.sleep(2)
	download_url = driver.find_elements_by_tag_name('video')[0].get_attribute('src')
	if download_url[0:4] == "blob":
		print("We are really sorry. The Episode couldn't be downloaded.\n")
	else:
		pass
	driver.quit()
	download.download(download_url, name, path)

def get_link(url, name, path):
	options = Options()
	options.add_argument("--headless")
	options.add_argument("--log-level=3")
	driver = webdriver.Chrome('./chromedriver.exe', options=options)

	driver.get(url)

	print("\n\n[+] Wait. We're getting the episode for you....")
	for i in range(0,5):
		time.sleep(1)
		
	iframe = driver.find_elements_by_tag_name('iframe')
	driver.switch_to.frame(iframe[1])
	driver.find_elements_by_tag_name('div')[-1].click()
	driver.switch_to.window(driver.window_handles[0])
	driver.switch_to.frame(iframe[1])
	driver.find_elements_by_xpath('//*[@id="myVideo"]/div[2]/div[12]/div[1]/div/div/div[2]/div')[0].click()
	download_url = driver.find_elements_by_tag_name('video')[0].get_attribute('src')
	
	if download_url[0:4] == "blob":
		print("\n[+] Hold Up. We are trying another server.")
		driver.quit()
		get_link_from_xtreamcdn(url, name, path)
	elif download_url[0:5] == "https":
		driver.quit()
		download.download(download_url, name, path)
	else:
		driver.quit()
		pass
	