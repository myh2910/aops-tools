import textwrap
from timeit import default_timer

from selenium import webdriver
from selenium_stealth import stealth

from .config import CONFIG
from .utils import AOPS_URL


def print_dict_list(dict_lst, titles, keys):
	lens = [max(len(titles[0]), len(str(len(dict_lst) - 1))), len(titles[1])]
	for dct in dict_lst:
		lens[1] = max(lens[1], len(str(dct[keys[1]])))
	spaces = [(space := sum(lens) + 5), CONFIG["textwidth"] - space]

	print(f" {titles[0].ljust(lens[0])}  {titles[1].ljust(lens[1])}  {titles[2]}")
	print(f" {'--'.ljust(lens[0])}  {'--'.ljust(lens[1])}  --")

	for i, dct in enumerate(dict_lst):
		if str2 := dct[keys[1]]:
			str1 = f" {str(i).ljust(lens[0])}  {dct[keys[0]].ljust(lens[1])}  "
			if len(str2) > spaces[1]:
				print(str1, end="")
				for j, str3 in enumerate(textwrap.fill(str2, spaces[1]).split("\n")):
					if j > 0:
						print(" " * spaces[0], end="")
					print(str3)
			else:
				print(str1 + str2)
		else:
			print(f" {str(i).ljust(lens[0])}  {dct[keys[0]]}")

def get_chromedriver(code):
	options = webdriver.ChromeOptions()
	options.add_argument("start-maximized")
	options.add_argument("--headless")
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option("useAutomationExtension", False)
	driver = webdriver.Chrome(options=options)

	stealth(
		driver,
		languages=["en-US", "en"],
		vendor="Google Inc.",
		platform="Win32",
		webgl_vendor="Intel Inc.",
		renderer="Intel Iris OpenGL Engine",
		fix_hairline=True
	)

	driver.get(f"{AOPS_URL}/community/{code}")
	return driver

def get_topic_data(code, script="aops_tools/assets/topic-data.js"):
	begin_time = default_timer()

	driver = get_chromedriver(code)
	with open(script, "r", encoding="utf8") as file:
		data = driver.execute_script(file.read())

	driver.quit()
	return data, begin_time

def get_category_data(
	code,
	search_method=None,
	script="aops_tools/assets/category-data.js"
):
	begin_time = default_timer()

	driver = get_chromedriver(code)
	with open(script, "r", encoding="utf8") as file:
		data = driver.execute_script(file.read())

	while data["category_type"] == "folder":
		search_success = False
		if search_method:
			if text := search_method[0].strip():
				for item_data in data["items"]:
					if (
						text in item_data["item_text"]
						or text in item_data["item_subtitle"]
					):
						driver.get(f"{AOPS_URL}/community/c{item_data['item_id']}")
						with open(script, "r", encoding="utf8") as file:
							data = driver.execute_script(file.read())
						search_success = True
						break
			del search_method[0]

		if search_success:
			continue

		begin_time -= default_timer()
		go_deeper = input(":: This is a folder. Do you want to explore? [y/N] ")
		begin_time += default_timer()

		if go_deeper not in ["y", "Y"]:
			break

		print_dict_list(
			data["items"],
			("Index", "Text", "Description"),
			("item_text", "item_subtitle")
		)

		begin_time -= default_timer()
		idx = input(":: Select item index [default: 0] ")
		begin_time += default_timer()

		if idx:
			idx = int(idx)
		else:
			idx = 0

		driver.get(f"{AOPS_URL}/community/c{data['items'][idx]['item_id']}")
		with open(script, "r", encoding="utf8") as file:
			data = driver.execute_script(file.read())

		print()

	driver.quit()
	return data, begin_time
