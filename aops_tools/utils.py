import json
import os
import textwrap
from datetime import datetime, timedelta
from timeit import default_timer

from bs4 import BeautifulSoup
from colorama import Fore

from .config import CONFIG

AOPS_URL = "https://artofproblemsolving.com"

COLORS = [
	(Fore.BLUE, Fore.LIGHTBLUE_EX),
	(Fore.MAGENTA, Fore.LIGHTMAGENTA_EX)
]

def print_centered(text, color):
	textwidth, delim = CONFIG["textwidth"], CONFIG["delim"]
	if text:
		diff = textwidth - len(text) - 2
		print(
			color + delim * (diff // 2),
			text,
			delim * ((diff + 1) // 2) + Fore.RESET
		)
	else:
		print(color + delim * textwidth + Fore.RESET)

def print_wrapped(values, color):
	text = textwrap.fill(f"{values[0]}: {values[1]}", CONFIG["textwidth"])
	idx = len(values[0]) + 1
	print(color + text[:idx] + Fore.RESET + text[idx:])

def print_post_content(content):
	print_centered("Content", Fore.GREEN)
	for line in content.split("\n"):
		print(textwrap.fill(line, CONFIG["textwidth"]))

def print_elapsed_time(begin_time):
	print_centered(None, Fore.CYAN)
	print_wrapped(
		("Elapsed time", f"{default_timer() - begin_time:.2f} seconds"),
		Fore.LIGHTCYAN_EX
	)

def hidden_thankers(num_hidden, all_hidden=False):
	if all_hidden:
		if num_hidden == 1:
			return "1 user"
		return f"{num_hidden} users"
	if num_hidden == 1:
		return "and 1 other user"
	return f"and {num_hidden} other users"

def stalk_success(stalk_users, username, thankers, num_thanks):
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
	return stalk_users & set(visible)

def to_datetime(time):
	if (utc_offset := CONFIG["utc-offset"]) == 0:
		timezone = "UTC±00"
	elif utc_offset < 0:
		timezone = f"UTC-{-utc_offset:02}"
	else:
		timezone = f"UTC+{utc_offset:02}"
	return (
		datetime.utcfromtimestamp(time) + timedelta(hours=utc_offset)
	).strftime(CONFIG["time-format"] + f" ({timezone})")

def create_path(category_id, topic_id=None):
	path = os.path.join(CONFIG["outdir"], f"c{category_id}")
	if topic_id:
		path = os.path.join(path, f"h{topic_id}")
	if not os.path.exists(path):
		os.makedirs(path)
	CONFIG["path"] = path

def write_json_file(data, name):
	with open(os.path.join(CONFIG["path"], name), "w", encoding="utf8") as file:
		json.dump(data, file, ensure_ascii=False, indent=CONFIG["num-indent"])

def write_html_file(data, title, name):
	tmp = BeautifulSoup(data, "html.parser")
	for img in tmp.find_all("img"):
		if (src := img["scr"]).startswith("//"):
			img["src"] = "https:" + src
		elif src.startswith("/"):
			img["src"] = AOPS_URL + src

	soup = BeautifulSoup(
f"""<!DOCTYPE html>
<html class="svg">
<head>
<meta charset="utf-8">
<meta name="viewport" content="initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../../../aops_tools/assets/aops.css">
<link rel="icon" href="https://artofproblemsolving.com/online-favicon.ico">
<script src="../../../aops_tools/assets/aops.js"></script>
<script src="https://assets.artofproblemsolving.com/js/jquery.min.js"></script>
</head>
<body></body>
</html>""", "lxml")
	soup.find("body").append(tmp)

	with open(os.path.join(CONFIG["path"], name), "w", encoding="utf8") as file:
		file.write(str(soup))
