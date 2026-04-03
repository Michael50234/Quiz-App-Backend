import firebase_admin
from firebase_admin import credentials
import os
import json
from django.conf import settings

if not firebase_admin._apps:
    cred_dict = json.loads(os.getenv("CRED_DICT"))
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)