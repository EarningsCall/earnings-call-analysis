import argparse
import json
import logging
from time import time

from earningscall.utils import configure_sane_logging
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import create_react_agent

from tools import CompanyMetaDataTool, EarningsEventTranscriptTool, CompanyEventsTool
from utils import verbose_timedelta

log = logging.getLogger(__file__)


def get_anthropic_secret_api_key():
    with open(".anthropic-api-key", "r") as fd:
        return fd.read().strip()


# https://docs.smith.langchain.com/how_to_guides/tracing/trace_without_env_vars
def get_langsmith_secret_api_key():
    with open(".langsmith-secret-key", "r") as fd:
        return fd.read().strip()


# Price is per million tokens
model_costs = {
    # https://www.anthropic.com/api#pricing
    "claude-3-haiku-20240307": {
        "input_tokens": 0.25,
        "output_tokens": 1.25,
    },
    "claude-3-sonnet-20240229": {
        "input_tokens": 3.0,
        "output_tokens": 15.0,
    },
    "claude-3-opus-20240229": {
        "input_tokens": 15.0,
        "output_tokens": 75.0,
    },
}


class Agent:

    def __init__(self, model_name):
        self.start_time = None
        self.end_time = None
        self.input_tokens = 0
        self.output_tokens = 0
        self.model_name = model_name

    def query(self, query: str):
        self.start_time = time()
        memory_checkpointer = SqliteSaver.from_conn_string(":memory:")
        model = ChatAnthropic(model_name=self.model_name, api_key=get_anthropic_secret_api_key())
        tools = [
            CompanyMetaDataTool(),
            CompanyEventsTool(),
            EarningsEventTranscriptTool(),
        ]
        agent_executor = create_react_agent(model, tools, checkpointer=memory_checkpointer)
        config = {
            "configurable": {
                "thread_id": "abc123",
            },
        }
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=query)]}, config
        ):
            if "agent" in chunk:
                for message in chunk["agent"]["messages"]:
                    self.input_tokens += message.usage_metadata["input_tokens"]
                    self.output_tokens += message.usage_metadata["output_tokens"]
            yield chunk
        self.end_time = time()

    def total_cost(self):
        input_cost = model_costs[self.model_name]["input_tokens"] * self.input_tokens / 1_000_000.0
        output_cost = model_costs[self.model_name]["output_tokens"] * self.output_tokens / 1_000_000.0
        return (input_cost + output_cost) * 100.0

    def log_cost(self):
        log.info(f"Total Cost of Query: ¢{round(self.total_cost(), 2)}")

    def log_query_time(self):
        elapsed_time = self.end_time - self.start_time
        log.info(f"Total Agent Runtime was {verbose_timedelta(elapsed_time)}.")


class LangChainObjEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseMessage):
            return obj.dict()
        elif isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def dump_ai_json(obj, indent=None, **kwargs):
    return json.dumps(obj, cls=LangChainObjEncoder, indent=indent, **kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Enable debug logs')
    parser.add_argument('--model',
                        type=str,
                        default="claude-3-sonnet-20240229",
                        help='The Anthropic Model to use.  One of: '
                             '[claude-3-haiku-20240307, claude-3-sonnet-20240229 or claude-3-opus-20240229]')
    parser.add_argument('--query',
                        default="Summarize MSFT's most recent earnings call.",
                        type=str,
                        help='Your query')
    args = parser.parse_args()
    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    configure_sane_logging(level)

    agent = Agent(args.model)
    chunks = [chunk for chunk in agent.query(query=args.query)]
    for chunk in chunks:
        log.info(dump_ai_json(chunk))
        log.info("   ----------------------------   ")
    agent.log_cost()
    agent.log_query_time()
