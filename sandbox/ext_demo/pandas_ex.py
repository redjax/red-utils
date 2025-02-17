# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "fastparquet",
#     "pandas",
#     "pyarrow",
#     "red-utils",
# ]
#
# [tool.uv.sources]
# red-utils = { path = "../../" }
# ///

from red_utils.ext import pandas_utils as pd_utils

import pandas as pd

DATA: list[dict] = [
    {"name": "George", "gender": "Male", "birthday": "1996-07-24", "enabled": True},
    {
        "name": "Elizabeth",
        "gender": "Female",
        "birthday": "2002-10-13",
        "enabled": False,
    },
    {"name": "Paul", "gender": "Female", "birthday": "1970-02-08", "enabled": True},
    {"name": "Sam", "gender": "Female", "birthday": "2008-05-18", "enabled": True},
]


def main(data: list[dict]) -> None:
    df = pd.DataFrame(data)
    print(f"Dataframe:\n{df}")

    print(f"There are {pd_utils.count_df_rows(df)} row(s) in the dataframe")

    oldest_newest = pd_utils.get_oldest_newest(df, date_col="birthday")
    print(f"Oldest/newest:\n{oldest_newest}")


if __name__ == "__main__":
    main(data=DATA)
