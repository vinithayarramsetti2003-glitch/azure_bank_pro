import os
import logging
import json
import azure.functions as func
from azure.servicebus import (
    ServiceBusClient,
    ServiceBusMessage,
    TransportType
)

def main(evt: func.EventGridEvent):
    logging.info("EventGrid trigger fired")
    try:
        # parse event safely (Event Grid sometimes sends raw dict or CloudEvent shape)
        try:
            body = evt.get_json()
        except Exception:
            raw = evt.get_body().decode("utf-8", errors="ignore")
            body = json.loads(raw) if raw else {}

        logging.info("Event body: %s", json.dumps(body))

        # Extract blob url from multiple possible places (top-level url, data.url, data.blobUrl, value[...] shapes)
        url = None
        if isinstance(body, dict):
            url = body.get("url")  # your payload shows top-level "url"
            if not url:
                data = body.get("data")
                if isinstance(data, dict):
                    url = data.get("url") or data.get("blobUrl") or data.get("uri")
            if not url:
                # sometimes Event Grid wraps events in a 'value' list
                if isinstance(body.get("value"), list) and body["value"]:
                    url = (body["value"][0].get("data") or {}).get("url")

        logging.info("Blob URL received: %s", url)

        # validate env
        conn = os.getenv("SERVICE_BUS_CONNECTION_STR")
        queue_name = os.getenv("SERVICE_BUS_QUEUE_NAME")
        if not conn:
            logging.error("SERVICE_BUS_CONNECTION_STR is not set in application settings.")
            return
        if not queue_name:
            logging.error("SERVICE_BUS_QUEUE_NAME is not set in application settings.")
            return

        # Use AMQP over WebSocket to avoid ssl.wrap_socket issues
        with ServiceBusClient.from_connection_string(conn, transport_type=TransportType.AmqpOverWebsocket) as sb_client:
            with sb_client.get_queue_sender(queue_name) as sender:
                sender.send_messages(ServiceBusMessage(url or ""))

        logging.info("Message successfully sent to Service Bus")

    except Exception:
        logging.exception("Error in handleEventGrid")
        raise