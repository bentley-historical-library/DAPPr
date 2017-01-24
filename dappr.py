import requests
import json
import os

class DAPPr:
    """
    DSpace [REST] API Python Programming [Language] resource (DAPPr), 
    a client to communicate with a remote DSpace installation 
    using its backend API."""

    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password    

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
        
        if response.status_code == 200:
            return response
        else:
            print "Error (" + str(response.status_code) + ") GETting " + endpoint
            exit()
        
    def _post_json(self, endpoint, token, json):
        url = self.base_url + endpoint
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        response = requests.post(url, headers=headers, json=json)
        
        if response.status_code == 200:
            return response
        else:
            print "Error (" + str(response.status_code) + ") POSTing " + str(json) + " to " + endpoint
            exit()
            
    def _post_data(self, endpoint, token, path):
        url = self.base_url + endpoint
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        with open(os.path.join(path), mode="r") as f:
            data = f.read()
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            return response
        else:
            print "Error (" + str(response.status_code) + ") POSTing " + str(path) + " to " + endpoint
            exit()
        
    def _put(self, endpoint, token, json):
        url = self.base_url + endpoint
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        response = requests.put(url, headers=headers, json=json)
        
        if response.status_code == 200:
            return response
        else:
            print "Error PUTting (" + str(response.status_code) + ") " + str(json) + " to " + endpoint
            exit()
        
    def _delete(self, endpoint, token):
        url = self.base_url + endpoint
        headers = {
            "Accept": "application/json",
            "rest-dspace-token": token
        }
        response = requests.delete(url, headers=headers)
        
        if response.status_code == 200:
            return response
        else:
            print "Error DELETEing (" + str(response.status_code) + ") " + endpoint
            exit()
        
    # communities
    def get_communities(self):
        """
        Returns array of all communities in DSpace."""
        
        response = self._get("/RESTapi/communities")
        
        try:
            communities = response.json()
            return communities
        except:
            exit()
        
    def get_top_communities(self):
        """
        Returns array of all top communities in DSpace."""
        
        response = self._get("/RESTapi/communities/top-communities")        
        
        try:
            top_communities = response.json()
            return top_communities
        except:
            exit()
        
    def get_community(self, community_id):
        """
        Returns community."""
        
        response = self._get("/RESTapi/communities/" + str(community_id))
        
        try:
            community = response.json()
            return community
        except:
            exit()
        
    def get_community_collections(self, community_id):
        """
        Returns array of collections of community."""
        
        response = self._get("/RESTapi/communities/" + str(community_id) + "/collections")
        
        try:
            collections = response.json()
            return collections
        except:
            exit()
        
    def get_community_subcommunities(self, community_id):
        """
        Returns array of subcommunities of community."""
        
        response = self._get("/RESTapi/communities/" + str(community_id) + "/communities")
        
        try:
            subcommunities = response.json()
            return subcommunities
        except:
            exit()
        
    def post_community(self, community_dictionary):
        """
        Create new community at top level. You must post community."""
        
        token = self._login()
        response = self._post_json("/RESTapi/communities/", token, community_dictionary)
        self._logout(token)
        
        try:
            community = response.json()
            return community
        except:
            exit()
        
    def post_community_collection(self, community_id, collection_dictionary):
        """
        Create new collections in community. You must post Collection."""
        
        token = self._login()
        response = self._post_json("/RESTapi/communities/" + str(community_id) + "/collections", token, collection_dictionary)
        self._logout(token)
        
        try:
            collection = response.json()
            return collection
        except:
            exit()
        
    def post_community_subcommunity(self, community_id, community_dictionary):
        """
        Create new subcommunity in community. You must post Community."""

        token = self._login()
        response = self._post_json("/RESTapi/communities/" + str(community_id) + "/communities", token, community_dictionary)
        self._logout(token)
        
        try:
            community = response.json()
            return community
        except:
            exit()
        
    def put_community(self, community_id, community_dictionary):
        """
        Update community. You must put Community"""
        
        token = self._login()
        response = self._put("/RESTapi/communities/" + str(community_id), token, community_dictionary)
        self._logout(token)
        
        return response
        
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
        
        try:
            collections = response.json()
            return collections
        except:
            exit()
        
    def get_collection(self, collection_id):
        """
        Return collection with id."""
        
        response = self._get("/RESTapi/collections/" + str(collection_id))
        
        try:
            collection = response.json()
            return collection
        except:
            exit()
        
    def get_collection_items(self, collection_id):
        """
        Return all items of collection."""
        
        response = self._get("/RESTapi/collections/" + str(collection_id) + "/items")
        
        try:
            items = response.json()
            return items
        except:
            exit()
        
    def post_collection_item(self, collection_id, item_dictionary):
        """
        Create posted item in collection. You must post an Item"""
        
        token = self._login()
        response = self._post_json("/RESTapi/collections/" + str(collection_id) + "/items", token, item_dictionary)     
        self._logout(token)
        
        try:
            item = response.json()
            return item
        except:
            exit()
        
    # TO-DO: Find collection by passed name.
        
    def put_collection(self, collection_id, collection_dictionary):
        """
        Update collection. You must put Collection."""
        
        token = self._login()
        response = self._put("/RESTapi/collections/" + str(collection_id), token, collection_dictionary)
        self._logout(token)
        
        return response
        
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
        
    
    # items
    def get_items(self):
        """
        Return list of items."""
        
        response = self._get("/RESTapi/items")
        
        try:
            items = response.json()
            return items
        except:
            exit()
            
    def get_item(self, item_id):
        """
        Return item."""
        
        response = self._get("/RESTapi/items/" + str(item_id))
        
        try:
            item = response.json()
            return item
        except:
            exit()
    
    def get_item_metadata(self, item_id):
        """
        Return item metadata."""
        
        response = self._get("/RESTapi/items/" + str(item_id) + "/metadata")
        
        try:
            metadata = response.json()
            return metadata
        except:
            exit()
    
    def get_item_bitstreams(self, item_id):
        """
        Return item bitstreams."""
        
        response = self._get("/RESTapi/items/" + str(item_id) + "/bitstreams")
        
        try:
            bitstreams = response.json()
            return bitstreams
        except:
            exit()
            
    # TO-DO: Find items by metadata entry. You must post a MetadataEntry.
    
    def post_item_metadata(self, item_id, metadata_list):
        """
        Add metadata to item. You must post an array of MetadataEntry"""
        
        token = self._login()
        response = self._post_json("/RESTapi/items/" + str(item_id) + "/metadata", token, metadata_list)
        self._logout(token)
        
        try:
            metadata = response.json()
            return metadata
        except:
            exit()
            
    def post_item_bitstream(self, item_id, bitstream_path):
        """
        Add bitstream to item. You must post a Bitstream"""
        
        token = self._login()
        response = self._post_data("/RESTapi/items/" + str(item_id) + "/bitstreams", token, bitstream_path)
        self._logout(token)
        
        try:
            bitstream = response.json()
            return bitstream
        except:
            exit()
            
    def put_item_metadata(self, item_id, metadata_list):
        """
        Update metadata in item. You must put a MetadataEntry"""
        
        token = self._login()
        response = self._put("/RESTapi/items/" + str(item_id) + "/metadata", token, metadata_list)
        self._logout(token)
        
        return response
        
    def delete_item(self, item_id):
        """
        Delete item."""
        
        token = self._login()
        response = self._delete("/RESTapi/items/" + str(item_id), token)
        self._logout(token)
        
        return response
        
    def delete_item_metadata(self, item_id):
        """
        Clear item metadata."""
        
        token = self._login()
        response = self._delete("/RESTapi/items/" + str(item_id) + "/metadata", token)
        self._logout(token)
        
        return response
        
    def delete_item_bitstream(self, item_id, bitstream_id):
        """
        Delete item bitstream."""
        
        token = self._login()
        response = self._delete("/RESTapi/items/" + str(item_id) + "/bitstreams/" + str(bitstream_id), token)
        self._logout(token)
        
        return response
        
    # bitstreams
    def get_bitstreams(self):
        """
        Return all bitstreams in DSpace."""
        
        response = self._get("/RESTapi/bitstreams")
        
        try:
            bitstreams = response.json()
            return bitstreams
        except:
            exit()
            
    def get_bitstream(self, bitstream_id):
        """
        Return bitstream."""
        
        response = self._get("/RESTapi/bitstreams/" + str(bitstream_id))
        
        try:
            bitstream = response.json()
            return bitstream
        except:
            exit()
            
    def get_bitstream_policy(self, bitstream_id):
        """
        Return bitstream policies."""
        
        response = self._get("/RESTapi/bitstreams/" + str(bitstream_id) + "/policy")
        
        try:
            policy = response.json()
            return policy
        except:
            exit()
            
    # TO-DO: Return data of bitstream.
    
    def put_bitstream_policy(self, bitstream_id, policy_list):
        """
        Add policy to item. You must post a ResourcePolicy"""
        
        token = self._login()
        
        url = self.base_url + "/RESTapi/bitstreams/" + str(bitstream_id)
        response = requests.get(url)
        
        if response.status_code == 200:
            
            bitstream = response.json()
            bitstream["policies"] = policy_list
            
            url = self.base_url + "/RESTapi/bitstreams/" + str(bitstream_id)
            headers = {
                "Accept": "application/json",
                "rest-dspace-token": token
            }
            json = bitstream
            response = requests.put(url, headers=headers, json=json)
        
            if response.status_code == 200:
                return response
            else:
                print "Error PUTting (" + str(response.status_code) + ") " + str(json) + " to " + "/RESTapi/bitstreams/" + str(bitstream_id)
                exit()
            
        else:
            print "Error (" + str(response.status_code) + ") GETting " + "/RESTapi/bitstreams/" + str(bitstream_id)
            exit()
            
        self._logout(token)
    
    # TO-DO: Update data/file of bitstream. You must put the data
    
    def put_bitstream(self, bitstream_id, bitstream):
        """
        Update metadata of bitstream. You must put a Bitstream, does not alter the file/data"""
        
        token = self._login()
        response = self._put("/RESTapi/bitstreams/" + str(bitstream_id), token, bitstream)
        self._logout(token)
        
        return response
        
    def delete_bitstream(self, bitstream_id):
        """
        Delete bitstream from DSpace."""
        
        token = self._login()
        response = self._delete("/RESTapi/bitstreams/" + str(bitstream_id), token)
        self._logout(token)
        
        return response
        
    def delete_bitstream_policy(self, bitstream_id, policy_id):
        """
        Delete bitstream policy."""
        
        response = self._delete("/RESTapi/bitstreams/" + str(bitstream_id) + "/policy/" + str(policy_id), token)
        token = self._login()
        self._logout(token)
        
        return response
        
    # handle
    def get_handle(self, handle):
        """
        Returns a Community, Collection, or Item object that matches that handle."""
        
        response = self._get("/RESTapi/handle/" + handle)
        
        try:
            object = response.json()
            return object
        except:
            exit()
    