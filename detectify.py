import requests
import hmac
import hashlib
import json
import os

from base64 import b64encode, b64decode
from datetime import datetime

ENDPOINT = "https://api.detectify.com/rest"
api_key = os.getenv("API_KEY")
api_secret_key = os.getenv("API_SECRET_KEY")


def send_post_request(data: dict or None, path: str, url: str) -> dict or None:
    timestamp = str(int(datetime.now().timestamp()))

    if data:
        headers = make_headers("POST", path, timestamp, json.dumps(data))
        req = requests.post(url, headers=headers, data=json.dumps(data))
    else:
        headers = make_headers("POST", path, timestamp, None)
        req = requests.post(url, headers=headers, data=None)

    try:
        req.raise_for_status()
    except Exception as e:
        print(e)
        return None

    print(f"Status code: {req.status_code} | Raw response: {req.json()}")
    return req.json()


def send_put_request(data: dict or None, path: str, url: str) -> dict or None:
    timestamp = str(int(datetime.now().timestamp()))

    if data:
        headers = make_headers("PUT", path, timestamp, json.dumps(data))
        req = requests.put(url, headers=headers, data=json.dumps(data))
    else:
        headers = make_headers("PUT", path, timestamp, None)
        req = requests.put(url, headers=headers, data=None)

    try:
        req.raise_for_status()
    except Exception as e:
        print(e)
        return None

    print(f"Status code: {req.status_code} | Raw response: {req.json()}")
    return req.json()


def send_get_request(path: str, url: str) -> dict or None:
    timestamp = str(int(datetime.now().timestamp()))

    headers = make_headers("GET", path, timestamp, None)
    req = requests.get(url, headers=headers)

    try:
        req.raise_for_status()
    except Exception as e:
        print(e)
        return None

    # print(f"Status code: {req.status_code} | Raw response: {req.json()}")
    # print(json.dumps(req.json()))
    return req.json()


def send_delete_request(path: str, url: str) -> dict or None:
    timestamp = str(int(datetime.now().timestamp()))

    headers = make_headers("DELETE", path, timestamp, None)
    req = requests.delete(url, headers=headers)

    try:
        req.raise_for_status()
    except Exception as e:
        print(e)
        return None

    print(f"Status code: {req.status_code} | Raw response: {req.json()}")
    return req.json()


def make_headers(method: str, path: str, timestamp: str, body: str = None):
    method = method.upper()
    signature = make_signature(method, path, timestamp, body)
    return {
        "X-Detectify-Key": api_key,
        "X-Detectify-Signature": signature,
        "X-Detectify-Timestamp": timestamp,
    }


def make_signature(method: str, path: str, timestamp: str, body: str = None):
    msg = f"{method};{path};{api_key};{timestamp};"
    if body:
        msg += f"{body}"

    secret = b64decode(api_secret_key)
    signature = hmac.new(
        secret, msg=bytes(msg, "utf=8"), digestmod=hashlib.sha256
    ).digest()

    b64_sig = b64encode(signature)
    return b64_sig.decode("utf-8")


def _create_add_domain_payload(domain: str) -> dict:
    data = {"name": f"{domain}"}
    return data


def add_domain(domain: str):
    path = "/v2/domains/"
    url = f"{ENDPOINT}{path}"
    data = _create_add_domain_payload(domain)
    send_post_request(data, path, url)


def _add_scan_profile_payload(scan_profile: str) -> dict:
    return {"endpoint": scan_profile, "unique": True}


def add_scan_profile(scan_profile: str) -> str or None:
    path = "/v2/profiles/"
    url = f"{ENDPOINT}{path}"
    data = _add_scan_profile_payload(scan_profile)
    resp = send_post_request(data, path, url)
    if resp is not None:
        scan_profile_token = resp.get("token", None)
        return scan_profile_token

    return None


def start_scan(scan_profile_token: str):
    path = f"/v2/scans/{scan_profile_token}/"
    url = f"{ENDPOINT}{path}"
    resp = send_post_request(None, path, url)
    if resp is not None:
        print(resp)

# ADDED


def get_scan_profiles() -> dict:
    path = "/v2/profiles/"
    url = f"{ENDPOINT}{path}"
    resp = send_get_request(path, url)
    return resp


#  get the latest full report with high severity only
def get_latest_full_report(scan_profile_token: str) -> dict:
    path = f"/v2/fullreports/{scan_profile_token}/latest/"
    param = "?severity=high"
    url = f"{ENDPOINT}{path}{param}"
    resp = send_get_request(path, url)
    return resp


""""
# scripts starts here
if __name__ == "__main__":
    profiles = get_scan_profiles()  # get 2 scan profiles, check if they are verified (status:verified)
    for profile in profiles:
        if profile['status'] == "verified":
            profileName = profile['name']
            report = get_latest_full_report(profile['token'])
            if len(report['findings']) == 0:
                print("No findings!")
            else:
                for finding in report['findings']:
                    title = finding['title']
                    for scores in finding['score']:
                        if scores['version'] == "2.0":  # assumed there is only one score with version 2.0
                            score = scores['score']
                    found_at = finding['found_at']
                    date = finding['timestamp'].split("T")[0]
                    print(profileName, title, score, found_at, date)
"""