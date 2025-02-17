# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "dynaconf",
#     "hishel",
#     "httpx",
#     "red-utils[httpx]",
# ]
#
# [tool.uv.sources]
# red-utils = { path = "../../" }
# ///

from red_utils.ext import httpx_utils

URL: str = "https://api.ipify.org"
USE_CACHE: bool = True
HEADERS: dict = {
    "User-Agent": "python red-utils",
    "Accept": "application/json,text/plain,text/html",
}


def main(url: str, use_cache: bool = False, headers: dict = {}) -> None:
    req = httpx_utils.build_request(
        url=url,
        headers=headers,
    )

    try:
        with httpx_utils.get_http_controller(use_cache=use_cache) as http_ctl:
            res = http_ctl.client.send(request=req)
            print(f"Response: [{res.status_code}: {res.reason_phrase}]: {res.text}")
    except Exception as exc:
        msg = f"({type(exc)}) Error sending request. Details: {exc}"
        print(f"[ERROR] {msg}")

        raise


if __name__ == "__main__":
    main(url=URL, use_cache=USE_CACHE, headers=HEADERS)
