from timeit import default_timer
from selenium import webdriver
from selenium_stealth import stealth
from .utils import aops_url, print_dict_list

def get_chromedriver(code):
	# Add ChromeDriver options
	options = webdriver.ChromeOptions()
	options.add_argument("start-maximized")
	options.add_argument("--headless")
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option("useAutomationExtension", False)
	driver = webdriver.Chrome(options=options)

	# Use selenium stealth
	stealth(
		driver,
		languages=["en-US", "en"],
		vendor="Google Inc.",
		platform="Win32",
		webgl_vendor="Intel Inc.",
		renderer="Intel Iris OpenGL Engine",
		fix_hairline=True
	)

	# Go to AoPS link and return driver
	driver.get(f"{aops_url}/community/{code}")
	return driver

def get_topic_data(code, js_script="topic-data.js"):
	begin_time = default_timer()

	driver = get_chromedriver(code)
	with open(f"aops_tools/assets/{js_script}", "r", encoding="utf8") as js_file:
		data = driver.execute_script(js_file.read())

	driver.quit()
	return data, begin_time

def get_category_data(code, textwidth, search_method=None, js_script="category-data.js"):
	begin_time = default_timer()

	driver = get_chromedriver(code)
	with open(f"aops_tools/assets/{js_script}", "r", encoding="utf8") as js_file:
		data = driver.execute_script(js_file.read())

	while data["category_type"] == "folder":
		search_success = False
		if search_method:
			if text := search_method[0].strip():
				for item_data in data["items"]:
					if text in item_data["item_text"] or text in item_data["item_subtitle"]:
						driver.get(f"{aops_url}/community/c{item_data['item_id']}")
						with open(f"aops_tools/assets/{js_script}", "r", encoding="utf8") as js_file:
							data = driver.execute_script(js_file.read())
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

		print_dict_list(items := data["items"],
			("Index", "Text", "Description"), ("item_text", "item_subtitle"), textwidth)

		begin_time -= default_timer()
		idx = input(":: Select item index [default: 0] ")
		begin_time += default_timer()

		if idx:
			idx = int(idx)
		else:
			idx = 0

		driver.get(f"{aops_url}/community/c{items[idx]['item_id']}")
		with open(f"aops_tools/assets/{js_script}", "r", encoding="utf8") as js_file:
			data = driver.execute_script(js_file.read())
		print()

	driver.quit()
	return data, begin_time
