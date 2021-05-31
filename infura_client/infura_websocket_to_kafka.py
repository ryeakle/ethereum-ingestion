import json

import websocket
from kafka import KafkaProducer
from settings import INFURA_SUBSCRIPTION, INFURA_WEBSOCKET, KAFKA_SERVER, KAFKA_TOPIC
from utils import retry_with_exponential_backoff


def pipe_infura_websocket_to_kafka(subscription_type):
    """
    Given a subscription type (https://infura.io/docs/ethereum/wss/eth-subscribe),
    set up a websocket connection, request that data, then receive and pipe to a kafka
    topic as described in settings.py
    """

    producer = get_kafka_producer(bootstrap_servers=[KAFKA_SERVER])

    ws = connect_to_websocket(
        ws_endpoint=INFURA_WEBSOCKET,
        start_request={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_subscribe",
            "params": [subscription_type],
        },
    )

    while True:
        message = ws.recv()
        if not message:
            continue

        producer.send(KAFKA_TOPIC, bytes(message, encoding="utf-8"))


@retry_with_exponential_backoff
def connect_to_websocket(ws_endpoint, start_request):
    """
    returns a successful websocket connection which we can use to start reading in data
    args:
    - ws_endpoint: your infura project websocket, will look something like
    - start_request: a dict of the first thing to send to the infura websocket to start receiving
      messages
    """

    EXPECTED_RESPONSE = {"jsonrpc": "2.0", "id": 1, "result": "0x1"}

    ws = websocket.WebSocket()
    ws.connect(ws_endpoint)
    ws.send(json.dumps(start_request))

    stream_start_response = json.loads(ws.recv())
    if stream_start_response != EXPECTED_RESPONSE:
        raise Exception(
            "failed to start subscription to topic: {}".format(
                start_request["params"][0]
            )
        )

    return ws


@retry_with_exponential_backoff
def get_kafka_producer(bootstrap_servers):
    return KafkaProducer(bootstrap_servers=KAFKA_SERVER)


if __name__ == "__main__":
    pipe_infura_websocket_to_kafka(INFURA_SUBSCRIPTION)
