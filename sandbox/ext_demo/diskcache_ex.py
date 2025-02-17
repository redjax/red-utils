# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "diskcache",
#     "red-utils",
# ]
#
# [tool.uv.sources]
# red-utils = { path = "../../" }
# ///

from red_utils.ext import diskcache_utils

if __name__ == "__main__":
    print(f"Default cache conf: {diskcache_utils.default_cache_conf}")
    cache = diskcache_utils.new_cache(cache_conf=diskcache_utils.default_cache_conf)
    cache["key"] = "value"
    print(cache["key"])
    print(f"Cache size: {diskcache_utils.get_cache_size(cache=cache)}")
