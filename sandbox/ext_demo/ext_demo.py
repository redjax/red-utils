from red_utils.ext import httpx_utils

if __name__ == "__main__":
    req = httpx_utils.build_request(method="GET", url="https://www.google.com")
    try:
        with httpx_utils.get_http_controller() as http_ctl:
            res = http_ctl.client.send(req)
            print(f"Response: [{res.status_code}: {res.reason_phrase}]: {res.text}")
    except Exception as exc:
        raise exc
