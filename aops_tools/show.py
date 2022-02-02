from . import utils
from .config import CONFIG
from .utils import AOPS_URL, COLORS


def show_post_data(data, print_item, colors=COLORS[0]):
	for idx, _data in enumerate(data):
		post_time = utils.to_datetime(_data["post_time"])

		if print_item(
			idx,
			_data["username"],
			_data["thankers"],
			_data["thanks_received"],
			_data["post_number"]
		):
			utils.print_centered("Post", colors[0])
			info = [
				("Number", f"{_data['post_number']} ({_data['post_url']})"),
				("Posted by", f"{_data['username']} ({AOPS_URL}/community/user/{_data['poster_id']})"),
				("Posted at", post_time)
			]
			if _data["thankers"]:
				info.extend([
					("Like count", _data["thanks_received"]),
					("Liked by", _data["thankers"])
				])
			for prop in info:
				utils.print_wrapped(prop, colors[1])

			if canonical := _data["post_canonical"].strip():
				utils.print_post_content(canonical)

		if CONFIG["write-html"]:
			utils.write_html_file(
				_data["post_rendered"],
				f"Post #{_data['post_number']} by {_data['username']} at {post_time}",
				f"{_data['post_number']}.html"
			)

def show_view_posts_data(data, print_item, colors=COLORS[1]):
	for idx, _data in enumerate(data):
		post_data = _data["post_data"]

		if print_item(
			text := _data["item_text"].strip(),
			canonical := post_data["post_canonical"].strip()
		):
			utils.print_centered("Item", colors[0])
			info = []
			if post_data["post_type"] == "forum":
				info.append(("Index", f"{idx} ({post_data['post_url']})"))
			info.append(("Type", _data["item_type"]))
			if text:
				info.append(("Text", text))
			info.append(("Post type", post_data["post_type"]))
			for prop in info:
				utils.print_wrapped(prop, colors[1])

			if canonical and (
				CONFIG["brave"]
				or _data["item_type"] != "post_hidden"
			):
				utils.print_post_content(canonical)

		if CONFIG["write-html"]:
			title = f"Post #{idx}"
			if text:
				title += ": " + text
			utils.write_html_file(post_data["post_rendered"], title, f"{idx}.html")

def show_folder_data(data, print_item, colors=COLORS[0]):
	for idx, _data in enumerate(data):
		if print_item(
			text := _data["item_text"].strip(),
			subtitle := _data["item_subtitle"].strip()
		):
			utils.print_centered("Item", colors[0])
			info = [
				("Index", f"{idx} ({_data['item_url']})"),
				("Type", _data["item_type"])
			]
			if text:
				info.append(("Text", text))
			if subtitle:
				info.append(("Subtitle", subtitle))
			for prop in info:
				utils.print_wrapped(prop, colors[1])

def show_topic_data(data, stalk_users, find_posts, colors=COLORS[1]):
	utils.print_centered("Topic", colors[0])
	info = [
		("Link", data["topic_url"]),
		("Category", data["category_name"]),
		("Title", data["topic_title"].strip())
	]
	if CONFIG["brave"] and (tags := data["tags"]):
		info.append(("Tags", ", ".join(tag["tag_text"] for tag in tags)))
	if source := data["source"].strip():
		info.append(("Source", source))
	info.extend([
		("Post count", data["num_posts"]),
		("View count", data["num_views"])
	])
	for prop in info:
		utils.print_wrapped(prop, colors[1])

	print_item = lambda idx, username, thankers, thanks_received, num_post : (
		not CONFIG["silent"] and (
			CONFIG["verbose"]
			or idx == 0
			or utils.stalk_success(stalk_users, username, thankers, thanks_received)
			or (find_posts and num_post in find_posts)
	))

	show_post_data(data["posts_data"], print_item)

def show_category_data(data, find_text, colors=COLORS[1]):
	utils.print_centered("Category", colors[0])
	info = [
		("Link", data["category_url"]),
		("Name", data["category_name"])
	]
	if description := data["short_description"].strip():
		info.append(("Description", description))
	for prop in info:
		utils.print_wrapped(prop, colors[1])

	print_item = lambda str1, str2 : not CONFIG["silent"] and (
		CONFIG["verbose"] or (find_text and (
			find_text in str1 or find_text in str2
	)))

	if data["category_type"] == "view_posts":
		show_view_posts_data(data["items"], print_item)

	elif data["category_type"] == "folder":
		show_folder_data(data["items"], print_item)
