from red_utils.utils import file_utils, context_managers
from red_utils import CustomException
import random
from pathlib import Path

from time import sleep


def test_file_utils_list() -> list[Path]:
    cwd = Path.cwd()
    search_dir = f"{cwd}/red_utils"

    list_files_test = file_utils.list_files(in_dir=search_dir, ext_filter=".py")
    print(f".py files found in {search_dir}: {len(list_files_test)}")

    rand_index = random.randint(0, len(list_files_test) - 1)
    print(f"Example util file: {list_files_test[rand_index]}")

    file_dicts: list[dict] = []

    try:
        for f in list_files_test:
            f_dict: dict = {"name": None, "path": None}

            f_dict["name"] = f.name
            f_dict["path"] = f.parent

            file_dicts.append(f_dict)

        return file_dicts

    except Exception as exc:
        raise CustomException(
            "Unhandled exception creating dict.",
            errors=exc,
            extra={"Exception type": exc.__class__},
        )


def test_context_managers(limit: int = 5, _sleep: int = 1) -> None:
    def benchmark_test(limit=limit, _sleep=_sleep) -> None:
        with context_managers.benchmark("Test benchmark"):
            current_count: int = 0

            while current_count < limit:
                print(f"Count: {current_count}")
                current_count += 1

                sleep(_sleep)

    def protected_list_test(
        original_list: list[str] = ["item1", "item2", "item3"]
    ) -> list[str]:
        print(f"List before protected update: {original_list}")

        with context_managers.ListProtect(original=original_list) as copy:
            copy.append("item4")

        return original_list

    def protected_dict_test(
        original_dict: dict[str, int] = {"one": 1, "two": 2, "three": 3}
    ) -> dict[str, int]:
        print(f"Dict before protected update: {original_dict}")

        with context_managers.DictProtect(original=original_dict) as copy:
            copy["four"] = 4

        return original_dict

    def sqlite_manager_test(db_path: str = "test.db"):
        with context_managers.SQLiteConnManager(path=db_path) as db:
            db.get_tables()

    # benchmark_test()

    # protect_list = protected_list_test()
    # print(f"List after protected copy: {protect_list}")

    # protect_dict = protected_dict_test()
    # print(f"Dict after protected copy: {protect_dict}")

    # sqlite_manager_test()
    pass


def main():
    # file_util_test = test_file_utils_list()
    # print(file_util_test)

    test_context_managers()


if __name__ == "__main__":
    main()
