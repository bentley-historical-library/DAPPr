# DAPPr

![Dapper men](https://images.nypl.org/index.php?id=5205109&t=w)

DSpace [REST] API Python Programming [Language] resource (DAPPr) is a client to communicate with a remote DSpace installation using its backend [API](https://wiki.duraspace.org/display/DSDOC5x/REST+API).

## Usage

Create a config.py file (currenlty ignored) with the following dictionaries:

    dev = {
        "base_url": string,
        "email": string,
        "password": string,
    }

    prod = {
        "base_url": string,
        "email": string,
        "password": string,
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

### Collections

Collections in DSpace are containers of Items.

  * `collections = deepblue.get_collections()`: Return all collections of DSpace in array.
  * `collection = deepblue.get_collection(Collection ID *integer*)`: Return collection with id.
  * `items = deepblue.get_collection_items(Collection ID *integer*)`: Return all items of collection.
  * `deepblue.post_collection_item(Collection ID *integer*, Item *dictionary*)`: Create posted item in collection. You must post an Item (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * TO-DO: `deepblue.find_collection(Collection Name *string*): Find collection by passed name.
  * `deepblue.put_collection(Collection ID *integer*, Collection *dictionary*)`: Update collection. You must put Collection (see [Model - Object data types](https://wiki.duraspace.org/display/DSDOC5x/REST+API#RESTAPI-Model-Objectdatatypes)).
  * `deepblue.delete_collection(Collection ID *integer*)`: Delete collection from DSpace.
  * `deepblue.delete_collection_item(Collection ID *integer*, Item ID *integer*)`: Delete item in collection.

### Items

Coming soon!

### Bitstreams

Coming soon!

### Handle

Coming soon!
