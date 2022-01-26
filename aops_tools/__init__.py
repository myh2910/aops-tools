from .extract import extract_topic_info
import os
import json
import textwrap

def show_topic_info(
	topic_code,
	to_stalk=None,
	json_indent=2,
	textwidth=95,
	verbose=False,
	silent=False,
	write_files=False,
	outdir="community"
):
	# Extract topic properties
	topic_dict = extract_topic_info(topic_code)
	topic_tags = topic_dict["tags"]
	topic_source = topic_dict["source"]
	topic_posts = topic_dict["posts"]

	if verbose or not silent:
		print("=" * textwidth)
		topic_info = [
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
		for prop in topic_info:
			print(textwrap.fill(prop, textwidth))

	# Write topic properties
	if write_files:
		if not os.path.exists(outdir):
			os.mkdir(outdir)
		with open(os.path.join(outdir, f"{topic_code}.json"), "w", encoding="utf8") as json_file:
			json.dump(topic_dict, json_file, indent=json_indent)

	for post_dict in topic_posts:
		# Extract post properties
		post_number = post_dict["number"]
		post_url = post_dict["url"]
		post_username = post_dict["username"]
		post_edit_info = post_dict["edit-info"]
		post_thankers = post_dict["thankers"]

		post_info = [
			"-" * textwidth,
			f"Post #{post_number}: {post_url}",
		]
		# User posted this post
		if to_stalk and to_stalk == post_username:
			post_info[1] += f" (posted by {to_stalk})"
		# User liked this post
		elif to_stalk and to_stalk in post_thankers:
			post_info[1] += f" (liked by {to_stalk})"
		elif not verbose:
			continue
		post_info += [
			f"Posted by: {post_username} ({post_dict['user-profile']})",
			f"Date posted: {post_dict['date']}"
		]
		if post_edit_info:
			post_info += [f"Edit info: {post_edit_info}"]
		if post_thankers:
			post_info += [f"Liked by: {', '.join(post_thankers)}"]

		# Print post properties
		for prop in post_info:
			print(textwrap.fill(prop, textwidth))
