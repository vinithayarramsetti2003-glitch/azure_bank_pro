import logging
import azure.functions as func

def main(msg: func.ServiceBusMessage):
    logging.info("QueueProcessor fired")

    try:
        body_bytes = msg.get_body()
        if body_bytes is None:
            logging.warning("Message body is None")
            body = None
        else:
            try:
                body = body_bytes.decode("utf-8")
            except Exception:
                # fallback; show raw bytes if decode fails
                body = str(body_bytes)

        logging.info("Message body: %s", body)

    except Exception as e:
        logging.exception("QueueProcessor error: %s", e)
        raise