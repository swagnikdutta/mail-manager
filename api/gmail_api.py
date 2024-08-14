import logging

from models.message import Message

LIST_RESULTS_MAX = 500
LIST_RESULTS_DEFAULT = 100


def get_message(svc, msg_id):
    logger = logging.getLogger(__name__)
    try:
        result = svc.users().messages().get(userId="me", id=msg_id).execute()
        return result
    except Exception as e:
        logger.error(f"Error while fetching message with id: ${id}. Error: ${e}")
        raise


def list_messages(svc, count=LIST_RESULTS_DEFAULT):
    if count > LIST_RESULTS_MAX:
        logging.info(f"count cannot exceed {LIST_RESULTS_MAX}. Setting count to {LIST_RESULTS_MAX}")
        count = LIST_RESULTS_MAX

    logger = logging.getLogger(__name__)
    try:
        results = []
        response = svc.users().messages().list(userId="me", maxResults=count).execute()
        messages = response.get("messages", [])

        for i, m in enumerate(messages):
            msg_id = messages[i].get("id", "")
            if msg_id:
                message = get_message(svc, msg_id)
                msg_object = Message().deserialize(message)
                results.append(msg_object)

        return results

    except Exception as e:
        logger.error(f"Error while listing messages: ${e}")
        return None


def modify_message(svc, msg_id, req_body):
    logger = logging.getLogger(__name__)
    try:
        svc.users().messages().modify(userId="me", id=msg_id, body=req_body).execute()
    except Exception as e:
        logger.error(f"Error modifying message. Error: {e}")