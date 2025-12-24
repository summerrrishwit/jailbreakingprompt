import requests
import json
from toxigen.alice import beam_search
class GPT3(object):
    def __init__(self, endpoint_url, apikey):
        self.apikey = apikey
        self.endpoint_url = endpoint_url

    def __call__(self, prompt, topk=1, max_tokens=1):
        if not isinstance(prompt, list):
            prompt = [prompt]
        prompt = [p.replace("'", "").replace('"', "") for p in prompt]
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.9,
            "n": 1,
            "stream": False,
            "logprobs": topk,
            "stop": ["<|endoftext|>", "\\n"]
        }
        r = requests.post(self.endpoint_url,
            headers={
                "Authorization": f"Bearer {self.apikey}",
                "Content-Type": "application/json"
            },
            json = payload
        )       
        output = json.loads(r.content)
        return output

    def from_prompt(self, prompt, topk=10, max_tokens=10):
        output = self.__call__(prompt, topk, max_tokens)
        return output["choices"][0]["text"]

class ALICE(object):
    def __init__(self, language_model, classifier, mode, device="cpu"):
        self.classifier = classifier
        self.language_model = language_model
        self.device = device
        self.mode = mode

    def __call__(self, prompt):
        return self.generate(prompt)

# class VivoLLM(object):
#     APP_ID = '0599323503'
#     APP_KEY = 'ZTluHGficaycuHPV'
#     URI = '/chatgpt/completions'
#     DOMAIN = 'chatgpt-api.vivo.lan:8080'
#
#     def __init__(self, model='vivo-BlueLM-TB-Pro', provider='vivo'):
#         self.model = model
#         self.provider = provider
#
#     def gen_nonce(self, length=8):
#         import string
#         import random
#         chars = string.ascii_lowercase + string.digits
#         return ''.join([random.choice(chars) for _ in range(length)])
#
#     def gen_canonical_query_string(self, params):
#         import urllib.parse
#         s = ''
#         if params:
#             escape_uri = urllib.parse.quote
#             raw = []
#             for k in sorted(params.keys()):
#                 tmp_tuple = (escape_uri(k), escape_uri(str(params[k])))
#                 raw.append(tmp_tuple)
#             s = "&".join("=".join(kv) for kv in raw)
#         return s
#
#     def gen_signature(self, app_secret, signing_string):
#         import hmac
#         import hashlib
#         import base64
#         bytes_secret = app_secret.encode('utf-8')
#         hash_obj = hmac.new(bytes_secret, signing_string, hashlib.sha256)
#         bytes_sig = base64.b64encode(hash_obj.digest())
#         signature = str(bytes_sig, encoding='utf-8')
#         return signature
#
#     def gen_sign_headers(self, app_id, app_key, method, uri, query):
#         import time
#         method = str(method).upper()
#         timestamp = str(int(time.time()))
#         nonce = self.gen_nonce()
#         canonical_query_string = self.gen_canonical_query_string(query)
#         signed_headers_string = 'x-ai-gateway-app-id:{}\\nx-ai-gateway-timestamp:{}\\nx-ai-gateway-nonce:{}'.format(app_id, timestamp, nonce)
#         signing_string = '{}\\n{}\\n{}\\n{}\\n{}\\n{}'.format(method, uri, canonical_query_string, app_id, timestamp, signed_headers_string)
#         signing_string = signing_string.encode('utf-8')
#         signature = self.gen_signature(app_key, signing_string)
#         return {'X-AI-GATEWAY-APP-ID': app_id, 'X-AI-GATEWAY-TIMESTAMP': timestamp, 'X-AI-GATEWAY-NONCE': nonce,
#             'X-AI-GATEWAY-SIGNED-HEADERS': "x-ai-gateway-app-id;x-ai-gateway-timestamp;x-ai-gateway-nonce", 'X-AI-GATEWAY-SIGNATURE': signature}
#
#     def __call__(self, prompt, topk=1, max_tokens=100):
#         import requests
#         import uuid
#         import time
#         import traceback
#
#         if isinstance(prompt, list):
#             prompt = prompt[0]
#
#         try_time = 2
#         for i in range(try_time):
#             try:
#                 params = {'requestId': str(uuid.uuid4())}
#                 data = {
#                     'systemPrompt': '',
#                     'prompt': prompt,
#                     'task_type': 'chatgpt',
#                     'sessionId': str(uuid.uuid4()),
#                     'model': self.model,
#                     'provider': self.provider,
#                     'temperature': '0.1',
#                 }
#                 url = 'http://{}{}'.format(self.DOMAIN, self.URI)
#                 headers = self.gen_sign_headers(self.APP_ID, self.APP_KEY, 'POST', self.URI, params)
#                 response = requests.post(url, json=data, headers=headers, params=params, timeout=60)
#                 if response.status_code == 200:
#                     recv_data = response.json()
#                     return recv_data['data']['content']
#                 else:
#                     print(f'【{self.model} try {i+1} error')
#             except Exception as e:
#                 print(self.model)
#                 traceback.print_exc()
#                 time.sleep(0.1)
#         return 'request exception'

    def generate(self, prompt):
        if self.mode == "neutral":
            flag = 0
        else:
            flag = 1
        return beam_search(prompt, self.language_model, self.classifier, flag, self.device)
