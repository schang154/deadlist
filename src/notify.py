import requests
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

def send_telegram_msg(token: str, chat_ids: List, message: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    for cid in chat_ids:
        cleaned_cid = cid.strip()
        payload = {"chat_id": cleaned_cid, "text": message}
  
        try:
            response = requests.post(url, data=payload, timeout=15)
            response.raise_for_status()
            resp_json = response.json()
            if not resp_json.get("ok", False):
                logger.error(
                    "Telegram API error for chat_id=%s: %s",
                    cid,
                    resp_json
                )
                continue

            logger.info("Message sent successfully to chat_id=%s", cid)

        except requests.exceptions.Timeout:
            logger.error("Telegram request timeout for chat_id=%s", cid)

        except requests.exceptions.RequestException as exc:
            logger.error(
                "Telegram request failed for chat_id=%s: %s",
                cid,
                exc
            )

        except Exception as exc:
            logger.exception(
                "Unexpected error when sending Telegram message to chat_id=%s: %s",
                cid,
                exc
            )

def send_notification(token: str, chat_ids: List[str], 
                      target_counties: List[str],  
                      metadata: dict) -> None:
    
    current_counts = metadata.get("focus_region_counts", {})
    previous_counts = metadata.get("focus_region_previous_counts", {})
    start_date = metadata.get("focus_region_start_date", "unknown date")

    current_total = sum(current_counts.get(county, 0) for county in target_counties)
    previous_total = sum(previous_counts.get(county, 0) for county in target_counties)
    new_records = current_total - previous_total

    counties_label = "/".join(county.replace("縣", "").replace("市", "")
                              for county in target_counties
                              )

    if new_records > 0:
        message = (
            f"🚨 Found {new_records} new records in {counties_label} "
            f"since {start_date}. Total: {current_total} "
            f"(Previous: {previous_total})"
        )
    else:
        message = (
            f"List updated. No new records found in {counties_label} "
            f"since {start_date}. Total remains {current_total}."
        )

    send_telegram_msg(token, chat_ids, message)

def maybe_send_alert(send_alert: bool, token: Optional[str], chat_ids: List[str], 
                     target_counties: List[str], metadata: dict) -> None:
    if not send_alert:
        return

    if not token or not chat_ids:
        raise ValueError("Missing TOKEN or CHAT_ID environment variables.")

    send_notification(
        token,
        chat_ids,
        target_counties,
        metadata,
    )