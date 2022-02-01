import json
import os
import textwrap
from datetime import datetime, timedelta
from timeit import default_timer
from bs4 import BeautifulSoup
from colorama import Fore

aops_url = "https://artofproblemsolving.com"

def print_centered(text, textwidth, delim, color):
	if text:
		diff = textwidth - len(text) - 2
		print(
			color + delim * (diff // 2),
			text,
			delim * ((diff + 1) // 2) + Fore.RESET
		)
	else:
		print(color + delim * textwidth + Fore.RESET)

def print_wrapped(key, value, textwidth, color):
	text = textwrap.fill(f"{key}: {value}", textwidth)
	idx = len(key) + 1
	print(color + text[:idx] + Fore.RESET + text[idx:])

def print_post(content, textwidth, delim):
	print_centered("Content", textwidth, delim, Fore.GREEN)
	for line in content.split("\n"):
		print(textwrap.fill(line, textwidth))

def print_elapsed_time(begin_time, textwidth, delim):
	print_centered(None, textwidth, delim, Fore.CYAN)
	print_wrapped(
		"Elapsed time",
		f"{default_timer() - begin_time:.2f} seconds",
		textwidth,
		Fore.LIGHTCYAN_EX
	)

def print_dict_list(dict_lst, titles, keys, textwidth):
	t0, t1, t2 = titles
	k1, k2 = keys
	l0, l1 = max(len(t0), len(str(len(dict_lst) - 1))), len(t1)
	for dct in dict_lst:
		l1 = max(l1, len(str(dct[k1])))
	e1 = l0 + l1 + 5
	e2 = textwidth - e1

	print(f" {t0.ljust(l0)}  {t1.ljust(l1)}  {t2}")
	print(f" {'--'.ljust(l0)}  {'--'.ljust(l1)}  --")

	for idx, dct in enumerate(dict_lst):
		if s2 := dct[k2]:
			s1 = f" {str(idx).ljust(l0)}  {dct[k1].ljust(l1)}  "
			if len(s2) > e2:
				print(s1, end="")
				for idx, p2 in enumerate(textwrap.fill(s2, e2).split("\n")):
					if idx > 0:
						print(" " * e1, end="")
					print(p2)
			else:
				print(s1 + s2)
		else:
			print(f" {str(idx).ljust(l0)}  {dct[k1]}")

def to_datetime(time, utc_offset, time_format):
	if utc_offset == 0:
		timezone = "UTC±00"
	elif utc_offset < 0:
		timezone = f"UTC-{-utc_offset:02}"
	else:
		timezone = f"UTC+{utc_offset:02}"
	return (datetime.utcfromtimestamp(time) + timedelta(hours=utc_offset)
		).strftime(time_format + f" ({timezone})")

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

def write_json_file(
	json_data, num_indent, outdir, stem, write_files,
	write_json, write_html, category_id, topic_id=None
):
	if write_files:
		write_json, write_html = True, True

	path = None
	if write_html or write_json:
		path = os.path.join(outdir, f"c{category_id}")
		if topic_id:
			path = os.path.join(path, f"h{topic_id}")
		if not os.path.exists(path):
			os.makedirs(path)

	if write_json:
		with open(
			os.path.join(path, f"{stem}.json"), "w", encoding="utf8"
		) as json_file:
			json.dump(json_data, json_file, ensure_ascii=False, indent=num_indent)

	return write_html, path

def write_html_file(html_data, html_title, path, stem):
	tmp = BeautifulSoup(html_data, "html.parser")
	for img in tmp.find_all("img"):
		if (src := img["scr"]).startswith("//"):
			img["src"] = "https:" + src
		elif src.startswith("/"):
			img["src"] = aops_url + src

	soup = BeautifulSoup(
f"""<!DOCTYPE html>
<html class="svg">
<head>
<meta charset="utf-8">
<meta name="viewport" content="initial-scale=1">
<title>{html_title}</title>
<link rel="stylesheet" href="../../../aops_tools/assets/aops.css">
<link rel="icon" href="https://artofproblemsolving.com/online-favicon.ico">
<script src="../../../aops_tools/assets/aops.js"></script>
<script src="https://assets.artofproblemsolving.com/js/jquery.min.js"></script>
</head>
<body></body>
</html>""", "lxml")
	soup.find("body").append(tmp)

	with open(
		os.path.join(path, f"{stem}.html"), "w", encoding="utf8"
	) as html_file:
		html_file.write(str(soup))
