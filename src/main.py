import scraper as s
from database import DB_FILENAME, TABLE_COLUMNS, TABLE_NAME, DatabaseManager


def main():
    scraper = s.ISSFScraper(s.URL)
    db = DatabaseManager(DB_FILENAME)

    scraper.get_championship_options_html()
    print("Starting scraper...")

    for championship_option in scraper.championships:
        scraper.get_year_options_html(championship_option["value"])

        for year_option in scraper.years:
            scraper.get_city_options_html(
                championship_option["value"], year_option["value"]
            )

            for city_option in scraper.cities:
                scraper.get_event_options_html(
                    championship_option["value"],
                    year_option["value"],
                    city_option["value"],
                )

                for event_option in scraper.events:
                    scraper.get_category_options_html(
                        championship_option["value"],
                        year_option["value"],
                        city_option["value"],
                        event_option["value"],
                    )

                    for category_option in scraper.categories:
                        championship_values = (
                            championship_option["value"],
                            year_option["value"],
                            city_option["value"],
                            event_option["value"],
                            category_option["value"],
                        )
                        championship_id = " ".join(championship_values)

                        championship_record = {
                            "championship": championship_option["text"],
                            "year": year_option["text"],
                            "city": city_option["text"],
                            "event": event_option["text"],
                            "category": category_option["text"],
                            "id": championship_id,
                        }
                        db.create_table(table_name=TABLE_NAME, columns=TABLE_COLUMNS)
                        db.add(table_name=TABLE_NAME, data=championship_record)

                        print(f"{championship_record} added to database.")


if __name__ == "__main__":
    main()
