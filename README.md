# aops-tools

Extract data from the
[Art of Problem Solving](https://artofproblemsolving.com/community/) website
with [Python Selenium](https://pypi.org/project/selenium/), which can be
exported to JSON or HTML format. It first executes a JavaScript code and then
displays the result on the terminal.

The configuration file is located at [config.py](aops_tools/config.py), which
can be manually edited.

## Requirements

- `pip install -r requirements.txt`
- Install [ChromeDriver](https://chromedriver.chromium.org/downloads) and add it
  to PATH.

## Usage

```python
from aops_tools import show_aops_data

show_aops_data("c6h1671291", stalk_users={"mijail"})
show_aops_data("c6184h1061455", write_files=True)
show_aops_data("c6h2484456", verbose=True)
show_aops_data("c3838", find_text="windmill")
show_aops_data("c13", search_method=["National Olympiads", "All-Russian", "2021"], verbose=True)
show_aops_data("c3831", brave=True, verbose=True)
show_aops_data("c14", verbose=True)
```

Their outputs are located in the [assets](aops_tools/assets/) folder.
