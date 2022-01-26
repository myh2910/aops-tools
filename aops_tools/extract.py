import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

def get_hidden_thankers(i, all_hidden=False):
	# If all users are hidden
	if all_hidden:
		if i == 1:
			return "1 user"
		return f"{i} users"
	# If not all users are hidden
	if i == 1:
		return "and 1 other user"
	return f"and {i} other users"

def extract_topic_info(topic_code):
	# ChromeDriver options
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
	aops_url = "https://artofproblemsolving.com/community"
	topic_url = aops_url + "/" + topic_code
	driver.get(topic_url)

	# Scroll down
	aops_scroll_inner = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
		(By.CLASS_NAME, "cmty-postbox-inner-box")
	)).find_element(By.XPATH, "..")
	prev_height = 0

	while True:
		time.sleep(1)
		driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", aops_scroll_inner)
		curr_height = driver.execute_script("return arguments[0].scrollHeight", aops_scroll_inner)
		if curr_height == prev_height:
			break
		prev_height = curr_height

	# Extract topic properties
	topic_subject = driver.find_element(By.CLASS_NAME, "cmty-topic-subject").text
	topic_tags = [item_tag.text for item_tag in driver.find_elements(
		By.XPATH, '//div[@class="cmty-tags-itembox-wrapper"]//a//div'
	)]
	topic_source = driver.find_element(By.CLASS_NAME, "cmty-topic-source-display").text
	if topic_source:
		topic_source = topic_source[8:]
	else:
		topic_source = None

	aops_dict = {
		"url": topic_url,
		"subject": topic_subject,
		"tags": topic_tags,
		"source": topic_source,
		"posts": []
	}

	# Extract post properties
	for cmty_post in driver.find_elements(By.CLASS_NAME, "cmty-post"):
		# Get post number and url
		cmty_post_number = cmty_post.find_element(By.CLASS_NAME, "cmty-post-number")
		cmty_post_number.click()
		cmty_post_direct_modal = driver.find_element(By.CLASS_NAME, "cmty-post-direct-modal")
		post_url = cmty_post_direct_modal.find_element(By.TAG_NAME, "input").get_attribute("value")
		driver.find_element(By.CLASS_NAME, "aops-close-x").click()

		# Get post html, username, user profile, date and edit info
		post_html = cmty_post.find_element(By.CLASS_NAME, "cmty-post-html").get_attribute("innerHTML")[11:]
		cmty_post_username = cmty_post.find_element(By.CLASS_NAME, "cmty-post-username")
		post_user_profile = cmty_post_username.find_element(By.TAG_NAME, "a").get_attribute("href")
		post_date = cmty_post.find_element(By.CLASS_NAME, "cmty-post-date").text
		post_edit_info = cmty_post.find_element(By.CLASS_NAME, "cmty-post-edit-info").text
		if not post_edit_info:
			post_edit_info = None

		# Get post thank count and thankers
		cmty_post_thank_count = cmty_post.find_element(By.CLASS_NAME, "cmty-post-thank-count")
		post_thank_count = cmty_post_thank_count.text
		if post_thank_count:
			post_thank_count = int(post_thank_count.split()[1])
			cmty_post_thank_count.click()
			cmty_thankers = cmty_post.find_element(By.CLASS_NAME, "cmty-thankers").text.split(", ")
			visible_thank_count = len(cmty_thankers)
			hidden_thankers = cmty_thankers[-1]
			if visible_thank_count == 1:
				if hidden_thankers == get_hidden_thankers(post_thank_count, True):
					cmty_thankers = []
				elif post_thank_count > 1:
					cmty_thankers = [hidden_thankers[:-len(get_hidden_thankers(post_thank_count - 1)) - 1]]
			elif hidden_thankers == get_hidden_thankers(post_thank_count - visible_thank_count + 1):
				del cmty_thankers[-1]
		else:
			post_thank_count = 0
			cmty_thankers = []

		aops_dict["posts"].append({
			"number": cmty_post_number.text[1:],
			"url": post_url,
			"username": cmty_post_username.text,
			"user-profile": post_user_profile,
			"date": post_date,
			"edit-info": post_edit_info,
			"thank-count": post_thank_count,
			"thankers": cmty_thankers,
			"html": post_html
		})

	# Quit driver and return dictionary
	driver.quit()
	return aops_dict
