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
  * `deepblue.post_community()`: Create new community at top level. You must post community (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `deepblue.post_community_collection(Community ID INTEGER)`: Create new collections in community. You must post Collection (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `deepblue.post_community_subcommunity(Community ID INTEGER)`: Create new subcommunity in community. You must post Community (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).

### Collections

Collections in DSpace are containers of Items.

  * `collections = deepblue.get_collections()`: Return all collections of DSpace in array.
  * `collection = deepblue.get_collection(Collection ID INTEGER)`: Return collection with id.
  * `items = deepblue.get_collection_items(Collection ID INTEGER)`: Return all items of collection.
  * `deepblue.post_collection_item(Collection ID INTEGER, Item *dictionary*)`: Create posted item in collection. You must post an Item (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * TO-DO: `deepblue.find_collection(Collection Name STRING)`: Find collection by passed name.
  * `deepblue.put_collection(Collection ID INTEGER, Collection *dictionary*)`: Update collection. You must put Collection (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `deepblue.delete_collection(Collection ID INTEGER)`: Delete collection from DSpace.
  * `deepblue.delete_collection_item(Collection ID INTEGER, Item ID INTEGER)`: Delete item in collection.

### Items

Coming soon!

### Bitstreams

Coming soon!

### Handle

Coming soon!
