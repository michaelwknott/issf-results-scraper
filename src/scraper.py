"""A script to scrape results data from the ISSF website.

ISSF results url:
https://www.issf-sports.org/competitions/results.ashx
"""


from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL = "https://www.issf-sports.org/competitions/results.ashx"

CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR = (
    "#ctl00_cphMainContent_issfViewControler_ctl01_ctl00_dllchampionship"
)

YEAR_DROPDOWN_CSS_SELECTOR = (
    "#ctl00_cphMainContent_issfViewControler_ctl01_ctl00_dllyear"
)

CITY_DROPDOWN_CSS_SELECTOR = (
    "#ctl00_cphMainContent_issfViewControler_ctl01_ctl00_dllcity"
)

EVENT_DROPDOWN_CSS_SELECTOR = (
    "#ctl00_cphMainContent_issfViewControler_ctl01_ctl00_dllevent"
)

CATEGORY_DROPDOWN_CSS_SELECTOR = (
    "#ctl00_cphMainContent_issfViewControler_ctl01_ctl00_dllcategory"
)

# css selector suffix required to check if html element is enabled following selection
# concatenated with *_*_CSS_SELECTOR above
SELECTOR_SUFFIX = " > option:nth-child(2)"


def get_championship_options_html():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(URL)
        html_championship_option_tags = page.inner_html(
            CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR
        )

        browser.close()

    return html_championship_option_tags


def get_year_options_html(championship_value):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(URL)
        page.locator(CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR).select_option(
            championship_value
        )

        page.locator(YEAR_DROPDOWN_CSS_SELECTOR + SELECTOR_SUFFIX).is_enabled()
        html_year_option_tags = page.inner_html(YEAR_DROPDOWN_CSS_SELECTOR)

        browser.close()

    return html_year_option_tags


def get_city_options_html(championship, year):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(URL)

        page.locator(CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR).select_option(championship)
        page.locator(YEAR_DROPDOWN_CSS_SELECTOR).select_option(year)

        page.locator(CITY_DROPDOWN_CSS_SELECTOR + SELECTOR_SUFFIX).is_enabled()
        html_city_option_tags = page.inner_html(CITY_DROPDOWN_CSS_SELECTOR)

        browser.close()

        return html_city_option_tags


def get_event_options_html(championship, year, city):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(URL)

        page.locator(CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR).select_option(championship)
        page.locator(YEAR_DROPDOWN_CSS_SELECTOR).select_option(year)
        page.locator(CITY_DROPDOWN_CSS_SELECTOR).select_option(city)

        page.locator(EVENT_DROPDOWN_CSS_SELECTOR + SELECTOR_SUFFIX).is_enabled()
        html_event_option_tags = page.inner_html(EVENT_DROPDOWN_CSS_SELECTOR)

        browser.close()

        return html_event_option_tags


def get_category_options_html(championship, year, city, event):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(URL)

        page.locator(CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR).select_option(championship)
        page.locator(YEAR_DROPDOWN_CSS_SELECTOR).select_option(year)
        page.locator(CITY_DROPDOWN_CSS_SELECTOR).select_option(city)
        page.locator(EVENT_DROPDOWN_CSS_SELECTOR).select_option(event)

        page.locator(CATEGORY_DROPDOWN_CSS_SELECTOR + SELECTOR_SUFFIX).is_enabled()
        html_category_option_tags = page.inner_html(CATEGORY_DROPDOWN_CSS_SELECTOR)

        browser.close()

        return html_category_option_tags


def parse_html_option_tags(html_options_tags):
    soup = BeautifulSoup(html_options_tags, "html.parser")
    options = soup.find_all("option")

    options_tags = []

    for option in options[1:]:
        option_data = {
            "value": option["value"],
            "text": option.text,
        }
        options_tags.append(option_data)

    return options_tags


if __name__ == "__main__":
    dropdown_options_html = get_championship_options_html()
    print(dropdown_options_html)
    options_data = parse_html_option_tags(dropdown_options_html)
    print(options_data)
