import json
import logging
from typing import Iterable, List

from more_itertools import chunked
from requests import post


log = logging.getLogger(__file__)


def add_index_actions(elements: Iterable, index_name: str) -> List:
    result = []
    for element in elements:
        if "id" in element:
            result.append({'index': {'_index': index_name, '_id': element["id"]}})
        else:
            result.append({'index': {'_index': index_name}})
        result.append(element)
    return result


def encode_elements(elements):
    try:
        return "\n".join(map(lambda elem: json.dumps(elem), elements)) + "\n"
    except Exception as e:
        log.error(f"Caught error serializing: {elements}")
        raise e


def bulk_index(elements: list):
    if len(elements) == 0:
        log.info("Skipping indexing of empty list.")
        return
    encoded_elements = encode_elements(elements)
    es_endpoint = "http://10.8.0.8:9200"
    log.debug(f"POST {es_endpoint}/_bulk")
    response = post(f"{es_endpoint}/_bulk", encoded_elements, headers={"Content-Type": "application/json"})
    log.debug(f"response code: {response.status_code}")
    hundred_status = int(response.status_code / 100)
    if hundred_status != 2:
        log.error(f"ElasticSearch ({response.status_code}: {response.content}")
        log.error(f"POST {es_endpoint}/_bulk")
        # log.error(encoded_elements)
        raise ValueError(f"ElasticSearch ({response.status_code}: {response.content}")
    return response.content


def index_documents(index_name: str, documents: Iterable, batch_size=100):
    for batch in chunked(documents, batch_size):
        bulk_index(add_index_actions(elements=batch, index_name=index_name))

