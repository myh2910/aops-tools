import colorama
import json
import os
import textwrap
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

def liked_by(to_stalk, thankers, num_thanks):
	# If `thankers` is not null
	if thankers:
		# Split `thankers` by comma
		visible = thankers.split(", ")
		num_visible = len(visible)
		# Get the last string of `visible`
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
		# Check if `visible` and `to_stalk` share a common user
		return set(visible) & to_stalk
	# Return false if `thankers` is null
	return False

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
	utc_offset=-5,
	time_format="%b %-d, %Y, %-I:%M %p"
):
	# Convert `to_stalk` to set
	if to_stalk:
		if type(to_stalk) == str:
			to_stalk = {to_stalk}
	else:
		to_stalk = set()
	# Convert `to_find` to list
	if to_find:
		if type(to_find) == str:
			to_find = [to_find]
	else:
		to_find = list()

	# Get topic data
	topic_data = get_topic_data(topic_code)
	(
		category_id,
		num_posts,
		posts_data,
		source,
		tags,
		topic_id,
		topic_title,
		topic_url
	) = topic_data.values()

	if verbose or not silent:
		colorama.init()
		# Print topic information
		print_centered("TOPIC INFO", textwidth, "#", BLUE)
		topic_info = {
			"Link": topic_url,
			"Title": topic_title
			}
		if tags:
			topic_info["Tags"] = ', '.join(tag["tag_text"] for tag in tags)
		if source:
			topic_info["Source"] = source
		topic_info["Post count"] = num_posts
		for key, value in topic_info.items():
			print_wrapped(textwrap.fill(f"{key}: {value}", textwidth), len(key), MAGENTA)

	if write_files:
		topic_path = os.path.join(outdir, f"c{category_id}", f"h{topic_id}")
		if not os.path.exists(topic_path):
			os.makedirs(topic_path)

		# Write json file
		with open(os.path.join(topic_path, "topic_data.json"), "w", encoding="utf8") as json_file:
			json.dump(topic_data, json_file, ensure_ascii=False, indent=num_indent)

	for post_data in posts_data:
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

		post_datetime = to_datetime(post_time, utc_offset, time_format)

		if (verbose
			or username in to_stalk
			or liked_by(to_stalk, thankers, thanks_received)
			or post_number in to_find
		):
			# Print post information
			print_centered("POST INFO", textwidth, "=", GREEN)
			post_info = {
				f"Post #{post_number}": post_url,
				"Posted by": f"{username} ({user_profile(poster_id)})",
				"Posted at": post_datetime
			}
			if thankers:
				post_info["Like count"] = thanks_received
				post_info["Liked by"] = thankers
			for key, value in post_info.items():
				print_wrapped(textwrap.fill(f"{key}: {value}", textwidth), len(key), YELLOW)

			print_centered("CONTENT", textwidth, "-", CYAN)
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
