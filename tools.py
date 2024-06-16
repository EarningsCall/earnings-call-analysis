import logging
from typing import Optional, Type

from earningscall import get_company
from langchain.pydantic_v1 import BaseModel
from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic.v1 import Field

log = logging.getLogger(__file__)


class CompanyMetaDataToolInput(BaseModel):
    ticker_symbol: str = Field(description="A ticker symbol is a unique series of letters assigned to a security or "
                                           "stock for trading purposes on a particular stock exchange. It acts as an"
                                           " abbreviation or code that represents the publicly traded company. For e"
                                           "xample, Apple’s ticker symbol is AAPL, and Microsoft’s is MSFT. Ticker s"
                                           "ymbols are used to identify the stock in trading and other financial tra"
                                           "nsactions. They can consist of letters, numbers, or a combination of bo"
                                           "th, depending on the exchange and the type of security.")


class CompanyMetaDataTool(BaseTool):
    name = "CompanyMetaDataTool"
    description = ("The Company Metadata Retriever is a tool designed to fetch comprehensive company "
                   "metadata using a stock ticker symbol. This tool is essential for investors, analysts, and "
                   "businesses seeking detailed information about a specific company in a streamlined and "
                   "efficient manner.")
    args_schema: Type[BaseModel] = CompanyMetaDataToolInput
    return_direct: bool = True

    def _run(
        self, ticker_symbol: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        company = get_company(ticker_symbol)
        return company.company_info.to_json()


class CompanyEventsToolInput(BaseModel):
    ticker_symbol: str = Field(description="A ticker symbol is a unique series of letters assigned to a security or "
                                           "stock for trading purposes on a particular stock exchange. It acts as an"
                                           " abbreviation or code that represents the publicly traded company. For e"
                                           "xample, Apple’s ticker symbol is AAPL, and Microsoft’s is MSFT. Ticker s"
                                           "ymbols are used to identify the stock in trading and other financial tra"
                                           "nsactions. They can consist of letters, numbers, or a combination of bo"
                                           "th, depending on the exchange and the type of security.")


class CompanyEventsTool(BaseTool):
    name = "CompanyEventsTool"
    description = ("The Company Events Tool is a tool designed to fetch earnings events for a company."
                   " Each earnings event contains metadata including the conference date, the quarter, and the year.")
    args_schema: Type[BaseModel] = CompanyMetaDataToolInput
    return_direct: bool = True

    def _run(
        self, ticker_symbol: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> list:
        """Use the tool."""
        company = get_company(ticker_symbol)
        return [event.to_json() for event in company.events()]


class EarningsEventTranscriptToolInput(BaseModel):
    ticker_symbol: str = Field(description="A ticker symbol is a unique series of letters assigned to a security or "
                                           "stock for trading purposes on a particular stock exchange. It acts as an"
                                           " abbreviation or code that represents the publicly traded company. For e"
                                           "xample, Apple’s ticker symbol is AAPL, and Microsoft’s is MSFT. Ticker s"
                                           "ymbols are used to identify the stock in trading and other financial tra"
                                           "nsactions. They can consist of letters, numbers, or a combination of bo"
                                           "th, depending on the exchange and the type of security.")
    year: int = Field(description="The year of the conference.")
    quarter: int = Field(description="The quarter of the conference.")


class EarningsEventTranscriptTool(BaseTool):
    name = "EarningsEventTranscriptTool"
    description = ("The Earnings Event Transcript Tool Events Tool is a tool designed to fetch the entire transcript"
                   " text for a given earnings event. The transcript text contains the full transcript for the event"
                   " and includes speaker names, timestamps, and other relevant information.")
    args_schema: Type[BaseModel] = EarningsEventTranscriptToolInput
    return_direct: bool = True

    def _run(
        self, ticker_symbol: str, year: int, quarter: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        company = get_company(ticker_symbol)
        transcript = company.get_transcript(year=year, quarter=quarter)
        return transcript.text
