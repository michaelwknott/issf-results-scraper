import scraper


def main():
    html_championship_options = scraper.get_championship_options_html()

    championship_options = scraper.parse_html_option_tags(html_championship_options)

    print(
        f"The following championship dropdown options have been scraped:\n"
        f"{championship_options}\n"
    )

    for championship_option in championship_options:
        html_year_options = scraper.get_year_options_html(championship_option["value"])

        year_options = scraper.parse_html_option_tags(html_year_options)
        print(
            f"The following year dropdown options have been scraped:\n"
            f"{year_options}\n"
        )

        for year_option in year_options:
            html_city_options = scraper.get_city_options_html(
                championship_option["value"], year_option["value"]
            )

            city_options = scraper.parse_html_option_tags(html_city_options)
            print(
                f"The following city dropdown options have been scraped:\n"
                f"{city_options}\n"
            )

            for city_option in city_options:
                html_event_options = scraper.get_event_options_html(
                    championship_option["value"],
                    year_option["value"],
                    city_option["value"],
                )

                event_options = scraper.parse_html_option_tags(html_event_options)
                if event_options:
                    print(
                        f"The following event dropdown options have been scraped:\n"
                        f"{event_options}\n"
                    )
                else:
                    print(
                        "The following event dropdown options have been scraped:\n"
                        "No required events\n"
                    )

                for event_option in event_options:
                    html_category_options = scraper.get_category_options_html(
                        championship_option["value"],
                        year_option["value"],
                        city_option["value"],
                        event_option["value"],
                    )

                    category_options = scraper.parse_html_option_tags(
                        html_category_options
                    )

                    print(
                        f"The following category dropdown options have been scraped:\n"
                        f"{category_options}\n"
                    )

                    for category_option in category_options:
                        championship_info = [
                            championship_option,
                            year_option,
                            city_option,
                            event_option,
                            category_option,
                        ]
                        print(championship_info)


if __name__ == "__main__":
    main()
