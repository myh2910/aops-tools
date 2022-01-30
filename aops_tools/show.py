import json
import os
import textwrap
from timeit import default_timer
import colorama
from bs4 import BeautifulSoup
from .get import get_topic_data
from .utils import *

def hidden_thankers(num_hidden, all_hidden=False):
	# If all users are hidden
	if all_hidden:
		if num_hidden == 1:
			return "1 user"
		return f"{num_hidden} users"
	# If one user is hidden
	if num_hidden == 1:
		return "and 1 other user"
	# If more than one user is hidden
	return f"and {num_hidden} other users"

def stalk_success(stalk_users, username, thankers, num_thanks):
	if not stalk_users:
		return False
	if username in stalk_users:
		return True
	if not thankers:
		return False
	visible = thankers.split(", ")
	num_visible = len(visible)
	hidden = visible[-1]
	# If there is only one string in `visible`
	if num_visible == 1:
		# Return false if the last message is hidden
		if hidden == hidden_thankers(num_thanks, True):
			return False
		# If there is only one user that is not hidden,
		# check if that user is contained in `stalk_users`
		if num_thanks > 1:
			return hidden[:-len(hidden_thankers(num_thanks - 1)) - 1] in stalk_users
	# Delete the last message if it's hidden
	elif hidden == hidden_thankers(num_thanks - num_visible + 1):
		del visible[-1]
	return stalk_users & set(visible)

def show_topic_data(
	topic_code,
	stalk_users=None,
	find_posts=None,
	verbose=False,
	silent=False,
	write_files=False,
	export_to_json=False,
	export_to_html=False,
	outdir="community",
	num_indent=2,
	textwidth=95,
	delim="=",
	utc_offset=-5,
	time_format="%b %-d, %Y, %-I:%M %p"
):
	# Initialize timer and colorama
	elapsed_time = -default_timer()
	colorama.init()

	# Initial settings
	if stalk_users:
		if type(stalk_users) == str:
			stalk_users = {stalk_users}
	else:
		stalk_users = set()

	if find_posts:
		if type(find_posts) == str:
			find_posts = {find_posts}
	else:
		find_posts = set()

	if write_files:
		export_to_json = True
		export_to_html = True

	# Get topic data
	topic_data = get_topic_data(topic_code)
	(
		category_id,
		category_name,
		_, # num_deleted
		num_posts,
		num_views,
		posts_data,
		source,
		tags,
		topic_id,
		topic_title,
		topic_url
	) = topic_data.values()

	# Print topic information
	print_centered("TOPIC INFO", textwidth, delim, Fore.BLUE)
	topic_info = {
		"Link": topic_url,
		"Category": category_name,
		"Title": topic_title,
	}
	if tags:
		topic_info["Tags"] = ', '.join(tag["tag_text"] for tag in tags)
	if source:
		topic_info["Source"] = source
	topic_info["Post count"] = num_posts
	topic_info["View count"] = num_views
	for key, value in topic_info.items():
		print_wrapped(textwrap.fill(f"{key}: {value}", textwidth), len(key), Fore.LIGHTBLUE_EX)

	# Create folder
	if export_to_html or export_to_json:
		topic_path = os.path.join(outdir, f"c{category_id}", f"h{topic_id}")
		if not os.path.exists(topic_path):
			os.makedirs(topic_path)

	# Export to JSON
	if export_to_json:
		with open(os.path.join(topic_path, "topic_data.json"), "w", encoding="utf8") as json_file:
			json.dump(topic_data, json_file, ensure_ascii=False, indent=num_indent)

	for idx, attrs in enumerate(posts_data):
		# Get post data
		post_canonical = attrs["post_canonical"]
		post_number = attrs["post_number"]
		post_rendered = attrs["post_rendered"]
		post_time = attrs["post_time"]
		post_url = attrs["post_url"]
		poster_id = attrs["poster_id"]
		thankers = attrs["thankers"]
		thanks_received = attrs["thanks_received"]
		username = attrs["username"]

		# Convert post time to utc format
		post_datetime = to_datetime(post_time, utc_offset, time_format)

		if not silent and (
			verbose
			or idx == 0
			or stalk_success(stalk_users, username, thankers, thanks_received)
			or post_number in find_posts
		):
			# Print post information
			print_centered("POST INFO", textwidth, delim, Fore.MAGENTA)
			post_info = {
				f"Post #{post_number}": post_url,
				"Posted by": f"{username} ({user_profile(poster_id)})",
				"Posted at": post_datetime
			}
			if thankers:
				post_info["Like count"] = thanks_received
				post_info["Liked by"] = thankers
			for key, value in post_info.items():
				print_wrapped(textwrap.fill(f"{key}: {value}", textwidth), len(key), Fore.LIGHTMAGENTA_EX)

			print_centered("CONTENT", textwidth, delim, Fore.GREEN)
			for prop in post_canonical.split("\n"):
				print(textwrap.fill(prop, textwidth))

		if export_to_html:
			soup = BeautifulSoup(
f"""<!DOCTYPE html>
<html class="svg">
<head>
<meta charset="utf-8">
<meta name="viewport" content="initial-scale=1">
<title>Post #{post_number} by {username} at {post_datetime}</title>
<link rel="stylesheet" href="../../../aops_tools/assets/aops.css">
<link rel="icon" href="https://artofproblemsolving.com/online-favicon.ico">
<script src="../../../aops_tools/assets/aops.js"></script>
<script src="https://assets.artofproblemsolving.com/js/jquery.min.js"></script>
</head>
<body></body>
</html>""", "lxml")
			tmp = BeautifulSoup(post_rendered, "html.parser")
			# Replace image source links
			for img in tmp.find_all("img"):
				src = img["src"]
				if src.startswith("//"):
					img["src"] = "https:" + src
				elif src.startswith("/"):
					img["src"] = aops_url + src
			soup.find("body").append(tmp)

			# Export to HTML
			with open(os.path.join(topic_path, f"{post_number}.html"), "w", encoding="utf8") as html_file:
				html_file.write(str(soup))

	# End timer
	elapsed_time += default_timer()
	print_centered(None, textwidth, delim, Fore.CYAN)
	print_wrapped(textwrap.fill(f"Elapsed time: {elapsed_time:.2f} seconds", textwidth), len("Elapsed time"), Fore.LIGHTCYAN_EX)
