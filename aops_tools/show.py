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

def stalk_success(to_stalk, username, thankers, num_thanks):
	if not to_stalk:
		return False
	if username in to_stalk:
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
		# check if that user is contained in `to_stalk`
		if num_thanks > 1:
			return hidden[:-len(hidden_thankers(num_thanks - 1)) - 1] in to_stalk
	# Delete the last message if it's hidden
	elif hidden == hidden_thankers(num_thanks - num_visible + 1):
		del visible[-1]
	return to_stalk & set(visible)

def show_topic_data(
	topic_code,
	to_stalk=None,
	to_find=None,
	verbose=False,
	silent=False,
	write_files=False,
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

	# Convert `to_stalk` and 'to_find` to set
	if to_stalk:
		if type(to_stalk) == str:
			to_stalk = {to_stalk}
	else:
		to_stalk = set()

	if to_find:
		if type(to_find) == str:
			to_find = {to_find}
		to_find.add(1)
	else:
		to_find = {1}

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

	if write_files:
		topic_path = os.path.join(outdir, f"c{category_id}", f"h{topic_id}")
		if not os.path.exists(topic_path):
			os.makedirs(topic_path)

		# Write json file
		with open(os.path.join(topic_path, "topic_data.json"), "w", encoding="utf8") as json_file:
			json.dump(topic_data, json_file, ensure_ascii=False, indent=num_indent)

	for post_idx, post_data in enumerate(posts_data):
		# Get post data
		post_canonical = post_data["post_canonical"]
		post_number = post_data["post_number"]
		post_rendered = post_data["post_rendered"]
		post_time = post_data["post_time"]
		post_url = post_data["post_url"]
		poster_id = post_data["poster_id"]
		thankers = post_data["thankers"]
		thanks_received = post_data["thanks_received"]
		username = post_data["username"]

		# Convert post time to utc format
		post_datetime = to_datetime(post_time, utc_offset, time_format)

		if not silent and (
			verbose
			or stalk_success(to_stalk, username, thankers, thanks_received)
			or post_number in to_find
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

		if write_files:
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

			# Write html content
			with open(os.path.join(topic_path, f"{post_number}.html"), "w", encoding="utf8") as html_file:
				html_file.write(str(soup))

	# End timer
	elapsed_time += default_timer()
	print_centered(None, textwidth, delim, Fore.CYAN)
	print_wrapped(textwrap.fill(f"Elapsed time: {elapsed_time:.2f} seconds", textwidth), len("Elapsed time"), Fore.LIGHTCYAN_EX)
