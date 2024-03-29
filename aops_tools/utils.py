import json
import os
import platform
import textwrap
import warnings
from datetime import datetime, timedelta
from timeit import default_timer

from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from colorama import Fore

from .config import CONFIG

AOPS_URL = "https://artofproblemsolving.com%s"
COMMUNITY_URL = AOPS_URL % "/community/%s"
PROFILE_URL = AOPS_URL % "/community/user/%d"

COLORS = [
    (Fore.BLUE, Fore.LIGHTBLUE_EX),
    (Fore.MAGENTA, Fore.LIGHTMAGENTA_EX),
    (Fore.CYAN, Fore.LIGHTCYAN_EX),
]


def print_centered(title, color=None):
    """Print centered and colored text.

    Args:
        title (str): Text to display at the center.
        color (str or None): Title color.
    """
    textwidth, delim = CONFIG["textwidth"], CONFIG["delim"]

    if title:
        diff = textwidth - len(title) - 2
        text = f"{delim * (diff // 2)} {title} {delim * ((diff + 1) // 2)}"
    else:
        text = delim * textwidth

    if color:
        text = color + text + Fore.RESET

    print(text)


def print_wrapped(key_value, color=None):
    """Print wrapped and colored text.

    Args:
        key_value (tuple): Property name and value.
        color (str or None): Property name color.
    """
    key, value = key_value
    text = textwrap.fill(f"{key}: {value}", CONFIG["textwidth"])

    if color:
        idx = len(key) + 1
        text = color + text[:idx] + Fore.RESET + text[idx:]

    print(text)


def print_text(text, title="Content", color=Fore.GREEN):
    """Print a text composed of several lines.

    Args:
        text (str): Text to display after the title.
        title (str): Title to display at the beginning.
        color (str or None): Title color.
    """
    print_centered(title, color)
    for line in text.split("\n"):
        print(textwrap.fill(line, CONFIG["textwidth"]))


def print_elapsed_time(start_time, colors=COLORS[2]):
    """Print the elapsed time since the specified start time.

    Args:
        start_time (float): The start time of some running process.
        colors (tuple of str and None): Title and content colors.
    """
    print_centered(None, colors[0])
    print_wrapped(
        ("Elapsed time", f"{default_timer() - start_time:.2f} seconds"), colors[1]
    )


def hidden_thankers(num_hidden, all_hidden=False):
    """Description of hidden thankers.

    Args:
        num_hidden (int): Number of hidden users who liked this post.
        all_hidden (bool): Indicates if all users who liked this post are
        hidden.

    Returns:
        str: Information about hidden users who liked this post.
    """
    if all_hidden:
        if num_hidden == 1:
            return "1 user"
        return f"{num_hidden} users"
    if num_hidden == 1:
        return "and 1 other user"
    return f"and {num_hidden} other users"


def stalk_success(stalk_users, username, thankers, num_thanks):
    """Indicate if a user we want to stalk is found.

    Args:
        stalk_users (set): Users to stalk in this post.
        username (str): User who posted this post.
        thankers (str): Description of the users who liked this post.
        num_thanks (int): Number of likes this post received.

    Returns:
        bool: Indicates whether some of the users we want to stalk liked or
        posted this post.
    """
    if not stalk_users:
        return False
    if username in stalk_users:
        return True
    if not thankers:
        return False

    hidden = (visible := thankers.split(", "))[-1]
    if (num_visible := len(visible)) == 1:
        if hidden == hidden_thankers(num_thanks, True):
            return False
        if num_thanks > 1:
            return hidden[: -len(hidden_thankers(num_thanks - 1)) - 1] in stalk_users
    elif hidden == hidden_thankers(num_thanks - num_visible + 1):
        del visible[-1]
    return bool(stalk_users & set(visible))


def to_datetime(timestamp):
    """Convert Unix time to UTC format.

    Args:
        timestamp (int): Unix timestamp.

    Returns:
        str: String representing the date and time corresponding to the Unix
        time.
    """
    return (
        datetime.utcfromtimestamp(timestamp) + timedelta(hours=CONFIG["utc_offset"])
    ).strftime(CONFIG["time_format"][platform.system()])


def create_path(category_id, topic_id=None):
    """Create the directory where the HTML and JSON files will be saved.

    Args:
        category_id (int): The category ID.
        topic_id (int): The topic ID.
    """
    path = os.path.join(CONFIG["outdir"], f"c{category_id}")
    if topic_id:
        path = os.path.join(path, f"h{topic_id}")
    if not os.path.exists(path):
        os.makedirs(path)
    CONFIG["path"] = path


