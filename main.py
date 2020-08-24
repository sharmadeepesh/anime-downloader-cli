import os
import get_download_url

try:
	import requests
	from bs4 import BeautifulSoup as bs
except ModuleNotFoundError:
	print("[NOTE] Some dependencies were not found on your system. Installing them automatically.")
	os.system('python -m pip install requests bs4 selenium clint')
	exit()

search_details = {}
links_to_download = []

final_data = {}
search_url = "https://www25.gogoanimes.tv/search.html?keyword={}"

def pass_data(data):
	global final_name
	links = [x for x in data.values()]
	names = [x for x in data.keys()]
	print("\nWe'll automatically save the videos in a folder named {} in your current directory: ".format(final_name))
	if ':' in final_name:
		final_name = final_name.replace(':','')
	try:
		os.mkdir(final_name)
	except FileExistsError:
		pass
	path = "./"+final_name+'/'
	for i in range(len(links)):
		try:
			get_download_url.get_link(links[i], names[i], path)
		except TypeError:
			print("[ERROR] Couldn't get this episode.")

def validate_choice(choice, resume_choice, links):
	anime_url = links[choice-1].split('/')[-1]
	final_data["Episode {}".format(resume_choice)] = "https://www25.gogoanimes.tv/{}-episode-{}".format(anime_url,resume_choice)
	pass_data(final_data)

def validate_choice_for_range(choice, start, end, links):
	anime_url = links[choice-1].split('/')[-1]
	for i in range(int(start)-1, int(end)):
		final_data["Episode {}".format(i+1)] = "https://www25.gogoanimes.tv/{}-episode-{}".format(anime_url,i+1)
	pass_data(final_data)

def validate_choice_for_whole(choice, links):
	global number_of_episodes
	anime_url = links[choice-1].split('/')[-1]
	for i in range(number_of_episodes):
		final_data["Episode {}".format(i+1)] = "https://www25.gogoanimes.tv/{}-episode-{}".format(anime_url,i+1)
	pass_data(final_data)

def get_choice(episodes, choice, links):
	print("\n[NOTE] Enter the number of episodes you want to download Total Episode Count = {}\n\nYou can :\n1. Enter the episode number for 1 episodes (example - 10).\n2. Enter episode range for multiple episodes (example - 2-6).\n3. Hit Enter for downloading the whole show.\n".format(episodes))
	resume_choice = input("[+] Enter your choice: ")
	if len(resume_choice)==0:
		validate_choice_for_whole(choice, links)
	elif '-' in resume_choice:
		start, end = resume_choice.split('-')
		validate_choice_for_range(choice, start, end, links)
	elif resume_choice.isdigit():
		validate_choice(choice, resume_choice, links)

def get_num_of_episodes(choice):
	global number_of_episodes
	links = [x for x in search_details.values()]
	titles = [x for x in search_details.keys()]
	try:
		res = requests.get(links[choice-1]).text
	except IndexError:
		print('\n[NOTE] Please choose a valid option next time.')
		exit()
	global final_name 
	final_name = titles[choice-1]
	soup = bs(res, 'html.parser')
	number_of_episodes = int(soup.find_all('ul',{'id':'episode_page'})[0].find_all('li')[-1].find('a').get('ep_end'))
	get_choice(number_of_episodes, choice, links)

def get_user_choice(search_details):
	i = 1
	print("\nWhich of the following animes would you like to download now (Enter Sno.): ")
	for key,value in search_details.items():
		print(i, ".", key)
		i = i + 1
	try:
		choice = int(input("\n[+] Enter your choice: "))
	except ValueError:
		print('\n[NOTE] Please choose a valid option next time.')
		exit()
	get_num_of_episodes(choice)

def get_details(soup):
    raw_soup = soup.find_all('div', {"class":'img'})
    for item in raw_soup:
        temp_soup = item.find('a')
        search_details[temp_soup['title']] = "https://www25.gogoanimes.tv" + temp_soup['href']

def get_soup(anime):
	res = requests.get(search_url.format(anime)).text
	soup = bs(res, 'html.parser')
	get_details(soup)

if __name__ == '__main__':
	anime = input("\nEnter the name of the anime you want to download : ")
	if len(list(anime))!=0:
		pass
	else:
		anime = input("\nEnter the name of the anime you want to download : ")
	get_soup(anime)
	get_user_choice(search_details)
	print("\n[DONE] All the episodes were downloaded and saved into the respective folder.")
