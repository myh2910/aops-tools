"""
Several functions defined for other modules.

"""
import json
import os
import textwrap
from datetime import datetime, timedelta
from timeit import default_timer

from colorama import Fore

from .config import CONFIG

AOPS_URL = "https://artofproblemsolving.com"

COLORS = [
	(Fore.BLUE, Fore.LIGHTBLUE_EX),
	(Fore.MAGENTA, Fore.LIGHTMAGENTA_EX),
	(Fore.CYAN, Fore.LIGHTCYAN_EX)
]

def aops_community(code):
	"""
	AoPS community link.

	Parameters
	----------
	code : str
		The code that follows after the community URL.

	Returns
	-------
	str
		AoPS community URL followed by `code`.
	"""
	return f"{AOPS_URL}/community/{code}"

def user_profile(user_id):
	"""
	AoPS user profile.

	Parameters
	----------
	user_id : int
		The user ID.

	Returns
	-------
	str
		The link of AoPS user profile.
	"""
	return f"{AOPS_URL}/community/user/{user_id}"

def print_centered(title, color=None):
	"""
	Print centered and colored text.

	Parameters
	----------
	title : str
		Text to display at the center.
	color : str or None, optional
		Title color.
	"""
	textwidth, delim = CONFIG['textwidth'], CONFIG['delim']

	if title:
		diff = textwidth - len(title) - 2
		text = f"{delim * (diff // 2)} {title} {delim * ((diff + 1) // 2)}"
	else:
		text = delim * textwidth

	if color:
		text = color + text + Fore.RESET

	print(text)

def print_wrapped(key_value, color=None):
	"""
	Print wrapped and colored text.

	Parameters
	----------
	key_value : tuple
		Property name and value.
	color : str or None, optional
		Property name color.
	"""
	key, value = key_value
	text = textwrap.fill(f"{key}: {value}", CONFIG['textwidth'])

	if color:
		idx = len(key) + 1
		text = color + text[:idx] + Fore.RESET + text[idx:]

	print(text)

def print_text(text, title="Content", color=Fore.GREEN):
	"""
	Print a text composed of several lines.

	Parameters
	----------
	text : str
		Text to display after the title.
	title : str, optional
		Title to display at the beginning.
	color : str or None, optional
		Title color.
	"""
	print_centered(title, color)
	for line in text.split("\n"):
		print(textwrap.fill(line, CONFIG['textwidth']))

def print_elapsed_time(start_time, colors=COLORS[2]):
	"""
	Print the elapsed time since the specified start time.

	Parameters
	----------
	start_time : float
		The start time of some running process.
	colors : tuple of str and None, optional
		Title and content colors.
	"""
	print_centered(None, colors[0])
	print_wrapped(
		("Elapsed time", f"{default_timer() - start_time:.2f} seconds"),
		colors[1]
	)

def hidden_thankers(num_hidden, all_hidden=False):
	"""
	Description of hidden thankers.

	Parameters
	----------
	num_hidden : int
		Number of hidden users who liked this post.
	all_hidden : bool, optional
		Indicates if all users who liked this post are hidden.

	Returns
	-------
	str
		Information about hidden users who liked this post.
	"""
	if all_hidden:
		if num_hidden == 1:
			return "1 user"
		return f"{num_hidden} users"
	if num_hidden == 1:
		return "and 1 other user"
	return f"and {num_hidden} other users"

def stalk_success(stalk_users, username, thankers, num_thanks):
	"""
	Indicate if a user we want to stalk is found.

	Parameters
	----------
	stalk_users : set
		Users to stalk in this post.
	username : str
		User who posted this post.
	thankers : str
		Description of the users who liked this post.
	num_thanks : int
		Number of likes this post received.

	Returns
	-------
	bool
		Indicates whether some of the users we want to stalk liked or posted this
		post.
	"""
	if not stalk_users:
		return False
	if username in stalk_users:
		return True
	if not thankers:
		return False

	hidden = (visible := thankers.split(","))[-1]
	if (num_visible := len(visible)) == 1:
		if hidden == hidden_thankers(num_thanks, True):
			return False
		if num_thanks > 1:
			return hidden[:-len(hidden_thankers(num_thanks - 1)) - 1] in stalk_users
	elif hidden == hidden_thankers(num_thanks - num_visible + 1):
		del visible[-1]
	return bool(stalk_users & set(visible))

def to_datetime(timestamp):
	"""
	Convert Unix time to UTC format.

	Parameters
	----------
	timestamp : int
		Unix timestamp.

	Returns
	-------
	str
		String representing the date and time corresponding to the Unix time.
	"""
	return (
		datetime.utcfromtimestamp(timestamp)
		+ timedelta(hours=CONFIG['utc_offset'])
	).strftime(CONFIG['time_format'])

def create_path(category_id, topic_id=None):
	"""
	Create the directory where the HTML and JSON files will be saved.

	Parameters
	----------
	category_id : int
		The category ID.
	topic_id : int, optional
		The topic ID.
	"""
	path = os.path.join(CONFIG['outdir'], f"c{category_id}")
	if topic_id:
		path = os.path.join(path, f"h{topic_id}")
	if not os.path.exists(path):
		os.makedirs(path)
	CONFIG['path'] = path

def write_json_file(data, filename):
	"""
	Export data to JSON file.

	Parameters
	----------
	data : dict
		Data to be exported.
	filename : str
		JSON file name.
	"""
	path = os.path.join(CONFIG['path'], filename)
	with open(path, "w", encoding="utf8") as file:
		json.dump(data, file, ensure_ascii=False, indent=CONFIG['num_indent'])

def write_html_file(data, title, filename):
	"""
	Export data to HTML file.

	Parameters
	----------
	data : str
		Data to be exported.
	title : str
		HTML document title.
	filename : str
		HTML file name.
	"""

	path = os.path.join(CONFIG['path'], filename)
	with open(path, "w", encoding="utf8") as file:
		file.write(
f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>{title}</title>
<link rel="icon" href="https://artofproblemsolving.com/online-favicon.ico">
<script src="https://assets.artofproblemsolving.com/js/jquery.min.js"></script>
</head>
<body style="padding: 10px; background: #fff;">
<div class="cmty-post-body">{data}</div>
<script src="../../../aops_tools/js/render.js"></script>
</body>
</html>"""
		)
