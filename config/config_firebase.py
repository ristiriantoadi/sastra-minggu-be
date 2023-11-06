import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("./config/serviceAccountKey.json")

firebase_admin.initialize_app(cred, {"storageBucket": "library-dd644.appspot.com"})

bucket = storage.bucket()
