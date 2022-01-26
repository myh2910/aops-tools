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
	to_stalk=None,
	verbose=False,
	silent=False,
	write_files=False,
	outdir="community",
	json_indent=2,
	textwidth=95
):
	# Extract topic properties
	topic_dict = extract_topic_info(topic_code)
	topic_tags = topic_dict["tags"]
	topic_source = topic_dict["source"]
	topic_posts = topic_dict["posts"]

	topic_info = [
		centered_text("TOPIC INFO", textwidth, "#"),
		f"Link: {topic_dict['url']}",
		f"Subject: {topic_dict['subject']}"
	]
	if topic_tags:
		topic_info += [f"Tags: {', '.join(topic_tags)}"]
	if topic_source:
		topic_info += [f"Source: {topic_source}"]
	if topic_posts:
		topic_info += [f"Post count: {len(topic_posts)}"]

	# Print topic properties
	if verbose or not silent:
		for prop in topic_info:
			print(textwrap.fill(prop, textwidth))

	# Write json file
	if write_files:
		topic_dir = os.path.join(outdir, topic_code)
		if not os.path.exists(topic_dir):
			os.makedirs(topic_dir)

		with open(os.path.join(topic_dir, "info.json"), "w", encoding="utf8") as json_file:
			json.dump(topic_dict, json_file, indent=json_indent)

	for post_dict in topic_posts:
		# Extract post properties
		post_number = post_dict["number"]
		post_url = post_dict["url"]
		post_username = post_dict["username"]
		post_edit_info = post_dict["edit-info"]
		post_thankers = post_dict["thankers"]
		post_html = post_dict["html"]

		post_info = [
			centered_text("POST INFO", textwidth, "="),
			f"Post #{post_number}: {post_url}"
		]

		user_found = False
		if to_stalk:
			if to_stalk == post_username: # User posted this post
				user_found = True
				post_info[1] += f" (posted by {to_stalk})"
			elif to_stalk in post_thankers: # User liked this post
				user_found = True
				post_info[1] += f" (liked by {to_stalk})"

		if verbose or user_found:
			post_info += [
				f"Posted by: {post_username} ({post_dict['user-profile']})",
				f"Date posted: {post_dict['date']}"
			]
			if post_edit_info:
				post_info += [f"Edit info: {post_edit_info}"]
			if post_thankers:
				post_info += [f"Liked by: {', '.join(post_thankers)}"]

			post_info += [centered_text("CONTENT", textwidth, "-")]
			soup = BeautifulSoup(post_html, "lxml")
			for html_img in soup.find_all("img"):
				html_img.string = html_img["alt"]
				html_img.unwrap()
			post_info += soup.get_text().split("\n")

			# Print post properties
			for prop in post_info:
				print(textwrap.fill(prop, textwidth))

		# Write html content
		if write_files:
			soup = BeautifulSoup(
"""<!DOCTYPE html>
<html lang="en">
<head>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<link rel="stylesheet" href="../../aops_tools/aops.css">
</head>
</html>""", "lxml")
			temp = BeautifulSoup(post_html, "lxml")
			for html_img in temp.find_all("img"):
				if html_img["src"].startswith("//"):
					html_img["src"] = "https:" + html_img["src"]
			soup.find("head").insert_after(temp.find("body"))

			with open(os.path.join(topic_dir, f"{post_number}.html"), "w", encoding="utf8") as html_file:
				html_file.write(str(soup))
