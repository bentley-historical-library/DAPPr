# DAPPr

![Dapper men](https://images.nypl.org/index.php?id=5205109&t=w)

DSpace [REST] API Python Programming [Language] resource (DAPPr) is a client to communicate with a remote DSpace installation using its backend [API](https://wiki.duraspace.org/display/DSDOC5x/REST+API).

## Usage

Create a config.py file (currenlty ignored) with the following dictionaries:

    dev = {
        "base_url": string,
        "email": string,
        "password": string,
        "community_id": integer
    }

    prod = {
        "base_url": string,
        "email": string,
        "password": string,
        "community_id": integer
    }
    
In your script, create an object, e.g.:

    from dappr import DAPPr
    from config import dev

    deepblue = DAPPr(
        dev.get("base_url"),
        dev.get("email"),
        dev.get("password"), 
        dev.get("community_id")
    )
    
Then, use the client to interact with the API...

### Communities

Communities in DSpace are used for organization and hierarchy, and are containers that hold sub-Communities and Collections. (ex: Department of Engineering)

Coming soon!

### Collections

Collections in DSpace are containers of Items.
  * deepblue.get_collections(): Returns array of collections of community.
  * deepblue.get_collection(*integer*): Return collection with id.
  * deepblue.get_collection_items(*integer*): Return all items of collection.
  * deepblue.post_collection_item(*integer*, *dictionary*): Create posted item in collection. You must post an Item
  * deepblue.put_collection(*integer*, *dictionary*): Update collection. You must put Collection.
  * deepblue.delete_collection(*integer*): Delete collection from DSpace.
  * deepblue.delete_collection_item(*integer*, *integer*): Delete item in collection.

### Items

Items in DSpace represent a "work" and combine metadata and files, known as Bitstreams.

Coming soon!

### Bitstreams

Coming soon!

### Handle

Coming soon!
