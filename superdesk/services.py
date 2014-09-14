

import logging


log = logging.getLogger(__name__)


class BaseService():
    '''
    Base service for all endpoints, defines the basic implementation
    for CRUD datalayer functionality.
    '''
    endpoint_name = None

    def __init__(self, backend=None, endpoint_name=None):
        self.backend = backend
        self.endpoint_name = endpoint_name

    def on_create(self, docs):
        pass

    def on_created(self, docs):
        pass

    def on_update(self, updates, original):
        pass

    def on_updated(self, updates, original):
        pass

    def on_replace(self, document, original):
        pass

    def on_replaced(self, document, original):
        pass

    def on_delete(self, doc):
        pass

    def on_deleted(self, doc):
        pass

    def create(self, docs, **kwargs):
        ids = self.backend.create(self.endpoint_name, docs, **kwargs)
        return ids

    def update(self, id, updates):
        res = self.backend.update(self.endpoint_name, id, updates)
        return res

    def replace(self, id, document):
        res = self.backend.replace(self.endpoint_name, id, document)
        return res

    def delete(self, lookup):
        res = self.backend.delete(self.endpoint_name, lookup)
        return res

    def find_one(self, req, **lookup):
        return self.backend.find_one(self.endpoint_name, req=req, **lookup)

    def get(self, req, lookup):
        return self.backend.get(self.endpoint_name, req=req, lookup=lookup)

    def post(self, docs, **kwargs):
        self.on_create(docs)
        ids = self.create(docs, **kwargs)
        self.on_created(docs)
        return ids

    def patch(self, id, updates):
        original = self.backend.find_one_in_base_backend(self.endpoint_name, req=None, _id=id)
        self.on_update(updates, original)
        res = self.update(id, updates)
        self.on_updated(updates, original)
        return res

    def put(self, id, document):
        original = self.backend.find_one_in_base_backend(self.endpoint_name, req=None, _id=id)
        self.on_replace(document, original)
        res = self.replace(id, document)
        self.on_replaced(document, original)
        return res

    def delete_action(self, lookup):
        if lookup:
            doc = self.backend.find_one_in_base_backend(self.endpoint_name, req=None, **lookup)
            self.on_delete(doc)
        res = self.delete(lookup)
        if lookup and doc:
            self.on_deleted(doc)
        return res
