from .constants import *
from .extract import extract_topic_info
from bs4 import BeautifulSoup
import os
import json
import textwrap

def centered_text(text, textwidth, delim):
	diff = textwidth - len(text) - 2
	return delim * (diff // 2) + f" {text} " + delim * ((diff + 1) // 2)

def show_topic_info(
	topic_code,
	to_stalk={},
	to_find=[],
	verbose=False,
	silent=False,
	write_files=False,
	outdir="community",
	json_indent=2,
	delim_num=3,
	textwidth=95
):
	# Convert str to set and list
	if type(to_stalk) == str:
		to_stalk = {to_stalk}
	if type(to_find) == str:
		to_find = [to_find]

	# Extract topic properties
	topic_dict = extract_topic_info(topic_code)
	(
		topic_url,
		topic_subject,
		topic_tags,
		topic_source,
		topic_posts
	) = topic_dict.values()

	# Print topic properties
	if verbose or not silent:
		topic_info = [
			centered_text("TOPIC INFO", textwidth, "#"),
			f"Link: {topic_url}",
			f"Subject: {topic_subject}"
		]
		if topic_tags:
			topic_info.append(f"Tags: {', '.join(topic_tags)}")
		if topic_source:
			topic_info.append(f"Source: {topic_source}")
		if topic_posts:
			topic_info.append(f"Post count: {len(topic_posts)}")

		for prop in topic_info:
			print(textwrap.fill(prop, textwidth))

	# Write json file
	if write_files:
		topic_dir = os.path.join(outdir, topic_code)
		if not os.path.exists(topic_dir):
			os.makedirs(topic_dir)

		with open(os.path.join(topic_dir, "info.json"), "w", encoding="utf8") as json_file:
			json.dump(topic_dict, json_file, indent=json_indent)

	for post_number in topic_posts.keys():
		# Extract post properties
		(
			_,
			post_url,
			post_username,
			post_user_profile,
			post_date,
			post_edit_info,
			post_thank_count,
			post_thankers,
			post_html
		) = topic_posts[post_number].values()

		# Print post properties
		if (
			verbose
			# Post posted by user
			or post_username in to_stalk
			# Post liked by user(s)
			or set(post_thankers) & to_stalk
			# Post found by number
			or post_number in to_find
		):
			post_info = [
				centered_text("POST INFO", textwidth, "="),
				f"Post #{post_number}: {post_url}",
				f"Posted by: {post_username} ({post_user_profile})",
				f"Posted at: {post_date}"
			]
			if post_edit_info:
				post_info.append(f"Edit info: {post_edit_info}")
			if post_thankers:
				post_info.append(f"Liked by: {', '.join(post_thankers)}")
			post_info.append(centered_text("CONTENT", textwidth, "-"))

			# Modify post html
			soup = BeautifulSoup(post_html, "html.parser")

			for html_img in soup.find_all("img"):
				html_img.string = html_img["alt"]
				# TODO: display equations
				# if "latexcenter" in html_img["class"]:
				#   html_img.string = "\n" + html_img.string + "\n"
				html_img.unwrap()

			for html_quote in soup.find_all("div", attrs={"class": "bbcode_quote"}):
				html_quote.contents = html_quote.contents[1:-1]
				quote_body = html_quote.find("div", attrs={"class": "bbcode_quote_body"})
				quote_body.insert(0, QUOTE_BODY_DELIMS[0] * delim_num + "\n")
				quote_body.append("\n" + QUOTE_BODY_DELIMS[1] * delim_num)
				html_quote.unwrap()

			for hide_heading in soup.select(".cmty-hide-heading"):
				hide_heading.string = HIDE_HEADING_DELIMS[0] + hide_heading.string + HIDE_HEADING_DELIMS[1]
				hide_content = hide_heading.find_next("div", attrs={"class": "cmty-hide-content"})
				hide_content.insert(0, "\n" + HIDE_CONTENT_DELIMS[0] * delim_num + "\n")
				hide_content.append("\n" + HIDE_CONTENT_DELIMS[1] * delim_num)

			post_info.extend(soup.get_text().split("\n"))

			for prop in post_info:
				print(textwrap.fill(prop, textwidth))

		# Write html content
		if write_files:
			soup = BeautifulSoup(
f"""<!DOCTYPE html>
<html class="svg">
<head>
<meta charset="utf-8">
<meta name="viewport" content="initial-scale=1">
<title>Post #{post_number} by {post_username} at {post_date}</title>
<link rel="stylesheet" href="../../aops_tools/assets/aops.css">
<link rel="icon" href="https://artofproblemsolving.com/online-favicon.ico">
<script src="../../aops_tools/assets/aops.js"></script>
<script src="https://assets.artofproblemsolving.com/js/jquery.min.js"></script>
</head>
<body></body>
</html>""", "lxml")
			tmp = BeautifulSoup(post_html, "html.parser")
			for html_img in tmp.find_all("img"):
				img_src = html_img["src"]
				if img_src.startswith("//"):
					html_img["src"] = "https:" + img_src
				elif img_src.startswith("/"):
					html_img["src"] = AOPS_DOMAIN + img_src
			soup.find("body").append(tmp)

			with open(os.path.join(topic_dir, f"{post_number}.html"), "w", encoding="utf8") as html_file:
				html_file.write(str(soup))
