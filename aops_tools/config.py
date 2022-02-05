"""
The configuration used throughout the `aops_tools` module.

Notes
-----
On Windows, some time format specifiers are different than on Linux, so be
aware of this. (e.g. `%-d` to `%#d`, `%-I` to `%#I`, etc.)

"""
CONFIG = {
	'silent': False,
	'brave': False,
	'verbose': False,
	'textwidth': 100,
	'delim': "=",
	'category_script': "aops_tools/js/aops-category.js",
	'topic_script': "aops_tools/js/aops-topic.js",
	'loading_time': 1200,
	'outdir': "community",
	'write_html': False,
	'write_json': False,
	'num_indent': 2,
	'utc_offset': -5,
	'time_format': "%b %-d, %Y, %-I:%M %p"
}
