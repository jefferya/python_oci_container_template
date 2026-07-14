#!/usr/bin/env python3

"""
Desc: use web scrapping on the Archive.org instance of the Pierre Ouvrard Archive
        to extract the URL, title, physical description, and bibliographic information for the binding records.
        Request by Sarah Severson, July 7/8 2026

Usage:
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        python3 src/2026-07-08_sarah_severson_pierre_ouvrard_archive.org.py --help
"""

import time
from urllib.parse import urljoin

import argparse
import csv
import logging
import requests

from bs4 import BeautifulSoup


# pylint: disable=R0801
def argument_parser():
    """
    Set up argument parsing for the script.
    """
    parser = argparse.ArgumentParser(
        description="Web scraper for extracting information from the Pierre Ouvrard Bindings and outputing as CSV"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    return parser.parse_args()


# This is quick but works. Disable the following.
# pylint: disable=too-many-locals, logging-fstring-interpolation, too-many-nested-blocks
def main():
    """
    Main function to demonstrate logging and argument parsing.
    """

    base_url = "https://web.archive.org"
    list_of_pages_prefix = f"{base_url}/web/20170423191925/http://ouvrard.library.ualberta.ca/english/browse"
    # 13 pages hard-code urls; range inclusive on lower bound, exclusive upper bound.
    list_of_pages = [f"{list_of_pages_prefix}{i}.htm" for i in range(1, 14)]

    args = argument_parser()

    # Configure logging based on argument
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    header = ["link_url", "title", "Physical description", "Bibliographic information"]
    with open("/tmp/scrap_v3.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(header)

        # Set a user-agent to mimic a real browser to help circumvent potential bot blocking mechanisms.
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/124.0.0.0 Safari/537.36"
        }

        for page in list_of_pages:
            logging.info("Processing page: %s", page)

            response = requests.get(page, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Grab all the nested tables
            nested_tables = soup.select("table table")
            # only want the thrid table in the page layout containing the links to individual records
            binding_table = nested_tables[2] if nested_tables else None

            for link in binding_table.select("a") if binding_table else []:
                extracted_data = {}

                url = link.get("href")
                thumbnail = link.select_one("img")
                logging.debug(
                    f"Found link: {url}, Thumbnail: {thumbnail['src'] if thumbnail else 'No thumbnail'}"
                )

                link_url = urljoin(page, url)
                extracted_data["link_url"] = link_url

                response_link = requests.get(link_url, headers=headers, timeout=30)
                response_link.raise_for_status()
                soup_details = BeautifulSoup(
                    response_link.content.decode("ISO-8859-1", errors="replace"),
                    "html.parser",
                )
                # soup_details = BeautifulSoup(response_link.text, 'html.parser')
                title = soup_details.title.text if soup.title else "No Title Found"
                extracted_data["title"] = title
                logging.info(f"Title of the linked page: {title}")

                for b_tag in soup_details.find_all("b"):
                    logging.debug(f"Processing <b> tag: {b_tag}")
                    label = b_tag.get_text(strip=True)

                    # Identify header tags)
                    clean_key = label.replace(":", "")
                    if clean_key in [
                        "Physical description",
                        "Bibliographic information",
                    ]:
                        value_parts = []

                        # Iterate through all upcoming siblings until we hit a <p> tag
                        for sibling in b_tag.next_siblings:
                            if sibling.name == "p":
                                break

                            if sibling.name is None:  # Text node
                                value_parts.append(sibling.text)
                            else:  # HTML elements (like the internal <b>Taxicologie ...</b>)
                                value_parts.append(sibling.get_text())

                        # Combine everything, strip messy whitespace, and replace non-breaking spaces
                        raw_text = "".join(value_parts)
                        # .split() combined with ' '.join() strips out all multiple spaces, \n, and \t
                        clean_text = " ".join(raw_text.split()).replace("\xa0", " ")

                        extracted_data[clean_key] = clean_text

                writer.writerow(extracted_data.values())

                logging.info(f"Extracted data: {extracted_data}")

                # Crude sleep to avoid triggering the rate limiting of archive.org. Adjust as necessary
                # Consider using a more configurable approach such as https://pypi.org/project/requests-ratelimiter/
                # to limit by the number of request per second or burst.
                time.sleep(30.0)
                # exit()

            # Here you can add your actual processing logic
            logging.debug(f"Finished processing page: {page}")


if __name__ == "__main__":
    main()
