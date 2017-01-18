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
    
    
    # methods    
    def _get(self, endpoint):
        url = self.base_url + endpoint
        response = requests.get(url)
        
        try:
            return response
        except:
            print "Error GETting " + endpoint
            exit()
        
    def _post(self, endpoint, token, body):
        url = self.base_url + endpoint
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        response = requests.post(url, headers=headers, json=body)
        
        try:
            return response
        except:
            print "Error POSTing " + str(body) + " to " + endpoint
            exit()
        
    def _put(self, endpoint, token, body):
        url = self.base_url + endpoint
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        response = requests.put(url, headers=headers, json=body)
        
        try:
            return response
        except:
            print "Error PUTting " + str(body) + " to " + endpoint
            exit()
        
    def _delete(self, endpoint, token):
        url = self.base_url + endpoint
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        response = requests.delete(url, headers=headers)
        
        try:
            return response
        except:
            print "Error DELETEing " + endpoint
            exit()
        
    # communities
    def get_communities(self):
        """
        Returns array of all communities in DSpace."""
        
        response = self._get("/RESTapi/communities")
        communities = response.json()
        
        return communities
        
    def get_top_communities(self):
        """
        Returns array of all top communities in DSpace."""
        
        response = self._get("/RESTapi/communities/top-communities")        
        top_communities = response.json()
        
        return top_communities
        
    def get_community(self, community_id):
        """
        Returns community."""
        
        response = self._get("/RESTapi/communities/" + str(community_id))
        community = response.json()
        
        return community
        
    def get_community_collections(self, community_id):
        """
        Returns array of collections of community."""
        
        response = self._get("/RESTapi/communities/" + str(community_id) + "/collections")
        collections = response.json()
        
        return collections
        
    def get_community_subcommunities(self, community_id):
        """
        Returns array of subcommunities of community."""
        
        response = self._get("/RESTapi/communities/" + str(community_id) + "/communities")
        communities = response.json()
        
        return communities
        
    def post_community(self, community):
        """
        Create new community at top level. You must post community."""
        
        token = self._login()
        response = self._post("/RESTapi/communities/", token, community)
        community = resonse.json()
        self._logout(token)
        
        return community
        
    def post_community_collection(self, community_id, collection):
        """
        Create new collections in community. You must post Collection."""
        
        token = self._login()
        response = self._post("/RESTapi/communities/" + str(community_id) + "/collections", token, collection)
        collection = resonse.json()
        self._logout(token)
        
        return collection
        
    def post_community_subcommunity(self, community_id, community):
        """
        Create new subcommunity in community. You must post Community."""

        token = self._login()
        response = self._post("/RESTapi/communities/" + str(community_id) + "/communities", token, community)
        subcommunity = response.json()
        self._logout(token)
        
        return subcommunity
        
    def put_community(self, community_id, community):
        """
        Update community. You must put Community"""
        
        token = self._login()
        response = self._put("/RESTapi/communities/" + str(community_id), token, community)
        community = response.json()
        self._logout(token)
        
        return community
        
    def delete_community(self, community_id):
        """
        Delete community."""
        
        token = self._login()
        response = self._delete("/RESTapi/communities/" + str(community_id), token)
        self._logout(token)
        
        return response
        
    def delete_community_collection(self, community_id, collection_id):
        """
        Delete collection in community."""
        
        token = self._login()
        response = self._delete("/RESTapi/communities/" + str(community_id) + "/collections/" + str(collection_id), token)
        self._logout(token)
        
        return response
        
    def delete_community_subcommunity(self, community_id, subcommunity_id):
        """
        Delete subcommunity in community."""
        
        token = self._login()
        response = self._delete("/RESTapi/communities/" + str(community_id) + "/communities/" + str(subcommunity_id), token)
        self._logout(token)
        
        return response
        
        
    # collections
    def get_collections(self):
        """
        Returns array of collections of community."""
        
        response = self._get("/RESTapi/collections")
        collections = response.json()
        
        return collections
        
    def get_collection(self, collection_id):
        """
        Return collection with id."""
        
        response = self._get("/RESTapi/collections/" + str(collection_id))
        collection = response.json()
        
        return collection
        
    def get_collection_items(self, collection_id):
        """
        Return all items of collection."""
        
        response = self._get("/RESTapi/collections/" + str(collection_id) + "/items")
        items = response.json()
        
        return items
        
    def post_collection_item(self, collection_id, item):
        """
        Create posted item in collection. You must post an Item"""
        
        token = self._login()
        response = self._post("/RESTapi/collections/" + str(collection_id) + "/items", token, item)     
        item = response.json()
        self._logout(token)
        
        return item
        
    # TO-DO: Find collection by passed name.
        
    def put_collection(self, collection_id, collection):
        """
        Update collection. You must put Collection."""
        
        token = self._login()
        response = self._put("/RESTapi/collections/" + str(collection_id), token, collection)
        collection = response.json()
        self._logout(token)
        
        return collection
        
    def delete_collection(self, collection_id):
        """
        Delete collection from DSpace."""
        
        token = self._login()
        response = self._delete("/RESTapi/collections/" + str(collection_id), token)
        self._logout(token)
        
        return response
        
    def delete_collection_item(self, collection_id, item_id):
        """
        Delete item in collection."""
        
        token = self._login()
        response = self._delete("/RESTapi/collections/" + str(collection_id) + "/items/" + str(item_id), token)
        self._logout(token)
        
        return response
    