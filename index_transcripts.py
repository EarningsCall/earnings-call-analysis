import logging
import sys
from typing import Iterable

import earningscall
from earningscall import get_sp500_companies
from earningscall.company import Company

from search import index_documents

log = logging.getLogger(__file__)
with open(".earnings-call-api-key", "r") as fd:
    earningscall.api_key = fd.read().strip()
LOG_FORMAT = "[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(lineno)s)"


def get_company_documents(company: Company) -> Iterable[dict]:
    for event in company.events():
        log.info(f"Event: {event.year} Q{event.quarter}")
        transcript = company.get_transcript(event=event)  # Fetch the earnings call transcript for this event
        yield {
            "id": f"{company.company_info.exchange}-{company.company_info.symbol}-{event.year}-{event.quarter}",
            "exchange": company.company_info.exchange,
            "symbol": company.company_info.symbol,
            "year": event.year,
            "quarter": event.quarter,
            "conference_date": event.conference_date.isoformat() if event.conference_date else None,
            "text": transcript.text if transcript else None,
        }


def sp_500_documents():
    for company in get_sp500_companies():
        for doc in get_company_documents(company):
            yield doc


def configure_sane_logging(level=logging.DEBUG):
    # Manually set the following loggers to "INFO", since they tend to be VERY noisy, and when we are
    # debugging our own application, we only care about DEBUG logs from OUR application, not these libs.
    for name in ['urllib3']:
        logging.getLogger(name).setLevel(logging.INFO)
    logging.getLogger("filelock").setLevel(logging.WARNING)
    logging.basicConfig(level=level, stream=sys.stdout, format=LOG_FORMAT)


configure_sane_logging()

index_documents("earnings-call", sp_500_documents())
