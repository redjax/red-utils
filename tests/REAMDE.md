# Pytest tests for red_utils

I am still learning the `pytest` framework, and make no promises or guarantees that there are tests for all of the functionality in this module.

## Tests TODO

- `std` tests
  - `database_managers` tests
    - [ ] create fixture for `SQLiteConnManager`
    - [ ] test initializing database file
    - [ ] test getting a connection
    - [ ] create default test data
    - [ ] test inserting records
    - [ ] test updating records
    - [ ] test deleting records
    - [ ] test `.get_tables()`
    - [ ] test `.run_sqlite_stmt()`
    - cleanup:
      - [ ] delete `sqlite` database file
- `ext` tests
  - `dataframe_utils` tests
    - Fixtures:
      - [ ] dict that can be converted to a Pandas dataframe
      - [ ] Pandas dataframe
      - [ ] list of Pandas dataframes
      - [ ] `dict` for a `.parquet` file
      - [ ] CSV data for a `.csv` file
    - [ ] test writing `.parquet` file
    - [ ] test reading `.parquet` file
    - [ ] test reading `.parquet` file to dataframe
    - [ ] test saving dataframe to `.parquet` file
    - [ ] test writing `.csv` file
    - [ ] test reading `.csv` file
    - [ ] test reading `.csv` file to dataframe
    - [ ] test saving dataframe to `.csv` file
    - [ ] test converting `.csv` file to `.parquet` file
    - [ ] test converting `.parquet` file to `.csv` file
    - [ ] test concatenating dataframes
    - [ ] test deduplicating Pandas dataframe
    - cleanup:
      - [ ] delete all `.csv` files
      - [ ] delete all `.parquet` files
  - `diskcache_utils` tests
    - Fixtures:
      - [ ] a `diskcache.Cache` object
      - [ ] an in-memory cache
    - [ ] test setting value
    - [ ] test getting value
    - [ ] test expiring value
    - [ ] test updating value
    - [ ] test updating expire value
    - [ ] test checking if key exists in cache
    - cleanup:
      - [ ] delete diskcache.cache dir/db