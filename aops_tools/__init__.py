from .extract import extract_topic_info
from bs4 import BeautifulSoup
import os

def show_topic_info(
	topic_code,
	verbose=False,
	silent=False,
	write_files=False,
	outdir="community",
	thanker_to_find=None,
	delim_cnt=80
):
	topic_dict = extract_topic_info(topic_code)
	topic_url = topic_dict["url"]
	topic_subject = topic_dict["subject"]
	topic_tags = topic_dict["tags"]
	topic_source = topic_dict["source"]
	topic_posts = topic_dict["posts"]

	topic_info = f"Topic url: {topic_url}\nSubject: {topic_subject}"
	if topic_tags:
		topic_info += f"\nTags: {', '.join(topic_tags)}"
	if topic_source:
		topic_info += f"\nSource: {topic_source}"
	if topic_posts:
		topic_info += f"\nPost count: {len(topic_posts)}"

	if verbose or not silent:
		print(topic_info)

	if write_files:
		topic_dir = os.path.join(outdir, topic_code)
		if not os.path.exists(topic_dir):
			os.makedirs(topic_dir)
		with open(os.path.join(topic_dir, "info.txt"), "w", encoding="utf8") as topic_info_file:
			topic_info_file.write(topic_info)

	if thanker_to_find:
		if verbose or not silent:
			print("-" * delim_cnt)
		print(f"Posts liked by {thanker_to_find}:")
		thanker_found = False

	for post_dict in topic_posts:
		post_number = post_dict["number"]
		post_url = post_dict["url"]
		post_username = post_dict["username"]
		post_user_profile = post_dict["user-profile"]
		post_date = post_dict["date"]
		post_edit_info = post_dict["edit-info"]
		post_thank_count = post_dict["thank-count"]
		post_thankers = post_dict["thankers"]
		post_html = post_dict["html"]

		post_info = f"""Post number: {post_number}
Post url: {post_url}
Username: {post_username}
User profile: {post_user_profile}
Date: {post_date}"""
		if post_edit_info:
			post_info += f"\nEdit info: {post_edit_info}"
		post_info += f"\nThank count: {post_thank_count}"
		if post_thankers:
			post_info += f"\nThankers: {', '.join(post_thankers)}"

		if verbose:
			print("-" * delim_cnt)
			print(post_info)

		if write_files:
			post_dir = os.path.join(topic_dir, post_number)
			if not os.path.exists(post_dir):
				os.makedirs(post_dir)

			with open(os.path.join(post_dir, "info.txt"), "w", encoding="utf8") as post_info_file:
				post_info_file.write(post_info)

			with open(os.path.join(post_dir, "content.html"), "w", encoding="utf8") as post_html_file:
				soup = BeautifulSoup(post_html, "lxml")
				for html_img in soup.find_all("img"):
					if html_img["src"].startswith("//"):
						html_img["src"] = "https:" + html_img["src"]
				html_head = soup.new_tag("head")
				html_style = soup.new_tag("style")
				html_style.string = """
body {
	line-height: 19px;
	font-family: Roboto, sans-serif;
	font-size: 15px;
	color: #333;
}

img.asy-image, img.latexcenter {
	display: block;
	margin: auto;
	padding: 1em 0;
	box-sizing: content-box;
	-moz-transform: rotate(0);
	max-width: 100%;
	height: auto;
}"""
				html_head.append(html_style)
				soup.find("body").insert_before(html_head)
				post_html_file.write(str(soup))

		if thanker_to_find and thanker_to_find in post_thankers:
			thanker_found = True
			print(f"Post #{post_number} ({post_url})")

	if thanker_to_find and not thanker_found:
		print("Not found")
