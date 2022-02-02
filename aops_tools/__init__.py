import colorama

from . import get, show, utils
from .config import CONFIG

__author__ = "Yohan Min"
__version__ = "3.0.0"

def show_aops_data(
	code,
	stalk_users=None,
	find_posts=None,
	search_method=None,
	find_text=None,
	write_files=False
):
	if write_files:
		CONFIG["write-html"] = CONFIG["write-json"] = True

	colorama.init()

	if "h" in code:
		data, begin_time = get.get_topic_data(code)
		if CONFIG["write-html"] or CONFIG["write-json"]:
			utils.create_path(data["category_id"], data["topic_id"])

		show.show_topic_data(data, stalk_users, find_posts)
		json_file = "topic-data.json"

	else:
		data, begin_time = get.get_category_data(code, search_method)
		if CONFIG["write-html"] or CONFIG["write-json"]:
			utils.create_path(data["category_id"])

		show.show_category_data(data, find_text)
		json_file = "category-data.json"

	if CONFIG["write-json"]:
		utils.write_json_file(data, json_file)

	utils.print_elapsed_time(begin_time)
