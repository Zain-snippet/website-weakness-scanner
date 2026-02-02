from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from http.client import HTTPResponse
from http.cookies import SimpleCookie
from typing import List, Dict, Union
from models import ResponseData

def send_request(url: str) -> Union[ResponseData, None]:
    """
    Send an HTTP/HTTPS request to the given URL.
    Returns a ResponseData object on success, None on failure.
    """
    try:
        req = Request(url, headers={"User-Agent": "SmartScanner/1.0"})
        with urlopen(req, timeout=10) as resp:  # type: HTTPResponse
            body = resp.read()  # bytes
            # Try decoding as utf-8, fallback to latin1
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin1")

            # Collect headers
            headers = dict(resp.getheaders())

            # Collect cookies
            cookies_list: List[Dict[str, Union[str, bool]]] = []
            if "Set-Cookie" in headers:
                cookie_header = headers["Set-Cookie"]
                simple_cookie = SimpleCookie()
                simple_cookie.load(cookie_header)
                for key, morsel in simple_cookie.items():
                    cookies_list.append({
                        "name": key,
                        "value": morsel.value,
                        "secure": morsel["secure"] == "True",
                        "httponly": morsel["httponly"] == "True",
                        "samesite": morsel["samesite"] or None
                    })

            # Determine if HTTPS
            is_https = url.startswith("https://")

            response_data = ResponseData(
                input_url=url,
                final_url=resp.geturl(),
                status_code=resp.getcode(),
                headers=headers,
                cookies=cookies_list,
                body=body_str,
                is_https=is_https
            )

            return response_data

    except (HTTPError, URLError) as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error for {url}: {e}")
        return None