import argparse
import csv
import logging

import earningscall
from earningscall import get_company, get_sp500_companies
from earningscall.company import Company
from earningscall.utils import configure_sane_logging
from textblob import TextBlob

from utils import get_earningscall_secret_api_key

log = logging.getLogger(__file__)
earningscall.api_key = get_earningscall_secret_api_key()


def run_sentiment(company: Company, _csv_writer=None):
    for event in company.events():
        transcript = company.get_transcript(event=event)  # Fetch the earnings call transcript for this event
        if not transcript:
            continue
        blob = TextBlob(transcript.text)
        log.info(f"{company} {event.year} Q{event.quarter} {blob.sentiment}")
        if _csv_writer:
            _csv_writer.writerow([
                company.company_info.name,
                company.company_info.symbol,
                company.company_info.sector,
                company.company_info.industry,
                event.year,
                event.quarter,
                blob.sentiment.polarity,
                blob.sentiment.subjectivity
            ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Enable debug logs')
    parser.add_argument('--sp500',
                        action='store_true',
                        help='Run sentiment analysis for all S&P 500 companies.')
    parser.add_argument('--ticker',
                        type=str,
                        help='Run sentiment analysis for individual company.')

    args = parser.parse_args()
    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    configure_sane_logging(level)

    with open('sentiment-data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            "Company Name",
            "Ticker Symbol",
            "Sector",
            "Industry",
            "Year",
            "Quarter",
            "Polarity",
            "Subjectivity",
        ])
        if args.ticker:
            run_sentiment(get_company(args.ticker))
        if args.sp500:
            for _company in get_sp500_companies():
                run_sentiment(_company, csv_writer)
