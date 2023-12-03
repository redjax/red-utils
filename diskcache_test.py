from red_utils.ext.diskcache_utils import CacheInstance
import time

if __name__ == "__main__":
    test_cache = CacheInstance(cache_dir="./test/cache")
    print(f"Cache dir: {test_cache.cache_dir}")
    print(f"Cache path: {test_cache.cache_path}")
    test_cache.init()

    print(f"Cache exists at {test_cache.cache_path}: {test_cache.exists()}")

    print(f"Cache type ({type(test_cache.cache)})")

    print(f"Cache instance dict: {test_cache.as_dict()}")

    test_cache.clear()

    test_key: str = "test"
    test_val: dict[str, int] = {"test": 1}

    print(f"Test retrieve key [{test_key}]: {test_cache.get_val(key=test_key)}")

    print(
        f"Key: [{test_key}]. Exists in cache (should be False): {test_cache.check_key_exists(test_key)}"
    )

    test_cache.set_val(key=test_key, val=test_val)
    print(
        f"Key: [{test_key}] Exists in cache (should be True): {test_cache.check_key_exists(test_key)}"
    )

    # print(f"Clearing cache")
    # test_cache.clear()
    # print(
    #     f"Key: [{test_key}]. Exists in cache (should be False): {test_cache.check_key_exists(test_key)}"
    # )

    # print("Test creating cache tag index")
    # test_cache.manage_cache_tag_index("create")
    # print("Deleting cache tag index")
    # test_cache.manage_cache_tag_index("delete")

    # test_cache.set_expire(key=test_key, expire=1)
    # time.sleep(1.5)
    # print(
    #     f"Key: [{test_key}] Exists in cache (should be False): {test_cache.check_key_exists(test_key)}"
    # )

    # test_cache.delete_val(key=test_key)
    # print(
    #     f"Key: [{test_key}] Exists in cache (should be False): {test_cache.check_key_exists(test_key)}"
    # )

    # test_cache.set_expire(key=test_key, expire=2)
    # print(f"Wait 2.5 seconds to allow key to expire...")
    # time.sleep(2.5)
    # print(
    #     f"Key: [{test_key}] Exists in cache (should be False): {test_cache.check_key_exists(test_key)}"
    # )

    # print(f"Cache size: {test_cache.get_cache_size()}")
    print(f"Cache warnings: {test_cache.check_cache()}")
