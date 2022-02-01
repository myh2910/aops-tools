import colorama
from .get import get_topic_data, get_category_data
from .utils import *

def show_topic_data(
	code,
	stalk_users=None,
	find_posts=None,
	silent=False,
	brave=False,
	verbose=False,
	write_files=False,
	write_json=False,
	write_html=False,
	outdir="community",
	num_indent=2,
	textwidth=95,
	delim="=",
	utc_offset=-5,
	time_format="%b %-d, %Y, %-I:%M %p"
):
	# Initial settings
	data, begin_time = get_topic_data(code)
	colorama.init()

	# Print topic information
	print_centered("Topic", textwidth, delim, Fore.BLUE)
	topic_info = {
		"Link": data["topic_url"],
		"Category": data["category_name"],
		"Title": data["topic_title"].strip()
	}
	if brave and (tags := data["tags"]):
		topic_info["Tags"] = ", ".join(tag["tag_text"] for tag in tags)
	if source := data["source"].strip():
		topic_info["Source"] = source
	topic_info["Post count"] = data["num_posts"]
	topic_info["View count"] = data["num_views"]
	for item in topic_info.items():
		print_wrapped(*item, textwidth, Fore.LIGHTBLUE_EX)

	# Create folder and write JSON file
	write_html, topic_path = write_json_file(
		data, num_indent, outdir, "topic-data",
		write_files, write_json, write_html, data["category_id"], data["topic_id"]
	)

	for idx, post_data in enumerate(data["posts_data"]):
		# Get post data
		post_number = post_data["post_number"]
		thankers = post_data["thankers"]
		thanks_received = post_data["thanks_received"]
		username = post_data["username"]

		# Convert post time to utc format
		post_datetime = to_datetime(post_time := post_data["post_time"], utc_offset, time_format)

		if not silent and (verbose or idx == 0
			or stalk_success(stalk_users, username, thankers, thanks_received)
			or (find_posts and post_number in find_posts)
		):
			# Print post information
			print_centered("Post", textwidth, delim, Fore.MAGENTA)
			post_info = {
				"Number": f"{post_number} ({post_data['post_url']})",
				"Posted by": f"{username} ({aops_url}/community/user/{post_data['poster_id']})",
				"Posted at": post_datetime
			}
			if thankers:
				post_info["Like count"] = thanks_received
				post_info["Liked by"] = thankers
			for item in post_info.items():
				print_wrapped(*item, textwidth, Fore.LIGHTMAGENTA_EX)

			if post_canonical := post_data["post_canonical"].strip():
				print_post(post_canonical, textwidth, delim)

		if write_html:
			write_html_file(f"Post #{post_number} by {username} at {post_datetime}",
				post_data["post_rendered"], topic_path, post_number)

	# End timer
	print_elapsed_time(begin_time, textwidth, delim)

def show_category_data(
	code,
	search_method=None,
	find_text=None,
	silent=False,
	brave=False,
	verbose=False,
	write_files=False,
	write_json=False,
	write_html=False,
	outdir="community",
	num_indent=2,
	textwidth=95,
	delim="="
):
	# Initial settings
	data, begin_time = get_category_data(code, textwidth, search_method)
	colorama.init()

	# Print category information
	print_centered("Category", textwidth, delim, Fore.BLUE)
	category_info = {"Link": data["category_url"], "Name": data["category_name"]}
	if short_description := data["short_description"].strip():
		category_info["Description"] = short_description
	for item in category_info.items():
		print_wrapped(*item, textwidth, Fore.LIGHTBLUE_EX)

	# Create folder and write JSON file
	write_html, path = write_json_file(
		data, num_indent, outdir, "category-data",
		write_files, write_json, write_html, data["category_id"]
	)

	if (category_type := data["category_type"]) == "view_posts":
		for idx, item_data in enumerate(data["items"]):
			item_text, item_type, post_data = item_data.values()
			post_canonical = post_data["post_canonical"].strip()
			post_type = post_data["post_type"]

			if not silent and (verbose or (find_text and (
				find_text in item_text or find_text in post_canonical
			))):
				# Print item information
				print_centered("Item", textwidth, delim, Fore.MAGENTA)
				post_info = dict()
				if post_type == "forum":
					post_info["Index"] = f"{idx} ({post_data['post_url']})"
				post_info["Type"] = item_type
				if item_text := item_text.strip():
					post_info["Text"] = item_text
				post_info["Post type"] = post_type
				for item in post_info.items():
					print_wrapped(*item, textwidth, Fore.LIGHTMAGENTA_EX)

				if (brave or item_type != "post_hidden") and post_canonical:
					print_post(post_canonical, textwidth, delim)

			if write_html:
				html_title = f"Post #{idx}"
				if item_text:
					html_title += ": " + item_text
				write_html_file(title, post_data["post_rendered"], path, idx)

	elif category_type == "folder":
		for idx, item_data in enumerate(data["items"]):
			item_subtitle = item_data["item_subtitle"].strip()
			item_text = item_data["item_text"].strip()

			if not silent and (verbose or (find_text and (
				find_text in item_text or find_text in item_subtitle
			))):
				# Print item information
				print_centered("Item info", textwidth, delim, Fore.MAGENTA)
				item_info = {
					f"Index": f"{idx} ({item_data['item_url']})",
					"Type": item_data["item_type"]
				}
				if item_text:
					item_info["Text"] = item_text
				if item_subtitle:
					item_info["Subtitle"] = item_subtitle
				for item in item_info.items():
					print_wrapped(*item, textwidth, Fore.LIGHTMAGENTA_EX)

	# End timer
	print_elapsed_time(begin_time, textwidth, delim)
