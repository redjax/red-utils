import logging

log = logging.getLogger(__name__)

from core import setup
import std_time_utils as time_utils
from std_context_managers import ListProtect, DictProtect


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


def main():
    # demo_timestamp()

    # demo_list_protect()

    demo_dict_protect()


if __name__ == "__main__":
    setup.setup_logging(level="DEBUG")
    log.info("Start demo")
    log.debug("Test DEBUG message")

    main()
