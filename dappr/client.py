import getpass
import humanize
import os
import requests
import sys
import urllib

if sys.version_info[:2] <= (2, 7):
    # Python 2
    get_input = raw_input
    import ConfigParser as configparser
    from urllib import quote
else:
    # Python 3
    get_input = input
    import configparser
    from urllib.parse import quote


class DSpaceError(Exception):
    pass


class DAPPr(object):
    """
    DSpace [REST] API Python Programming [Language] resource (DAPPr),
    a client to communicate with a remote DSpace installation
    using its backend API."""

    def __init__(self, base_url=None, email=None, password=None, instance_name=None):
        if base_url and email and password:
            self.base_url = base_url
            self.email = email
            password = password
        else:
            self.config_file = os.path.join(os.path.expanduser("~"), ".dappr")
            configuration = self._load_config(instance_name)
            self.base_url = configuration["base_url"]
            self.email = configuration["email"]
            password = configuration.get("password")
            if not password:
                password = getpass.getpass("Password: ")
            self._parse_groups(configuration)
        self._login(password)

    def _load_config(self, instance_name):
        config = configparser.RawConfigParser()
        config.read(self.config_file)
        instances = config.sections()
        if len(instances) == 0:
            print("No DSpace instances configured. Configure an instance? (y/n)")
            configure = get_input(": ")
            if configure.lower().strip() in ["y", "yes"]:
                configuration = self._add_instance(config)
                return configuration
            else:
                sys.exit()
        elif instance_name and instance_name in instances:
            configuration = {key: value for (key, value) in config.items(instance_name)}
            return configuration
        else:
            instance_mapping = {}
            instance_number = 0
            print("*** CONFIGURED DSPACE INSTANCES ***")
            for instance in instances:
                instance_number += 1
                instance_mapping[str(instance_number)] = instance
                instance_url = config.get(instance, "base_url")
                email = config.get(instance, "email")
                print("{} - {} [{}, {}]".format(instance_number, instance, instance_url, email))
            print("A - Add Instance")
            option = get_input("Select an instance: ")
            if option.strip() in instance_mapping.keys():
                instance = instance_mapping[option]
                configuration = {key: value for (key, value) in config.items(instance)}
                return configuration
            elif option.lower().strip() == "a":
                configuration = self._add_instance(config)
                return configuration
            else:
                sys.exit()

    def _parse_groups(self, configuration):
        self.groups = {}
        group_keys = [key for key in configuration.keys() if (key.startswith("group_") and key.endswith("_id"))]
        if any(group_keys):
            group_names = list(set([group_key.replace("group_", "").replace("_id", "").strip() for group_key in group_keys]))
            for group_name in group_names:
                group_key_prefix = "group_{}".format(group_name)
                group_id = configuration["{}_id".format(group_key_prefix)]
                group_description = configuration["{}_description".format(group_key_prefix)]
                group_long_name = configuration["{}_long_name".format(group_key_prefix)]
                group_metadata = {"description": group_description, "group_id": group_id, "long_name": group_long_name}
                self.groups[group_name] = group_metadata

    def _save_config(self, config):
        with open(self.config_file, "w") as f:
            config.write(f)

    def _add_instance(self, config):
        instance_name = get_input("Instance name: ")
        base_url = get_input("Base URL: ")
        email = get_input("Email: ")
        store_password = get_input("Store a password for this instance? (y/n) ")
        if store_password.lower().strip() in ["y", "yes"]:
            password = getpass.getpass("Enter password: ")
        else:
            password = False
        config.add_section(instance_name)
        config.set(instance_name, "base_url", base_url)
        config.set(instance_name, "email", email)
        if password:
            config.set(instance_name, "password", password)
        add_groupIds = get_input("Would you like to add groupIds for this instance? (y/n) ")
        while add_groupIds.lower().strip() in ["y", "yes"]:
            group_name_long = get_input("Enter a long name for the group (e.g., Bentley Only Users): ")
            group_name = get_input("Enter a short name for the group (e.g., um_users): ")
            print("Enter a description for the group")
            print("Example: Archival materials. Access restricted to Bentley Reading Room.")
            group_description = get_input("Description: ")
            group_id = get_input("Enter the groupId for the group in DSpace (e.g., 474): ")
            group_name_prefix = "group_{}".format(group_name)
            config.set(instance_name, "{}_long_name".format(group_name_prefix), group_name_long)
            config.set(instance_name, "{}_id".format(group_name_prefix), group_id)
            config.set(instance_name, "{}_description".format(group_name_prefix), group_description)
            add_groupIds = get_input("Add another groupId for this instance? (y/n) ")
        self._save_config(config)
        return {key: value for (key, value) in config.items(instance_name)}

    def _login(self, password):
        url = self.base_url + "/RESTapi/login"
        body = {"email": self.email, "password": password}
        response = requests.post(url, json=body)
        if response.status_code == 200:
            self.session = requests.Session()
            token = response.text
            self.session.headers.update({"rest-dspace-token": token})
        else:
            raise DSpaceError("Error logging in - {}".format(response.text))

    def _request(self, method, url, params={}, expected_response=200, data=None, json=None, json_expected=True):
        response = method(url, params=params, data=data, json=json)
        if response.status_code != expected_response:
            raise DSpaceError("DSpace server responded with {}. Expected {}".format(response.status_code, expected_response))

        if json_expected:
            try:
                response.json()
            except Exception:
                raise DSpaceError("DSpace server responded with status {}, but returned a non-JSON document".format(response.status_code))

        return response

    def _get(self, endpoint, params={}, expected_response=200, json_expected=True):
        url = self.base_url + endpoint
        params["expand"] = "all"
        params["limit"] = 1000000
        response = self._request(self.session.get, url, params=params, expected_response=expected_response, json_expected=json_expected)
        return response

    def _post_json(self, endpoint, params={}, expected_response=200, json_expected=True, json=None):
        url = self.base_url + endpoint
        self.session.headers.update({"Accept": "application/json"})
        response = self._request(self.session.post, url, params=params, json=json, expected_response=expected_response, json_expected=json_expected)
        return response

    def _post_data(self, endpoint, params={}, expected_response=200, json_expected=True, data=None):
        url = self.base_url + endpoint
        self.session.headers.update({"Accept": "application/json"})
        response = self._request(self.session.post, url, data=data, expected_response=expected_response, json_expected=json_expected)
        return response

    def _post_big_data(self, endpoint, params={}, expected_response=200, json_expected=True, data=None, path=None):
        url = self.base_url + endpoint
        self.session.headers.update({
                                    "Accept": "application/json",
                                    "Content-Type": "multipart/form-data",
                                    "Content-Disposition": "attachment; filename=%s" % quote(os.path.basename(path))
                                    })
        
        response = self._request(self.session.post, url, data=data, expected_response=expected_response, json_expected=json_expected)
        del self.session.headers["Content-Type"]
        del self.session.headers["Content-Disposition"]
        return response

    def _put(self, endpoint, json=None, expected_response=200, json_expected=False):
        url = self.base_url + endpoint
        self.session.headers.update({"Accept": "application/json"})
        response = self._request(self.session.put, url, json=json, expected_response=expected_response, json_expected=json_expected)
        return response

    def _delete(self, endpoint, expected_response=200, json_expected=True):
        url = self.base_url + endpoint
        self.session.headers.update({"Accept": "application/json"})
        response = self._request(self.session.delete, url, expected_response=expected_response, json_expected=json_expected)
        return response

    # public functions
    def logout(self):
        endpoint = "/RESTapi/logout"
        self._post_json(endpoint, json_expected=False)

    # communities
    def get_communities(self):
        """
        Returns array of all communities in DSpace."""

        endpoint = "/RESTapi/communities"
        response = self._get(endpoint)
        return response.json()

    def get_top_communities(self):
        """
        Returns array of all top communities in DSpace."""

        endpoint = "/RESTapi/communities/top-communities"
        response = self._get(endpoint)
        return response.json()

    def get_community(self, community_id):
        """
        Returns community."""

        endpoint = "/RESTapi/communities/{}".format(community_id)
        response = self._get(endpoint)
        return response.json()

    def get_community_collections(self, community_id):
        """
        Returns array of collections of community."""

        endpoint = "/RESTapi/communities/{}/collections".format(community_id)
        response = self._get(endpoint)
        return response.json()

    def get_community_subcommunities(self, community_id):
        """
        Returns array of subcommunities of community."""

        endpoint = "/RESTapi/communities/{}/communities".format(community_id)
        response = self._get(endpoint)
        return response.json()

    def post_community(self, community_dictionary):
        """
        Create new community at top level. You must post community."""

        endpoint = "/RESTapi/communities/"
        response = self._post_json(endpoint, json=community_dictionary)
        return response.json()

    def post_community_collection(self, community_id, collection_dictionary):
        """
        Create new collections in community. You must post Collection."""

        endpoint = "/RESTapi/communities/{}/collections".format(community_id)
        response = self._post_json(endpoint, json=collection_dictionary)
        return response.json()

    def post_community_subcommunity(self, community_id, community_dictionary):
        """
        Create new subcommunity in community. You must post Community."""

        endpoint = "/RESTapi/communities/{}/communities".format(community_id)
        response = self._post_json(endpoint, json=community_dictionary)
        return response.json()

    def put_community(self, community_id, community_dictionary):
        """
        Update community. You must put Community"""

        endpoint = "/RESTapi/communities/{}".format(community_id)
        response = self._put(endpoint, json=community_dictionary)
        return response

    def delete_community(self, community_id):
        """
        Delete community."""

        endpoint = "/RESTapi/communities/{}".format(community_id)
        response = self._delete(endpoint)

        return response

    def delete_community_collection(self, community_id, collection_id):
        """
        Delete collection in community."""

        endpoint = "/RESTapi/communities/{}/collections/{}".format(community_id, collection_id)
        response = self._delete(endpoint)
        return response

    def delete_community_subcommunity(self, community_id, subcommunity_id):
        """
        Delete subcommunity in community."""

        endpoint = "/RESTapi/communities/{}/communities/{}".format(community_id, subcommunity_id)
        response = self._delete(endpoint)
        return response

    # collections
    def get_collections(self):
        """
        Returns array of collections of community."""

        endpoint = "/RESTapi/collections"
        response = self._get(endpoint)
        return response.json()

    def get_collection(self, collection_id):
        """
        Return collection with id."""

        endpoint = "/RESTapi/collections/{}".format(collection_id)
        response = self._get(endpoint)
        return response.json()

    def get_collection_items(self, collection_id):
        """
        Return all items of collection."""

        endpoint = "/RESTapi/collections/{}/items".format(collection_id)
        response = self._get(endpoint)
        return response.json()

    def post_collection_item(self, collection_id, item_dictionary):
        """
        Create posted item in collection. You must post an Item"""

        endpoint = "/RESTapi/collections/{}/items".format(collection_id)
        response = self._post_json(endpoint, json=item_dictionary)     
        return response.json()

    # TO-DO: Find collection by passed name.

    def put_collection(self, collection_id, collection_dictionary):
        """
        Update collection. You must put Collection."""

        endpoint = "/RESTapi/collections/{}".format(collection_id)
        response = self._put(endpoint, json=collection_dictionary)
        return response

    def delete_collection(self, collection_id):
        """
        Delete collection from DSpace."""

        endpoint = "/RESTapi/collections/{}".format(collection_id)
        response = self._delete(endpoint)
        return response

    def delete_collection_item(self, collection_id, item_id):
        """
        Delete item in collection."""

        endpoint = "/RESTapi/collections/{}/items/{}".format(collection_id, item_id)
        response = self._delete(endpoint)
        return response

    # items
    def get_items(self):
        """
        Return list of items."""

        endpoint = "/RESTapi/items"
        response = self._get(endpoint)
        return response.json()

    def get_item(self, item_id):
        """
        Return item."""

        endpoint = "/RESTapi/items/{}".format(item_id)
        response = self._get(endpoint)
        return response.json()

    def get_item_metadata(self, item_id):
        """
        Return item metadata."""

        endpoint = "/RESTapi/items/{}/metadata".format(item_id)
        response = self._get(endpoint)
        return response.json()

    def get_item_bitstreams(self, item_id):
        """
        Return item bitstreams."""

        endpoint = "/RESTapi/items/{}/bitstreams".format(item_id)
        response = self._get(endpoint)
        return response.json()

    # TO-DO: Find items by metadata entry. You must post a MetadataEntry.

    def post_item_metadata(self, item_id, metadata_list):
        """
        Add metadata to item. You must post an array of MetadataEntry"""

        endpoint = "/RESTapi/items/{}/metadata".format(item_id)
        response = self._post_json(endpoint, json=metadata_list, json_expected=False)
        return response

    def post_item_bitstream(self, item_id, bitstream_path):
        """
        Add bitstream to item. You must post a Bitstream"""

        endpoint = "/RESTapi/items/{}/bitstreams".format(item_id)
        with open(bitstream_path, "rb") as f:
            response = self._post_big_data(endpoint, data=f, path=bitstream_path)
        return response.json()

    def put_item_metadata(self, item_id, metadata_list):
        """
        Update metadata in item. You must put a MetadataEntry"""

        endpoint = "/RESTapi/items/{}/metadata".format(item_id)
        response = self._put(endpoint, json=metadata_list, json_expected=False)        
        return response

    def delete_item(self, item_id):
        """
        Delete item."""

        endpoint = "/RESTapi/items/{}".format(item_id)
        response = self._delete(endpoint)
        return response

    def delete_item_metadata(self, item_id):
        """
        Clear item metadata."""

        endpoint = "/RESTapi/items/{}/metadata".format(item_id)
        response = self._delete(endpoint, json_expected=False)
        return response

    def delete_item_bitstream(self, item_id, bitstream_id):
        """
        Delete item bitstream."""

        endpoint = "/RESTapi/items/{}/bitstreams/{}".format(bitstream_id)
        response = self._delete(endpoint)
        return response

    # bitstreams
    def get_bitstreams(self):
        """
        Return all bitstreams in DSpace."""

        endpoint = "/RESTapi/bitstreams"
        response = self._get(endpoint)
        return response.json()

    def get_bitstream(self, bitstream_id):
        """
        Return bitstream."""

        endpoint = "/RESTapi/bitstreams/{}".format(bitstream_id)
        response = self._get(endpoint)
        return response.json()

    def get_bitstream_policy(self, bitstream_id):
        """
        Return bitstream policies."""

        endpoint = "/RESTapi/bitstreams/{}/policy".format(bitstream_id)
        response = self._get(endpoint)
        return response.json()

    def get_bitstream_data(self, bitstream_id):
        """
        Return data of bitstream."""

        endpoint = "/RESTapi/bitstreams/{}/retrieve".format(bitstream_id)
        response = self._get(endpoint)
        return response

    def put_bitstream_policy(self, bitstream_id, policy_list):
        """
        Add policy to item. You must post a ResourcePolicy"""

        endpoint = "/RESTapi/bitstreams/{}".format(bitstream_id)
        bitstream = self._get(endpoint).json()
        bitstream["policies"] = policy_list
        response = self._put(endpoint, json=bitstream, json_expected=False)
        return response

    # TO-DO: Update data/file of bitstream. You must put the data

    def put_bitstream(self, bitstream_id, bitstream):
        """
        Update metadata of bitstream. You must put a Bitstream, does not alter the file/data"""

        endpoint = "/RESTapi/bitstreams/{}".format(bitstream_id)
        response = self._put(endpoint, json=bitstream, json_expected=False)        
        return response

    def delete_bitstream(self, bitstream_id):
        """
        Delete bitstream from DSpace."""

        endpoint = "/RESTapi/bitstreams/{}".format(bitstream_id)
        response = self._delete(endpoint)
        return response

    def delete_bitstream_policy(self, bitstream_id, policy_id):
        """
        Delete bitstream policy."""

        endpoint = "/RESTapi/bitstreams/{}/policy/{}".format(bitstream_id, policy_id)
        response = self._delete(endpoint)
        return response

    # handle
    def get_handle(self, handle):
        """
        Returns a Community, Collection, or Item object that matches that handle."""

        endpoint = "/RESTapi/handle/{}".format(handle)
        response = self._get(endpoint)
        return response.json()

    # bhl
    def _find_license_txt(self, supplied_filepath):
        if supplied_filepath:
            license_txt_filepath = supplied_filepath
        else:
            base_dir = os.path.abspath(os.path.dirname(__file__))
            license_txt_filepath = os.path.join(base_dir, "lib", "license.txt")

        if os.path.exists(license_txt_filepath):
            return license_txt_filepath
        else:
            raise DSpaceError("license.txt not found at {}. Supplied a valid filepath using the supplied_filepath parameter.".format(license_txt_filepath))

    def post_item_license(self, item_id, supplied_filepath=False):
        """
        Posts a license in a license bundle to an item."""

        license_txt = self._find_license_txt(supplied_filepath)
        endpoint = "/RESTapi/items/{}/bitstreams".format(item_id)
        with open(license_txt, "r") as f:
            bitstream = self._post_data(endpoint, data=f.read()).json()
            bitstream_id = bitstream["id"]
            bitstream['name'] = 'license.txt'
            bitstream['bundleName'] = 'LICENSE'
            bitstream_endpoint = "/RESTapi/bitstreams/{}".format(bitstream_id)
            response = self._put(bitstream_endpoint, json=bitstream)
            return response

    def embed_kaltura_videos(self, handle, kaltura_video_ids):
        """
        Embeds one or more Kaltura videos from the Bentley Digital Media Library into a DeepBlue item."""

        item = self.get_handle(handle)
        item_id = item['id']
        if item['type'] != 'item':
            raise DSpaceError("Not an item!")
        metadata = self.get_item_metadata(item_id)    
        kaltura_player = 1455309001
        for kaltura_video_id in kaltura_video_ids:
            value = "https://cdnapisec.kaltura.com/p/1758271/sp/175827100/embedIframeJs/uiconf_id/29300931/partner_id/1758271?autoembed=true&entry_id=" + kaltura_video_id + "&playerId=kaltura_player_" + str(kaltura_player) + "&cache_st=1455309475&width=400&height=330&flashvars[streamerType]=auto"
            kaltura_player += 1
            metadata.append({"key": "dc.identifier.videostream", "value": value})
        response = self.put_item_metadata(item_id, metadata)
        return response

    def get_metadata_entry_by_key(self, metadata, key):
        entries = [entry for entry in metadata if entry["key"] == key]
        if len(entries) == 1:
            return entries[0]
        else:
            raise DSpaceError("Returned {} results for {} in {}".format(len(entries), key, metadata))

    def get_metadata_entry_value_by_key(self, metadata, key):
        entry = self.get_metadata_entry_by_key(metadata, key)
        return entry["value"]

    def update_metadata_entry_by_key(self, metadata, key, value):
        entry = self.get_metadata_entry_by_key(metadata, key)
        entry["value"] = value

    def more_title_context(self, handle):
        """
        Adds one ancestor from dc.relation.ispartofseries to the title and takes on away from the dc.relation.ispartofseries."""

        item = self.get_handle(handle)
        item_id = item['id']
        if item['type'] != 'item':
            sys.exit("Not an item!")
        metadata = self.get_item_metadata(item_id)
        title = self.get_metadata_entry_value_by_key(metadata, "dc.title")
        relation = self.get_metadata_entry_value_by_key(metadata, "dc.relation.ispartofseries")
        more_title_context = relation.split(' - ')[-1] + ' - ' + title
        less_relation_context = ' - '.join(relation.split(' - ')[:-1])
        self.update_metadata_entry_by_key(metadata, "dc.title", more_title_context)
        self.update_metadata_entry_by_key(metadata, "dc.relation.ispartofseries", less_relation_context)
        response = self.put_item_metadata(item_id, metadata)
        return response

    def get_collection_extent_by_series(self, collection_id):
        """
        Returns a dictionary with the extent for each series."""
        items = self.get_collection_items(collection_id)

        series_extent = {}
        for item in items:
            metadata = item['metadata']
            relation = self.get_metadata_entry_value_by_key(metadata, "dc.relation.ispartofseries")
            series = relation.split(" - ")[0].strip()          
            size_bytes = 0
            bitstreams = item['bitstreams']
            for bitstream in bitstreams:
                size_bytes += bitstream['sizeBytes']
            series_extent[series] = series_extent.get(series, 0) + size_bytes

        for series, extent in series_extent.items():
            series_extent[series] = humanize.naturalsize(extent)

        return series_extent

    def get_item_extent(self, item):
        size_bytes = 0
        bitstreams = item.get("bitstreams")
        for bitstream in bitstreams:
            size_bytes += bitstream.get("sizeBytes")
        return size_bytes

    def get_collection_extent(self, collection):
        size_bytes = 0
        items = collection.get("items")
        for item in items:
            item_id = item["id"]
            item_json = self.get_item(item_id)
            size_bytes += self.get_item_extent(item_json)
        return size_bytes

    def get_community_extent(self, community):
        size_bytes = 0
        collections = community.get("collection")
        for collection in collections:
            collection_id = collection["id"]
            collection_json = self.get_collection(collection_id)
            size_bytes += self.get_collection_extent(collection_json)

        subcommunities = community.get("subcommunities")
        for subcommunity in subcommunities:
            subcommunity_id = subcommunity["id"]
            subcommunity_json = self.get_community(subcommunity_id)
            subcommunity_collections = subcommunity_json.get("collections")
            for subcommunity_collection in subcommunity_collections:
                subcommunity_collection_id = subcommunity_collection["id"]
                subcommunity_collection_json = self.get_collection(subcommunity_collection_id)
                size_bytes += self.get_collection_extent(subcommunity_collection_json)

        return size_bytes

    def get_handle_extent(self, handle):
        """
        Returns the total sizeBytes for all Bitstreams on an Item, all Bitstreams on all Items in a Collection, or all Bitstreams on all Items in all Collections (and all Bitstreams on all Items in all Collections in all Sub-Communities) in a Community."""

        handle = self.get_handle(handle)
        if handle.get("type") == "item":
            size_bytes = self.get_item_extent(handle)
        elif handle.get("type") == "collection":
            size_bytes = self.get_collection_extent(handle)
        elif handle.get("type") == "community":
            size_bytes = self.get_community_extent(handle)

        return humanize.naturalsize(size_bytes)
