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

    dspace = DAPPr(
        dev.get("base_url"),
        dev.get("email"),
        dev.get("password"), 
    )
    
Then, use the client to interact with the API...

### Communities

Communities in DSpace are used for organization and hierarchy, and are containers that hold sub-Communities and Collections.

  * `communities = dspace.get_communities()`: Returns array of all communities in DSpace.
  * `top_communities = dspace.get_top_communities()`: Returns array of all top communities in DSpace.
  * `community = dspace.get_community(Community ID INTEGER)`: Returns community.
  * `collections = dspace.get_community_collections(Community ID INTEGER)`: Returns array of collections of community.
  * `communities = dspace.get_community_subcommunities(Community ID INTEGER)`: Returns array of subcommunities of community.
  * `community = dspace.post_community(Community DICTIONARY)`: Create new community at top level. You must post community (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `collection = dspace.post_community_collection(Community ID INTEGER, Collection DICTIONARY)`: Create new collections in community. You must post Collection (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `subcommunity = dspace.post_community_subcommunity(Community ID INTEGER, Sub-Community DICTIONARY)`: Create new subcommunity in community. You must post Community (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.put_community(Community ID INTEGER, Community DICTIONARY)`: Update community. You must put Community (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.delete_community(Community ID INTEGER)`: Delete community.
  * `dspace.delete_community_collection(Community ID INTEGER, Collection ID INTEGER)`: Delete collection in community.
  * `dspace.delete_community_subcommunity(Community ID INTEGER, Sub-Community ID INTEGER)`: Delete subcommunity in community.

### Collections

Collections in DSpace are containers of Items.

  * `collections = dspace.get_collections()`: Return all collections of DSpace in array.
  * `collection = dspace.get_collection(Collection ID INTEGER)`: Return collection with id.
  * `items = dspace.get_collection_items(Collection ID INTEGER)`: Return all items of collection.
  * `item = dspace.post_collection_item(Collection ID INTEGER, Item DICTIONARY)`: Create posted item in collection. You must post an Item (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * TO-DO: Find collection by passed name.
  * `dspace.put_collection(Collection ID INTEGER, Collection DICTIONARY)`: Update collection. You must put Collection (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.delete_collection(Collection ID INTEGER)`: Delete collection from DSpace.
  * `dspace.delete_collection_item(Collection ID INTEGER, Item ID INTEGER)`: Delete item in collection.

### Items

Items in DSpace represent a "work" and combine metadata and files, known as Bitstreams.

  * `items = dspace.get_items()`: Return list of items.
  * `item = dspace.get_item(Item ID INTEGER)`: Return item.
  * `metadata = dspace.get_item_metadata(Item ID INTEGER)`: Return item metadata.
  * `bitstreams = dspace.get_item_bitstreams(Item ID INTEGER)`: Return item bitstreams.
  * TO-DO: Find items by metadata entry. You must post a MetadataEntry.
  * `metadata = dspace.post_item_metadata(Item ID INTEGER, Metdata LIST)`: Add metadata to item. You must post an array of MetadataEntry (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `bitstream = dspace.post_item_bitstream(Item ID INTEGER, Bitstream PATH)`: Add bitstream to item. You must post a Bitstream (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.put_item_metadata(Item ID Integer, Metadata LIST)`: Update metadata in item. You must put a MetadataEntry (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.delete_item(Item ID INTEGER)`: Delete item.
  * `dspace.delete_item_metadata(Item ID INTEGER)` Clear item metadata.
  * `dspace.delete_item_bitstream(Item ID INTEGER, Bitstream ID INTEGER)` Delete item bitstream.
  
### Bitstreams

In DSpace, Communities, Collections, and Items typically get minted a Handle Identifier. You can reference these objects in the REST API by their handle, as opposed to having to use the internal item-ID.

  * `bitstreams = dspace.get_bitstreams()`: Return all bitstreams in DSpace.
  * `bitstream = dspace.get_bitstream(Bitstream ID INTEGER)`: Return bitstream.
  * `policy = dspace.get_bitstream_policy(Bitstream ID INTEGER)`: Return bitstream policies.
  * TO-DO: Return data of bitstream.
  * `dspace.put_bitstream_policy(Bitsream ID INTEGER, Policy LIST)`: Add policy to item. You must post a ResourcePolicy (see "We have had success updating the bitstream policies at the bitstream endpoint rather than the policy endpoint You can just embed the policy JSON in the bitstream JSON as for example..." in [Setting a ResourcePolicy via REST API?](https://groups.google.com/forum/#!topic/dspace-tech/5uPhsbNkWek)).
  * TO-DO: Update data/file of bitstream. You must put the data
  * `dspace.put_bitstream(Bitstream ID INTEGER, Bitstream DICTIONARY)`: Update metadata of bitstream. You must put a Bitstream, does not alter the file/data (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.delete_bitstream(Bitstream ID)`: Delete bitstream from DSpace.
  * `dspace.delete_bitstream_policy(Bitstream ID INTEGER, Policy ID INTEGER)`: Delete bitstream policy.

### Handle

In DSpace, Communities, Collections, and Items typically get minted a Handle Identifier. You can reference these objects in the REST API by their handle, as opposed to having to use the internal item-ID.

  * `object = dspace.get_handle(Handle STRING)`: Returns a Community, Collection, or Item object that matches that handle.
  
### BHL

Custom for the Bentley by the Bentley!

  * `bitstream = dspace.post_item_license(Item ID INTEGER)`: Posts a license in a license bundle to an item.
  * `extent = dspace.get_handle_extent(Handle STRING)`: Returns the total sizeBytes for all Bitstreams on an Item, all Bitstreams on all Items in a Collection, or all Bitstreams on all Items in all Collections (and all Bitstreams on all Items in all Collections in all Sub-Communities) in a Community.
 

IMAGE  
[Dapper Men](https://dp.la/item/12e5d867c20e7d9c9824e06aa08f39aa?back_uri=https%3A%2F%2Fdp.la%2Fsearch%3Futf8%3D%25E2%259C%2593%26q%3Ddapper&next=4&previous=2)  
1912 - 1930  
Digitization funded with donations in memory of Olive Wong.  
[Get full image from Billy Rose Theatre Division. The New York Public Library](http://digitalcollections.nypl.org/items/169c51b0-3f63-0131-7ec5-58d385a7bbd0)
