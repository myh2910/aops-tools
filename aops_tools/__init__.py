import colorama

from . import get, show, utils
from .config import CONFIG

__author__ = "Yohan Min"
__version__ = "3.4.2"


def show_aops_data(
    code,
    stalk_users=None,
    find_posts=None,
    search_method=None,
    find_text=None,
    **kwargs
):
    """Show data extracted from AoPS on the terminal.

    It is recommended to only extract an AoPS topic with 1000 or less posts, due
    to the time limit of the Selenium script execution.

    Args:
        code (str): Code of the AoPS category or topic. It will be automatically
        determined if the code belongs to a category or a topic.
        stalk_users (set of str): Users to stalk in this topic. If a user we
        want to stalk posted or liked a post from this topic, we will be
        notified.
        find_posts (list of int): Post numbers to find in this topic.
        search_method (list of str): Strings to be searched in this category. It
        will guide us to find a sequence of subcategories and subfolders
        containing those texts.
        find_text (str): Text to find in the items from this category.
    """
    for arg, value in kwargs.items():
        CONFIG[arg] = value

    if "write_files" in CONFIG and CONFIG["write_files"]:
        CONFIG["write_html"] = CONFIG["write_json"] = True

    colorama.init()

    json_file = None

    if "h" in code:
        data, begin_time = get.get_topic_data(code)

        if CONFIG["write_html"] or CONFIG["write_json"]:
            utils.create_path(data["category_id"], data["topic_id"])
            json_file = "topic-data.json"

        show.show_topic_data(data, stalk_users, find_posts)

    else:
        data, begin_time = get.get_category_data(code, search_method)

        if CONFIG["write_html"] or CONFIG["write_json"]:
            utils.create_path(data["category_id"])
            json_file = "category-data.json"

        show.show_category_data(data, find_text)

    if CONFIG["write_json"]:
        utils.write_json_file(data, json_file)

    utils.print_elapsed_time(begin_time)
