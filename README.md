# DAPPr

![Dapper men](https://images.nypl.org/index.php?id=5205109&t=w)

DSpace [REST] API Python Programming [Language] resource (DAPPr) is a client to communicate with a remote DSpace installation using its backend [API](https://wiki.duraspace.org/display/DSDOC5x/REST+API).

## Usage

Create a config.py file (currenlty ignored) with the following dictionaries:

    dev = {
        "base_url": STRING,
        "email": STRING,
        "password": STRING,
    }

    prod = {
        "base_url": STRING,
        "email": STRING,
        "password": STRING,
    }
    
In your script, create an object, e.g.:

    from dappr import DAPPr
    from config import dev

    deepblue = DAPPr(
        dev.get("base_url"),
        dev.get("email"),
        dev.get("password"), 
    )
    
Then, use the client to interact with the API...

### Communities

Communities in DSpace are used for organization and hierarchy, and are containers that hold sub-Communities and Collections.

  * `communities = deepblue.get_communities()`: Returns array of all communities in DSpace.
  * `top_communities = deepblue.get_top_communities()`: Returns array of all top communities in DSpace.
  * `community = deepblue.get_community(Community ID INTEGER)`: Returns community.
  * `collections = deepblue.get_community_collections(Community ID INTEGER)`: Returns array of collections of community.
  * `communities = deepblue.get_community_subcommunities(Community ID INTEGER)`: Returns array of subcommunities of community.
  * `community = deepblue.post_community(Community DICTIONARY)`: Create new community at top level. You must post community (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `collection = deepblue.post_community_collection(Community ID INTEGER, Collection DICTIONARY)`: Create new collections in community. You must post Collection (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `subcommunity = deepblue.post_community_subcommunity(Community ID INTEGER, Sub-Community DICTIONARY)`: Create new subcommunity in community. You must post Community (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `deepblue.put_community(Community ID INTEGER, Community DICTIONARY)`: Update community. You must put Community (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `deepblue.delete_community(Community ID INTEGER)`: Delete community.
  * `deepblue.delete_community_collection(Community ID INTEGER, Collection ID INTEGER)`: Delete collection in community.
  * `deepblue.delete_community_subcommunity(Community ID INTEGER, Sub-Community ID INTEGER)`: Delete subcommunity in community.

### Collections

Collections in DSpace are containers of Items.

  * `collections = deepblue.get_collections()`: Return all collections of DSpace in array.
  * `collection = deepblue.get_collection(Collection ID INTEGER)`: Return collection with id.
  * `items = deepblue.get_collection_items(Collection ID INTEGER)`: Return all items of collection.
  * `item = deepblue.post_collection_item(Collection ID INTEGER, Item DICTIONARY)`: Create posted item in collection. You must post an Item (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * TO-DO: Find collection by passed name.
  * `deepblue.put_collection(Collection ID INTEGER, Collection DICTIONARY)`: Update collection. You must put Collection (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `deepblue.delete_collection(Collection ID INTEGER)`: Delete collection from DSpace.
  * `deepblue.delete_collection_item(Collection ID INTEGER, Item ID INTEGER)`: Delete item in collection.

### Items

Items in DSpace represent a "work" and combine metadata and files, known as Bitstreams.

  * `items = deepblue.get_items()`: Return list of items.
  * `item = deepblue.get_item(Item ID INTEGER)`: Return item.
  * `metadata = deepblue.get_item_metadata(Item ID INTEGER)`: Return item metadata.
  * `bitstreams = deepblue.get_item_bitstreams(Item ID INTEGER)`: Return item bitstreams.
  * TO-DO: Find items by metadata entry. You must post a MetadataEntry.
  * `metadata = deepblue.post_item_metadata(Item ID INTEGER, Metdata LIST)`: Add metadata to item. You must post an array of MetadataEntry (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `bitstream = deepblue.post_item_bitstream(Item ID INTEGER, Bitstream PATH)`: Add bitstream to item. You must post a Bitstream (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `deepblue.put_item_metadata(Item ID Integer, Metadata LIST)`: Update metadata in item. You must put a MetadataEntry (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * 'deepblue.delete_item(Item ID INTEGER)`: Delete item.
  * 'deepblue.delete_item_metadata(Item ID INTEGER)` Clear item metadata.
  * 'deepblue.delete_item_bitstream(Item ID INTEGER, Bitstream ID INTEGER)` Delete item bitstream.
  
### Bitstreams

Coming soon!

### Handle

Coming soon!
