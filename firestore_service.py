import os

import firebase_admin
from firebase_admin import credentials, firestore
from models import Post, Place

BATCH_LIMIT = 400


class FirestoreService:

    def __init__(self, path):
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.batch = self.db.batch()
        self.batch_counter = 0

    def commit_batch(self):
        self.batch.commit()
        self.batch_counter = 0

    def add_to_batch(self, doc_ref, data):
        self.batch.set(doc_ref, data)
        self.batch_counter += 1
        if self.batch_counter >= BATCH_LIMIT:
            self.commit_batch()

    def upload_place(self, place: Place):
        data = place.__dict__
        doc_ref = self.db.collection('places').document(str(place.id))
        self.add_to_batch(doc_ref, data)

    def upload_post(self, post: Post):
        data = post.__dict__
        doc_ref = self.db.collection('posts').document()
        self.add_to_batch(doc_ref, data)


SERVICE_ACCOUNT_KEY_PATH = os.path.join(os.path.dirname(__file__), "./secrets/serviceAccountKey.json")
app = FirestoreService(SERVICE_ACCOUNT_KEY_PATH)
