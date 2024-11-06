import csv
import asyncio

from vera_gpt.models.iab import IAB

from vera_gpt.web_scrapers import WebScraper
from vera_gpt.web_scrapers.utils import text_from_html
from vera_gpt.web_scrapers.utils import truncate_content_for_gpt


INPUT_FILE = "urls_to_categorize.csv"
OUTPUT_FILE = "categorized_urls.csv"
GPT_INPUT_WORD_LIMIT = 2800


def create_output_file():
    with open(OUTPUT_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "ind",
                "URL",
                "IAB Category IDs",
                "IAB Category Names",
                "Content Summary",
            ]
        )


def write_to_output_file(data):
    with open(OUTPUT_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def main():
    create_output_file()
    scraper = WebScraper()
    iab = IAB(async_call=False)

    output = []
    scraped_urls = []
    contents = []
    with open(INPUT_FILE, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers

        print("SCRAPING URLS")
        for ind, row in enumerate(reader):
            url = row[0]
            response = asyncio.run(scraper.scrape(url))
            if response.status_code != 200:
                output.append(
                    [
                        ind,
                        url,
                        "N/A",
                        "N/A",
                        f"Got error: {response.status_code}",
                    ]
                )
                continue

            page_content = text_from_html(response.content)
            content = truncate_content_for_gpt(
                page_content, GPT_INPUT_WORD_LIMIT
            )
            scraped_urls.append([ind, url])
            contents.append(content)

    results = iab.categorize_batch(contents)
    for scraped_url, result in zip(scraped_urls, results):
        entry = scraped_url + result
        output.append(entry)
    write_to_output_file(sorted(output))


if __name__ == "__main__":
    main()
