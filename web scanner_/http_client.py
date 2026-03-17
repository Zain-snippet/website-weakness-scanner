from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from http.client import HTTPResponse
from http.cookies import SimpleCookie
from typing import List, Union

from models import HttpSnapshot, CookieSnapshot


def send_request(url: str) -> Union[HttpSnapshot, None]:
    """
    Send an HTTP/HTTPS request to the given URL.
    Returns a HttpSnapshot object on success, None on failure.
    """
    try:
        req = Request(url, headers={"User-Agent": "SmartScanner/1.0"})
        with urlopen(req, timeout=10) as resp:  # type: HTTPResponse
            body = resp.read()  # bytes

            # Decode body safely
            try:
                body_str = body.decode("utf-8")
            except UnicodeDecodeError:
                body_str = body.decode("latin1")

            # Headers
            headers = dict(resp.getheaders())

            # Cookies → convert to CookieSnapshot
            cookies_list: List[CookieSnapshot] = []

            if "Set-Cookie" in headers:
                cookie_header = headers["Set-Cookie"]
                simple_cookie = SimpleCookie()
                simple_cookie.load(cookie_header)

                for key, morsel in simple_cookie.items():
                    cookies_list.append(
                        CookieSnapshot(
                            name=key,
                            value=morsel.value,
                            secure=bool(morsel["secure"]),
                            httponly=bool(morsel["httponly"]),
                            samesite=morsel["samesite"] or None
                        )
                    )

            # IMPORTANT FIX:
            # Use final URL (after redirect), not input URL
            final_url = resp.geturl()
            is_https = final_url.startswith("https://")

            # Build snapshot
            response_data = HttpSnapshot(
                input_url=url,
                final_url=final_url,
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