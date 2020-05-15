# DAPPr

![Dapper men](https://images.nypl.org/index.php?id=5205109&t=w)

DSpace [REST] API Python Programming [Language] resource (DAPPr) is a client to communicate with a remote DSpace 6.x installation using its backend [API](https://wiki.lyrasis.org/display/DSDOC6x/REST+API).

## Installation

`pip install git+https://github.com/bentley-historical-library/DAPPr.git`

## Usage

```python
from dappr import DAPPr
dspace = DAPPr()
```

The first time you call `DAPPr()`, you will be prompted to configure a DSpace instance, supplying a base URL, email address, and optionally a password and group IDs and descriptions. Configured instances are saved in a `.dappr` file in the user's home directory.

 Future calls to `DAPPr()` will prompt you to select one of the configured instances or give you the option to configure another instance (i.e., production and development). `DAPPr()` optionally takes an `instance_name` parameter to pre-select a configured instance, or `base_url`, `email`, and `password` parameters to log in without selecting a configured instance. 

### Groups
Any groups that are configured when setting up an instance are accessible through the `dspace.groups` variable. This functionality is primarily intended to assist with setting bitstream policies. The `dspace.groups` variable contains a dictionary of configured groups with keys of the group's configured "short name" and values of a dictionary containing a longer name for the group (`long_name`), a description of the access conditions set by the group (`description`), and the groups DSpace groupId (`group_id`).

```python
from dappr import DAPPr

dspace = DAPPr(instance_name="prod")
bhl_staff_group = dspace.groups["bhl_staff"]
bhl_staff_group_id = bhl_staff_group["group_id"]
bhl_staff_group_description = bhl_staff_group["description"]
```

### Communities

Communities in DSpace are used for organization and hierarchy, and are containers that hold sub-Communities and Collections.

  * `communities = dspace.get_communities()`: Returns array of all communities in DSpace.
  * `top_communities = dspace.get_top_communities()`: Returns array of all top communities in DSpace.
  * `community = dspace.get_community(Community UUID STRING)`: Returns community.
  * `collections = dspace.get_community_collections(Community UUID STRING)`: Returns array of collections of community.
  * `communities = dspace.get_community_subcommunities(Community UUID STRING)`: Returns array of subcommunities of community.
  * `community = dspace.post_community(Community DICTIONARY)`: Create new community at top level. You must post community (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `collection = dspace.post_community_collection(Community UUID STRING, Collection DICTIONARY)`: Create new collections in community. You must post Collection (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `subcommunity = dspace.post_community_subcommunity(Community UUID STRING, Sub-Community DICTIONARY)`: Create new subcommunity in community. You must post Community (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.put_community(Community UUID STRING, Community DICTIONARY)`: Update community. You must put Community (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.delete_community(Community UUID STRING)`: Delete community.
  * `dspace.delete_community_collection(Community UUID STRING, Collection UUID STRING)`: Delete collection in community.
  * `dspace.delete_community_subcommunity(Community UUID STRING, Sub-Community UUID STRING)`: Delete subcommunity in community.

### Collections

Collections in DSpace are containers of Items.

  * `collections = dspace.get_collections()`: Return all collections of DSpace in array.
  * `collection = dspace.get_collection(Collection UUID STRING)`: Return collection with UUID.
  * `items = dspace.get_collection_items(Collection UUID STRING)`: Return all items of collection.
  * `item = dspace.post_collection_item(Collection UUID STRING, Item DICTIONARY)`: Create posted item in collection. You must post an Item (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * TO-DO: Find collection by passed name.
  * `dspace.put_collection(Collection UUID STRING, Collection DICTIONARY)`: Update collection. You must put Collection (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.delete_collection(Collection UUID STRING)`: Delete collection from DSpace.
  * `dspace.delete_collection_item(Collection UUID STRING, Item UUID STRING)`: Delete item in collection.

### Items

Items in DSpace represent a "work" and combine metadata and files, known as Bitstreams.

  * `items = dspace.get_items()`: Return list of items.
  * `item = dspace.get_item(Item UUID STRING)`: Return item.
  * `metadata = dspace.get_item_metadata(Item UUID STRING)`: Return item metadata.
  * `bitstreams = dspace.get_item_bitstreams(Item UUID STRING)`: Return item bitstreams.
  * TO-DO: Find items by metadata entry. You must post a MetadataEntry.
  * `metadata = dspace.post_item_metadata(Item UUID STRING, Metdata LIST)`: Add metadata to item. You must post an array of MetadataEntry (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `bitstream = dspace.post_item_bitstream(Item UUID STRING, Bitstream PATH)`: Add bitstream to item. You must post a Bitstream (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.put_item_metadata(Item UUID STRING, Metadata LIST)`: Update metadata in item. You must put a MetadataEntry (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.delete_item(Item UUID STRING)`: Delete item.
  * `dspace.delete_item_metadata(Item UUID STRING)` Clear item metadata.
  * `dspace.delete_item_bitstream(Item UUID STRING, Bitstream UUID STRING)` Delete item bitstream.
  
### Bitstreams

In DSpace, Communities, Collections, and Items typically get minted a Handle Identifier. You can reference these objects in the REST API by their handle, as opposed to having to use the internal item-ID.

  * `bitstreams = dspace.get_bitstreams()`: Return all bitstreams in DSpace.
  * `bitstream = dspace.get_bitstream(Bitstream UUID STRING)`: Return bitstream.
  * `policy = dspace.get_bitstream_policy(Bitstream UUID STRING)`: Return bitstream policies.
  * TO-DO: Return data of bitstream.
  * `dspace.put_bitstream_policy(Bitsream UUID STRING, Policy LIST)`: Add policy to bitstream. You must post a ResourcePolicy (see "We have had success updating the bitstream policies at the bitstream endpoint rather than the policy endpoint You can just embed the policy JSON in the bitstream JSON as for example..." in [Setting a ResourcePolicy via REST API?](https://groups.google.com/forum/#!topic/dspace-tech/5uPhsbNkWek)).
  * TO-DO: Update data/file of bitstream. You must put the data
  * `dspace.put_bitstream(Bitstream UUID STRING, Bitstream DICTIONARY)`: Update metadata of bitstream. You must put a Bitstream, does not alter the file/data (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `dspace.delete_bitstream(Bitstream UUID STRING)`: Delete bitstream from DSpace.
  * `dspace.delete_bitstream_policy(Bitstream UUID STRING, Policy UUID STRING)`: Delete bitstream policy.

### Handle

In DSpace, Communities, Collections, and Items typically get minted a Handle Identifier. You can reference these objects in the REST API by their handle, as opposed to having to use the internal item-ID.

  * `object = dspace.get_handle(Handle STRING)`: Returns a Community, Collection, or Item object that matches that handle.
  
### BHL

Custom for the Bentley by the Bentley!

  * `bitstream = dspace.post_item_license(Item UUID STRING)`: Posts a license in a license bundle to an item.
  * `dspace.embed_kaltura_videos(Handle String, Kaltura ID LIST)`: Embeds one or more Kaltura videos from the Bentley Digital Media Library into a DeepBlue item.  
  * `extent = dspace.get_handle_extent(Handle STRING)`: Returns the total sizeBytes for all Bitstreams on an Item, all Bitstreams on all Items in a Collection, or all Bitstreams on all Items in all Collections (and all Bitstreams on all Items in all Collections in all Sub-Communities) in a Community.
  * `series_extent = dspace.get_collection_extent_by_series(Collection UUID STRING)`: Returns a dictionary with the extent for each series.
  * `dspace.more_title_context(Handle STRING)`: Adds one ancestor from `dc.relation.ispartofseries` to the title and takes on away from the `dc.relation.ispartofseries`. 

IMAGE  
[Dapper Men](https://dp.la/item/12e5d867c20e7d9c9824e06aa08f39aa?back_uri=https%3A%2F%2Fdp.la%2Fsearch%3Futf8%3D%25E2%259C%2593%26q%3Ddapper&next=4&previous=2)  
1912 - 1930  
Digitization funded with donations in memory of Olive Wong.  
[Get full image from Billy Rose Theatre Division. The New York Public Library](http://digitalcollections.nypl.org/items/169c51b0-3f63-0131-7ec5-58d385a7bbd0)
