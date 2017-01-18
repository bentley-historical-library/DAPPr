import requests
import json

class DAPPr:
    """
    DSpace [REST] API Python Programming [Language] resource (DAPPr), 
    a client to communicate with a remote DSpace installation 
    using its backend API."""

    def __init__(self, base_url, email, password, community_id):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.community_id = community_id

    def _login(self):
        url = self.base_url + "/RESTapi/login"
        body = {"email": self.email, "password": self.password}
        response = requests.post(url, json=body)

        token = response.text
        
        return token
        
    def _logout(self, token):
        url = self.base_url + "/RESTapi/logout"
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        response = requests.post(url, headers=headers)
        
    def get_collections(self):
        """
        Returns array of collections of community."""
        
        url = self.base_url + "/RESTapi/collections"
        response = requests.get(url)
        
        collections = response.json()
        
        return collections
        
    def get_collection(self, collection_id):
        """
        Return collection with id."""
        
        url = self.base_url + "/RESTapi/collections/" + str(collection_id)
        response = requests.get(url)
        
        collection = response.json()
        
        return collection
        
    def get_collection_items(self, collection_id):
        """
        Return all items of collection."""
        
        url = self.base_url + "/RESTapi/collections/" + str(collection_id) + "/items"
        response = requests.get(url)
        
        collection = response.json()
        
        return collection
        
    def post_collection_item(self, collection_id, item):
        """
        Create posted item in collection. You must post an Item"""
        
        token = self._login()
        
        url = self.base_url + "/RESTapi/collections/" + str(collection_id) + "/items"
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        body = item
        response = requests.post(url, headers=headers, json=body)
                
        self._logout(token)
        
    def put_collection(self, collection_id, collection):
        """
        Update collection. You must put Collection."""
        
        token = self._login()
        
        url = self.base_url + "/RESTapi/collections/" + str(collection_id)
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        body = collection
        response = requests.put(url, headers=headers, json=body)
        
        self._logout(token)
        
    def delete_collection(self, collection_id):
        """
        Delete collection from DSpace."""
        
        token = self._login()
        
        url = self.base_url + "/RESTapi/collections/" + str(collection_id)
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        response = requests.delete(url, headers=headers)
        
        self._logout(token)
        
    def delete_collection_item(self, collection_id, item_id):
        """
        Delete item in collection."""
        
        token = self._login()
        
        url = self.base_url + "/RESTapi/collections/" + str(collection_id) + "/items/" + str(item_id)
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        response = requests.delete(url, headers=headers)

        self._logout(token)    
        