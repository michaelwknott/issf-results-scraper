"""A script to scrape results data from the ISSF website.

ISSF results url:
https://www.issf-sports.org/competitions/results.ashx
"""

from typing import Sequence

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = "https://www.issf-sports.org/competitions/results.ashx"

CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR = (
    "#ctl00_cphMainContent_issfViewControler_ctl01_ctl00_dllchampionship"
)


def get_dropdown_options_html(css_selector: str) -> str:
    """ "
    Get the html of the dropdown option tags.
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
        )
        page = browser.new_page()

        page.goto(URL)
        dropdown_html_option_tags = page.inner_html(selector=css_selector)

        browser.close()

    return dropdown_html_option_tags


def parse_dropdown_options_html(html: str) -> Sequence[dict[str, str]]:
    """Parse the html of the dropdown option tags."""

    soup = BeautifulSoup(html, "html.parser")
    options = soup.find_all("option")

    options_data = []

    for option in options[1:]:  # Skip dropdown placeholder text
        option_data = {
            "value": option["value"],
            "text": option.text,
        }
        options_data.append(option_data)

    return options_data


if __name__ == "__main__":
    dropdown_options_html = get_dropdown_options_html(
        CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR
    )
    print(dropdown_options_html)
    options_data = parse_dropdown_options_html(dropdown_options_html)
    print(options_data)
