import platform
import textwrap
from timeit import default_timer

from selenium import webdriver
from selenium_stealth import stealth

from .config import CONFIG
from .utils import COMMUNITY_URL


def print_data_as_table(
    data, titles=("Index", "Text", "Description"), keys=("item_text", "item_subtitle")
):
    """Print data in table form.

    Args:
        data (list of dict): Data of the items to display as a table.
        titles (tuple of str): Headers of the table.
        keys (tuple of str): Property names of the items to display.
    """
    lens = [max(len(titles[0]), len(str(len(data) - 1))), len(titles[1])]
    for dct in data:
        lens[1] = max(lens[1], len(str(dct[keys[0]])))
    spaces = [(space := sum(lens) + 5), CONFIG["textwidth"] - space]

    print(f" {titles[0].ljust(lens[0])}  {titles[1].ljust(lens[1])}  {titles[2]}")
    print(f" {'--'.ljust(lens[0])}  {'--'.ljust(lens[1])}  --")

    for i, dct in enumerate(data):
        if str2 := dct[keys[1]]:
            str1 = f" {str(i).ljust(lens[0])}  {dct[keys[0]].ljust(lens[1])}  "
            if len(str2) > spaces[1]:
                print(str1, end="")
                for j, str3 in enumerate(textwrap.fill(str2, spaces[1]).split("\n")):
                    if j > 0:
                        print(" " * spaces[0], end="")
                    print(str3)
            else:
                print(str1 + str2)
        else:
            print(f" {str(i).ljust(lens[0])}  {dct[keys[0]]}")


def get_webdriver():
    """Selenium WebDriver.

    We use `selenium-stealth` to prevent possible detections.

    Returns:
        WebDriver: The Selenium WebDriver object.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    if platform.system() == "Windows":
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options)
    driver.set_script_timeout(CONFIG["loading_time"])

    stealth(driver, platform="Win32", fix_hairline=True)
    return driver


def get_topic_data(code):
    """Extract data from AoPS topic.

    Args:
        code (str): Topic code in the format "c" + category_id + "h" + topic_id.

    Returns:
        tuple of dict and float: Data extracted from AoPS topic and the starting
        time.
    """
    start_time = default_timer()
    print(":: Extracting topic data...")

    with open(CONFIG["topic_script"], "r", encoding="utf8") as file:
        script = file.read()

    driver = get_webdriver()
    driver.get(COMMUNITY_URL % code)
    data = driver.execute_script(script)
    driver.quit()

    return data, start_time


def get_category_data(code, search_method=None):
    """Extract data from AoPS category.

    Args:
        code (str): Category code in the format "c" + category_id.
        search_method (list of str): Strings to be searched in this category.

    Returns:
        tuple of dict and float: Data extracted from AoPS category and the
        starting time.
    """
    start_time = default_timer()
    print(":: Extracting category data...")

    with open(CONFIG["category_script"], "r", encoding="utf8") as file:
        script = file.read()

    driver = get_webdriver()
    driver.get(COMMUNITY_URL % code)
    data = driver.execute_script(script)

    while data["category_type"] == "folder":
        search_success = False
        if search_method:
            if text := search_method[0].strip():
                for item_data in data["items"]:
                    if (
                        text in item_data["item_text"]
                        or text in item_data["item_subtitle"]
                    ):
                        driver.get(COMMUNITY_URL % f"c{item_data['item_id']}")
                        data = driver.execute_script(script)
                        search_success = True
                        break
            del search_method[0]

        if search_success:
            continue

        start_time -= default_timer()
        go_deeper = input(":: This is a folder. Do you want to explore? [y/N] ")
        start_time += default_timer()

        if go_deeper not in ["y", "Y"]:
            break

        print_data_as_table(data["items"])

        start_time -= default_timer()
        idx = input(":: Select item index [default: 0] ")
        start_time += default_timer()

        if idx:
            idx = int(idx)
        else:
            idx = 0

        driver.get(COMMUNITY_URL % f"c{data['items'][idx]['item_id']}")
        data = driver.execute_script(script)

    driver.quit()

    return data, start_time
