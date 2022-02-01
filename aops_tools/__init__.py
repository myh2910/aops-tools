from .show import show_topic_data, show_category_data

__author__ = "Yohan Min"
__version__ = "2.2"

def show_aops_data(
	code,
	stalk_users=None,
	find_posts=None,
	search_method=None,
	find_text=None,
	silent=False,
	brave=False,
	verbose=False,
	write_files=False,
	write_json=False,
	write_html=False,
	outdir="community",
	num_indent=2,
	textwidth=95,
	delim="=",
	utc_offset=-5,
	time_format="%b %-d, %Y, %-I:%M %p"
):
	if "h" in code:
		show_topic_data(
			code,
			stalk_users,
			find_posts,
			silent,
			brave,
			verbose,
			write_files,
			write_json,
			write_html,
			outdir,
			num_indent,
			textwidth,
			delim,
			utc_offset,
			time_format
		)
	else:
		show_category_data(
			code,
			search_method,
			find_text,
			silent,
			brave,
			verbose,
			write_files,
			write_json,
			write_html,
			outdir,
			num_indent,
			textwidth,
			delim
		)
