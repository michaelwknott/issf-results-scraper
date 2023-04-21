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


class ISSFScraper:
    """ISSF results scraper."""

    def __init__(self, url: str) -> None:
        self.url = url
        self.championships: list[dict[str, str]] = []
        self.years: list[dict[str, str]] = []
        self.cities: list[dict[str, str]] = []
        self.events: list[dict[str, str]] = []
        self.categories: list[dict[str, str]] = []
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()
        self.page.goto(self.url)

    def __del__(self):
        self.page.close()
        self.browser.close()

    def get_championship_options_html(self):
        self.page.locator(
            CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR + SELECTOR_SUFFIX
        ).is_enabled()
        championship_html = self.page.inner_html(CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR)
        self.championships = self._parse_html_option_tags(championship_html)

    def get_year_options_html(self, championship_value: str):
        self.page.reload(wait_until="domcontentloaded")
        self.page.locator(CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR).select_option(
            championship_value
        )
        self.page.locator(YEAR_DROPDOWN_CSS_SELECTOR + SELECTOR_SUFFIX).is_enabled()
        year_html = self.page.inner_html(YEAR_DROPDOWN_CSS_SELECTOR)
        self.years = self._parse_html_option_tags(year_html)

    def get_city_options_html(self, championship: str, year: str):
        # Using page.reload() as a workaround to ensure that CITY_DROPDOWN_CSS_SELECTOR
        # selects the updated city. Previously, the CITY_DROPDOWN_CSS_SELECTOR would
        # select the city from the previous championship selection.
        self.page.reload(wait_until="domcontentloaded")
        self.page.locator(CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR).select_option(
            championship
        )
        self.page.locator(YEAR_DROPDOWN_CSS_SELECTOR).select_option(year)

        self.page.locator(CITY_DROPDOWN_CSS_SELECTOR + SELECTOR_SUFFIX).is_enabled()

        city_html = self.page.inner_html(CITY_DROPDOWN_CSS_SELECTOR)
        self.cities = self._parse_html_option_tags(city_html)

    def get_event_options_html(self, championship: str, year: str, city: str):
        self.page.reload(wait_until="domcontentloaded")
        self.page.locator(CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR).select_option(
            championship
        )
        self.page.locator(YEAR_DROPDOWN_CSS_SELECTOR).select_option(year)
        self.page.locator(CITY_DROPDOWN_CSS_SELECTOR).select_option(city)

        self.page.locator(EVENT_DROPDOWN_CSS_SELECTOR + SELECTOR_SUFFIX).is_enabled()
        event_html = self.page.inner_html(EVENT_DROPDOWN_CSS_SELECTOR)
        self.events = self._parse_html_option_tags(event_html)

    def get_category_options_html(
        self, championship: str, year: str, city: str, event: str
    ):
        self.page.locator(CHAMPIONSHIP_DROPDOWN_CSS_SELECTOR).select_option(
            championship
        )
        self.page.locator(YEAR_DROPDOWN_CSS_SELECTOR).select_option(year)
        self.page.locator(CITY_DROPDOWN_CSS_SELECTOR).select_option(city)
        self.page.locator(EVENT_DROPDOWN_CSS_SELECTOR).select_option(event)
        self.page.locator(CATEGORY_DROPDOWN_CSS_SELECTOR + SELECTOR_SUFFIX).is_enabled()
        category_html = self.page.inner_html(CATEGORY_DROPDOWN_CSS_SELECTOR)
        self.categories = self._parse_html_option_tags(category_html)

    def _parse_html_option_tags(self, html_options_tags: str) -> list[dict[str, str]]:
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
    s = ISSFScraper(URL)
    s.get_championship_options_html()
    print(s.championships)
    print(s.championships)
    print(s.championships)
