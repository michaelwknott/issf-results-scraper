import logging
import logging.config

import yaml

import scraper as s
from database import DB_FILENAME, TABLE_COLUMNS, TABLE_NAME, DatabaseManager


def main() -> None:
    # Logging
    with open("logging_config.yaml", "r") as f:
        config = yaml.safe_load(f.read())

    logging.config.dictConfig(config)
    logger = logging.getLogger("issf_scraper")

    # Scraper
    scraper = s.ISSFScraper(s.URL)

    # Database
    db = DatabaseManager(DB_FILENAME)
    db.create_table(table_name=TABLE_NAME, columns=TABLE_COLUMNS)

    print("Starting scraper...")
    logger.info("Starting scraper.")

    scraper.get_championship_options_html()

    for championship_option in scraper.championships:
        logger.info(f"Current championship: {championship_option['text']}.")

        scraper.get_year_options_html(championship_option["value"])

        for year_option in scraper.years:
            logger.info(
                f"Current championship {championship_option['text']}, "
                f"Current year: {year_option['text']}."
            )

            scraper.get_city_options_html(
                championship_option["value"], year_option["value"]
            )

            for city_option in scraper.cities:
                logger.info(
                    f"Current championship {championship_option['text']}, "
                    f"Current year: {year_option['text']}, "
                    f"Current city: {city_option['text']}."
                )

                scraper.get_event_options_html(
                    championship_option["value"],
                    year_option["value"],
                    city_option["value"],
                )

                for event_option in scraper.events:
                    logger.info(
                        f"Current championship {championship_option['text']}, "
                        f"Current year: {year_option['text']}, "
                        f"Current city: {city_option['text']}, "
                        f"Current event: {event_option['text']}."
                    )

                    scraper.get_category_options_html(
                        championship_option["value"],
                        year_option["value"],
                        city_option["value"],
                        event_option["value"],
                    )

                    for category_option in scraper.categories:
                        logger.info(
                            f"Current championship {championship_option['text']}, "
                            f"Current year: {year_option['text']}, "
                            f"Current city: {city_option['text']}, "
                            f"Current event: {event_option['text']}, "
                            f"Current category: {category_option['text']}."
                        )

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

                        logger.info(f"Championship record: {championship_record}.")

                        db.add(table_name=TABLE_NAME, data=championship_record)

                        logger.info(f"{championship_record} added to database.")

                        print(f"{championship_record} added to database.")


if __name__ == "__main__":
    main()
