import requests
import json


class MessagerClient:
    def __init__(self, page_id):
        self.page_id = page_id

    def send_message(self, user_id, message):
        requests.post('https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(self.page_id),
                      headers={'Content-Type': 'application/json'},
                      data=json.dumps({"recipient": {"id": user_id }, "message": {"text": message} }))
