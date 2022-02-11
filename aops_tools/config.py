"""
The configuration file for the `aops_tools` module.

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
	'time_format': {
		'Windows': "%b %#d, %Y, %#I:%M %p",
		'Linux': "%b %-d, %Y, %-I:%M %p"
	}
}
