from selenium import webdriver
from selenium_stealth import stealth
from .utils import aops_url

def get_topic_data(topic_code):
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

	# Go to AoPS topic
	driver.get(f"{aops_url}/community/{topic_code}")

	# Extract data and quit driver
	with open("aops_tools/assets/script.js", "r", encoding="utf8") as js_file:
		topic_data = driver.execute_script(js_file.read())
	driver.quit()

	# Return data
	return topic_data
