import logging

log = logging.getLogger(__name__)

from red_utils.core import setup
import red_utils.std as time_utils
from red_utils.std.context_managers import ListProtect, DictProtect
from red_utils.ext import httpx_utils

import pandas as pd


def demo_timestamp():
    ts = time_utils.get_ts()
    log.info(f"Timestamp ({type(ts)}): {ts}")

    ts_str = time_utils.get_ts(as_str=True)
    log.info(f"Timestamp string ({type(ts_str)}): {ts_str}")


def demo_list_protect():
    original_list = [1, 2, 3, 4]

    with ListProtect(original_list) as copy:
        log.info(f"Copied list: {copy}")

        copy.append(5)
        copy = copy + [6, 7, 8]
        log.info(f"Original list: {original_list}, ListProtect copy: {copy}")

    log.info(f"Original list (after update): {original_list}")

    original_list = ["a", "b", "c"]
    with ListProtect(original_list) as copy:
        log.info(f"Copied list: {copy}")

        copy.append("d")
        log.info(f"Original list: {original_list}, ListProtect copy: {copy}")

        log.warning(
            f"An error will now be caused intentionally, the list will not be modified"
        )
        copy.append(1 / 0)

    log.info(f"Original list (unmodified because of exception): {original_list}")


def demo_dict_protect():
    original_dict = {"name": "lucy", "age": 25}

    with DictProtect(original_dict) as copy:
        log.info(f"Copied dict: {copy}")

        copy["name"] = "paul"
        copy["age"] = 32

        log.info(f"Original dict: {original_dict}, DictProtect copy: {copy}")

    log.info(f"Original dict (after update): {original_dict}")

    original_dict = {"name": "lucy", "age": 25, "favorite_color": "blue"}
    with DictProtect(original_dict) as copy:
        log.info(f"Copied dict: {copy}")

        copy["favorite_color"] = "green"
        log.info(f"Original dict: {original_dict}, DictProtect copy: {copy}")

        log.warning(
            f"An error will now be caused intentionally, the dict will not be modified"
        )
        copy["name"] = "paul"
        assert copy["name"] == "lucy", ValueError(
            f"copy['name'] should have been 'lucy', got {copy['name']}. THIS ERROR IS EXPECTED, PROGRAM WILL CONTINUE"
        )

    log.info(f"Original dict (unmodified because of exception): {original_dict}")


def demo_http_client():
    http_controller = httpx_utils.get_http_controller()

    req = httpx_utils.build_request(url="https://xkcd.com/info.0.json")

    with http_controller as http:
        res = http.client.send(request=req)

    log.info(f"Response: [{res.status_code}: {res.reason_phrase}]: {res.text}")


def demo_pandas():
    df_data_dict = [
        {"name": "Lucy", "age": 35, "occupation": "nurse"},
        {"name": "Fred", "age": 16, "occupation": "mechanic"},
        {"name": "Geronimo", "age": 64, "occupation": "retired"},
        {"name": "Giselda", "age": 72, "occupation": "retired"},
    ]
    df = pd.DataFrame(df_data_dict)

    log.info("Printing person dataframe")

    print(df.head(5))


def main():
    # log.info("DEMO timestamps")
    # demo_timestamp()

    # log.info("DEMO ListProtect class")
    # demo_list_protect()

    # log.info("DEMO DictProtect class")
    # demo_dict_protect()

    # log.info("DEMO httpx request controller")
    # demo_http_client()

    log.info("DEMO pandas dataframe utils")
    demo_pandas()


if __name__ == "__main__":
    setup.setup_logging(level="DEBUG")
    log.info("Start demo")
    log.debug("Test DEBUG message")

    main()
