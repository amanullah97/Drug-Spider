# Drug-Spider
"Web Scraping Drug Information from target website: [drugs](https://www.drugs.com/) with Scrapy"

This Git repository contains a Scrapy spider script that performs web scraping to gather drug information from the drugs.com website. The spider, named "DrugSpider," starts by visiting the main drugs.com page and then navigates through various links to scrape drug and condition data.

The spider follows links on the main page to extract drug and condition URLs. It then proceeds to scrape information about individual drugs, including their names, generic names, medical reviews, last update dates, drug classes, ratings, reviews, and item types (whether it is a drug or condition).

The script utilizes Scrapy's callback mechanism to navigate through different levels of URLs and extract the desired data. It employs CSS selectors to identify HTML elements and extract relevant information. Additionally, it uses regular expressions to extract and format dates and medically reviewed information from the scraped data.

The extracted data is yielded as Python dictionaries for further processing or storage. The spider is designed to handle both drug and condition pages, extracting the necessary information accordingly.

This project serves as an example of how to scrape drug-related data from the drugs.com website using the Scrapy framework in Python. It demonstrates navigation through multiple levels of pages, extraction of data using CSS selectors, and the utilization of regular expressions for specific data formatting.