def write_json_file(data, filename):
    """Export data to JSON file.

    Args:
        data (dict): Data to be exported.
        filename (str): JSON file name.
    """
    path = os.path.join(CONFIG["path"], filename)
    with open(path, "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=CONFIG["num_indent"])


def sanitize_html(post_rendered):
    """Sanitize HTML.

    Args:
        post_rendered (str): Original post HTML content.

    Returns:
        str
    """
    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

    soup = BeautifulSoup(post_rendered, "html.parser")
    for img in soup.find_all("img"):
        url = img["src"]
        if url.startswith("//"):
            img["src"] = f"https:{url}"
        elif url.startswith("/"):
            img["src"] = AOPS_URL % url
    return str(soup)


def topic_html(data, post_time):
    """Export topic post to HTML.

    Args:
        data (dict): Data to be exported.
        post_time (str): Posted time.

    Returns:
        content (str): HTML content of the post.
    """
    if (num_posts := data["num_posts"]) == 1:
        num_posts = "1 post"
    else:
        num_posts = f"{num_posts} posts"

    content = f"""<div class="cmty-post-wrapper">
<div class="cmty-post-tr">
<div class="cmty-post-left">
<a title="{data['username']}\nClick to view user profile." href="{PROFILE_URL % data['poster_id']}">
<img class="cmty-avatar no-print" src="https:{data['avatar']}" width="80" height="80">
</a>
<div class="cmty-post-username">
<a title="{data['username']}\nClick to view user profile." href="{PROFILE_URL % data['poster_id']}">{data['username']}</a>
</div>
<div class="cmty-post-num-posts">{num_posts}</div>
</div>
<div class="cmty-post-middle">
<div class="cmty-post-top-inline cmty-post-top-data">
<div class="cmty-post-top">
<a title="Get Post URL" class="cmty-post-number clickable" href="{data['post_url']}">#{data['post_number']}</a>
<span class="cmty-pm-from-post"><span><span class="aops-font">V</span>PM</span></span>
<span class="cmty-post-date">{post_time}</span>"""
    if data["thanks_received"]:
        content += f"""
<span class="cmty-post-thank-count"> • {data['thanks_received']} <span class="aops-font">Y</span></span>"""
    content += f"""
</div>
</div>
<div class="cmty-post-body">{sanitize_html(data['post_rendered'])}</div>
</div>
<div class="cmty-post-right no-print">
<span title="Report post" class="cmty-post-report aops-font">Z</span>
<span title="Quote this post in a reply" class="cmty-post-quote aops-font">K</span>
<span class="cmty-post-thank aops-font" title="Give thumbs up">Y</span>
</div>
</div>
</div>"""
    return content


def category_html(data):
    """Export category item to HTML.

    Args:
        data (dict): Data to be exported.

    Returns:
        str: HTML content of the category item.
    """
    post_data = data["post_data"]
    post_rendered = sanitize_html(post_data["post_rendered"])
    content = """<div id="main-content">"""

    if data["item_type"] == "post":
        if post_data["post_type"] == "forum":
            content += f"""
<div class="cmty-view-posts-item cmty-view-post-item-w-label cmty-vp-both">
<div class="cmty-view-post-item-label">{data['item_text']}</div>
<div class="cmty-view-post-item-text">{post_rendered}</div>"""
        else:
            content += f"""
<div class="cmty-view-posts-item cmty-view-post-item-w-label cmty-vp-left">
<div class="cmty-view-post-item-label">{data['item_text']}</div>
<div class="cmty-view-post-item-text">{post_rendered}</div>"""
    else:
        content += f"""
<div class="cmty-view-posts-item cmty-vp-both">
<div class="cmty-view-post-item-label"></div>
<div class="cmty-view-post-item-text">
<div class="cmty-post-item-hidden-bar">{data['item_text']}</div>
<div class="cmty-post-item-hidden-content">{post_rendered}</div>
</div>"""

    if post_data["post_type"] == "forum":
        content += f"""
<div class="cmty-view-post-poster">
<div class="cmty-view-post-poster-avatar">
<img class="cmty-avatar" src="https:{post_data['poster_avatar']}" width="30" height="30">
</div>
<div class="cmty-view-post-poster-username">{post_data['username']}</div>
<div class="cmty-view-post-topic-link">
<a href="{post_data['post_url']}">view topic</a>
</div>
</div>"""

    content += """
</div>
</div>"""
    return content


def write_html_file(data, title, data_type, post_time=None, idx=None):
    """Export data to HTML file.

    Args:
        data (str): Data to be exported.
        title (str): HTML document title.
        date_type (str): Type of the data.
        post_time (str or None)
        idx (int or None)
    """
    if data_type == "category":
        path = os.path.join(CONFIG["path"], f"{idx}.html")
        master = "../.."
        content = category_html(data)
    else:
        path = os.path.join(CONFIG["path"], f"{data['post_number']}.html")
        master = "../../.."
        content = topic_html(data, post_time)

    with open(path, "w", encoding="utf8") as file:
        file.write(
            f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>{title}</title>
<link rel="icon" href="https://artofproblemsolving.com/online-favicon.ico">
<link rel="stylesheet" href="{master}/aops_tools/css/aops-style.css">
</head>
<body>
{content}
<script src="{master}/aops_tools/js/jquery.min.js"></script>
<script src="{master}/aops_tools/js/aops-utils.js"></script>
</body>
</html>"""
        )
