"""
The configuration used throughout the aops_tools module.

Notes
-----
In Windows, the `time_format` value should be "%b %#d, %Y, %#I:%M %p" instead.

"""
CONFIG = {
	'silent': False,
	'brave': False,
	'verbose': False,
	'textwidth': 100,
	'delim': "=",
	'category_script': "aops_tools/assets/category-script.js",
	'topic_script': "aops_tools/assets/topic-script.js",
	'loading_time': 1800,
	'outdir': "community",
	'write_html': False,
	'write_json': False,
	'num_indent': 2,
	'utc_offset': -5,
	'time_format': "%b %-d, %Y, %-I:%M %p"
}
