"""
Functions that display data on the terminal.

"""
from . import utils
from .config import CONFIG
from .utils import COLORS


def show_post_data(posts_data, topic_title, print_item, colors=COLORS[0]):
	"""
	Show AoPS post data on the terminal.

	Parameters
	----------
	posts_data : list of dict
		Data of the posts to display.
	topic_title : str
		Topic title.
	print_item : function
		Determines if the data of a post will be displayed.
	colors : tuple of str and None, optional
		Title and post property name colors.
	"""
	if (utc_offset := CONFIG['utc_offset']) == 0:
		timezone = "UTC±00"
	elif utc_offset < 0:
		timezone = f"UTC-{-utc_offset:02}"
	else:
		timezone = f"UTC+{utc_offset:02}"

	for idx, data in enumerate(posts_data):
		post_time = f"{utils.to_datetime(data['post_time'])} ({timezone})"

		if print_item(
			idx,
			data['username'],
			data['thankers'],
			data['thanks_received'],
			data['post_number']
		):
			utils.print_centered("Post", colors[0])
			info = [
				("Number", f"{data['post_number']} ({data['post_url']})"),
				(
					"Posted by",
					f"{data['username']} ({utils.user_profile(data['poster_id'])})"
				),
				("Posted at", post_time)
			]
			if data['thankers']:
				info.extend([
					("Like count", data['thanks_received']),
					("Liked by", data['thankers'])
				])
			for prop in info:
				utils.print_wrapped(prop, colors[1])

			if canonical := data['post_canonical'].strip():
				utils.print_text(canonical)

		if CONFIG['write_html']:
			utils.write_html_file(data, topic_title, "topic", post_time=post_time)

def show_view_posts_data(items_data, category_name, print_item, colors=COLORS[1]):
	"""
	Show AoPS category (of type `view_posts`) data on the terminal.

	Parameters
	----------
	items_data : list of dict
		Data of the items to display.
	category_name : str
		Category name.
	print_item : function
		Determines if the data of an item will be displayed.
	colors : tuple of str and None, optional
		Title and property name colors.
	"""
	for idx, data in enumerate(items_data):
		post_data = data['post_data']

		if print_item(
			text := data['item_text'].strip(),
			canonical := post_data['post_canonical'].strip()
		):
			utils.print_centered("Item", colors[0])
			info = []
			if post_data['post_type'] == "forum":
				info.append(("Index", f"{idx} ({post_data['post_url']})"))
			info.append(("Type", data['item_type']))
			if text:
				info.append(("Text", text))
			info.append(("Post type", post_data['post_type']))
			for prop in info:
				utils.print_wrapped(prop, colors[1])

			if canonical and (
				CONFIG['brave']
				or data['item_type'] != "post_hidden"
			):
				utils.print_text(canonical)

		if CONFIG['write_html']:
			utils.write_html_file(data, category_name, "category", idx=idx)

def show_folder_data(items_data, print_item, colors=COLORS[0]):
	"""
	Show AoPS category (of type `folder`) data on the terminal.

	Parameters
	----------
	items_data : list of dict
		Data of the items to display.
	print_item : function
		Determines if the data of an item will be displayed.
	colors : tuple of str and None, optional
		Title and property name colors.
	"""
	for idx, data in enumerate(items_data):
		if print_item(
			text := data['item_text'].strip(),
			subtitle := data['item_subtitle'].strip()
		):
			utils.print_centered("Item", colors[0])
			info = [
				("Index", f"{idx} ({data['item_url']})"),
				("Type", data['item_type'])
			]
			if text:
				info.append(("Text", text))
			if subtitle:
				info.append(("Subtitle", subtitle))
			for prop in info:
				utils.print_wrapped(prop, colors[1])

def show_topic_data(data, stalk_users, find_posts, colors=COLORS[1]):
	"""
	Show AoPS topic data on the terminal.

	Parameters
	----------
	data : dict
		Topic data.
	stalk_users : set of str
		Users to stalk in this topic.
	find_posts : list of int
		Post numbers to find in this topic.
	colors : tuple of str and None, optional
		Title and property name colors.
	"""
	utils.print_centered('Topic', colors[0])
	info = [
		("Link", data['topic_url']),
		("Category", data['category_name']),
		("Title", data['topic_title'])
	]
	if CONFIG['brave'] and (tags := data['tags']):
		info.append(("Tags", ", ".join(tag['tag_text'] for tag in tags)))
	if source := data['source'].strip():
		info.append(("Source", source))
	info.extend([
		("Post count", data['num_posts']),
		("View count", data['num_views'])
	])
	for prop in info:
		utils.print_wrapped(prop, colors[1])

	print_item = lambda idx, username, thankers, thanks_received, num_post : (
		not CONFIG['silent'] and (
			CONFIG['verbose']
			or idx == 0
			or utils.stalk_success(stalk_users, username, thankers, thanks_received)
			or (find_posts and num_post in find_posts)
	))

	show_post_data(data['posts_data'], data['topic_title'], print_item)

def show_category_data(data, find_text, colors=COLORS[1]):
	"""
	Show AoPS category data on the terminal. An AoPS category consists of several
	types, where only the `view_posts` and `folder` types will be displayed.

	Parameters
	----------
	data : dict
		Category data.
	find_text : str
		Text to find in this category.
	colors : tuple of str and None, optional
		Title and property name colors.
	"""
	utils.print_centered("Category", colors[0])
	info = [
		("Link", data['category_url']),
		("Name", data['category_name'])
	]
	if description := data['short_description'].strip():
		info.append(("Description", description))
	for prop in info:
		utils.print_wrapped(prop, colors[1])

	print_item = lambda str1, str2 : not CONFIG['silent'] and (
		CONFIG['verbose'] or (find_text and (
			find_text in str1 or find_text in str2
	)))

	if data['category_type'] == "view_posts":
		show_view_posts_data(data['items'], data['category_name'], print_item)

	elif data['category_type'] == "folder":
		show_folder_data(data['items'], print_item)
