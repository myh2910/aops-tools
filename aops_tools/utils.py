from colorama import Fore
from datetime import datetime, timedelta

# AoPS links
aops_url = "https://artofproblemsolving.com"

def user_profile(poster_id):
	return f"{aops_url}/community/user/{poster_id}"

# Print colored text
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
GREEN = Fore.GREEN
YELLOW = Fore.LIGHTYELLOW_EX
CYAN = Fore.CYAN

def print_centered(text, textwidth, delim, color):
	diff = textwidth - len(text) - 2
	print(color + delim * (diff // 2), text, delim * ((diff + 1) // 2) + Fore.RESET)

def print_wrapped(text, width, color):
	print(color + text[:width + 1] + Fore.RESET + text[width + 1:])

# Convert to datetime
def to_datetime(time, utc_offset, time_format):
	if utc_offset == 0:
		timezone = "UTC±00"
	elif utc_offset < 0:
		timezone = f"UTC-{-utc_offset:02}"
	else:
		timezone = f"UTC+{utc_offset:02}"
	return (datetime.utcfromtimestamp(time) + timedelta(hours=utc_offset)
		).strftime(time_format + f" ({timezone})")
