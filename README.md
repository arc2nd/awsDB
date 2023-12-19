# Setup

### Set your credentials:
In the creds folder you should find two JSON files: push_db_creds.json and 
push_s3_creds.json. You will want to copy these and remove the "push_" prefixes. 
Then you may alter them by filling in your database and aws information. Once 
your JSON files are in order it's time to encrypt them by running

    python creds/make_crypt.py
This will call awsDB.services.creds functions in order to encrypt these json files. 
It would now be safe to delete the source JSON files to better hide your database 
and aws credentials. This is not really secure as python is interpreted and your
credentials must be decrypted at some point in order to be used. In a real 
professional setup secrets would be stored elsewhere in a more secure fashion.

Example db_creds.json:

    {
      "DB_TYPE": "postgresql+psycopg2",
      "DB_INSTANCE": "<DATABASE INSTANCE>",
      "MASTER_USER": "<MASTER USER NAME>",
      "PASSWORD": "<MASTER USER PASSWORD>",
      "AWS_ENDPOINT": "<DATABASE ENDPOINT>",
      "PORT": "<DATABASE PORT>",
      "DB_NAME": "<DATABASE NAME>"
    }
Example s3_creds.json: 

    {
        "AWS_ACCESS_KEY": "<AWS ACCESS KEY",
        "AWS_SECRET_ACCESS_KEY": "<AWS_SECRET_ACCESS_KEY>",
        "BUCKET": "<AWS BUCKET NAME>"
    }
### Configure your settings:
In the config folder you should find a JSON file: config.json. You will want 
to alter its values to match how you want your system to behave. There is also a 
default config dictionary in config.py just in case the system can't find the 
config.json file. You will probably want to alter that as well.

Example config.json:

    {
      "aws_creds": "~/scripts/awsDB/creds/aws_creds.crypt",
      "db_creds": "~/scripts/awsDB/creds/db_creds.crypt",
      "broker_creds": "~/scripts/awsDB/creds/broker_creds.crypt",
      "test_aws_creds": "~/scripts/awsDB/creds/test_aws_creds.crypt",
      "test_db_creds": "~/scripts/awsDB/creds/test_db_creds.crypt",
      "errormail": "james_kirk@starfleet.ufp",
      "logfile": "testLog.log",
      "loglevel": "info",
      "ffmpeg_loglevel": "error",
      "thumbnail_x_size": "320",
      "thumbnail_y_size": "240",
      "movie_thumbnail_frame": "00:00:15",
      "thumbnail_extension": ".jpg",
      "test": true
    }
### Errormail
At some point we would like to email errors and other issues to this address. 
This might actually be better handled through an event monitoring system that
will allow individual users to subscribe to specific events.
### loglevel
How much logging do you want?
### ffmpeg_loglevel
FFMpeg comes with its own logging command switch.
### thumbnail_x_size, thumbnail_y_size
This determines the x and y size of the thumbnails that are generated.
### movie_thumbnail_frame
This determines what which movie frame is extracted to create the thumbnail.
### thumbnail_extension
This will determine what file type the thumbnails are.
###  Test
The test value controls which set of credentials to decrypt and user. This 
way you can set up a test database server. It might be interesting instead 
to replace this with a more flexible system that reads a value as a prefix to 
apply to which creds to use.

# Organization
The module as a whole is divided into subsections based on the area of focus.

**config:**  
overall configuration tools and settings

    config.json
    config.py
    utils.py

**creds:**  
encrypted credentials

    db_creds.crypt
    test_db_creds.crypt
    s3_creds.crypt
    test_s3_creds.crypt

**GUI:**  
graphical user interface tools

    submit.py
    search.py

**icons:**  
icons and images needed for the system and tools, including some default thumbnails
for non-graphical files


**services:**  
the meat of the module

    connection.py  - Create a connection to the database
    creds.py       - Find and encrypt/decrypt credentials and passwords
    filedata.py    - Get information about a file on disk
    hashing.py     - Create and test file hashes
    log.py         - Get our logger
    s3.py          - For working with s3
    thumbnailer.py - For making thumbnails out of various file types
    userdata.py    - Get information about our user and machine

**setup_scripts:**  
gotta build the backend stuff

    01_CreateTables_ORM.py - Create the database tables (using ORM methods)
    02_SeedDB_ORM.py       - Add initial data to tables (using ORM methods)
    03_verify.py           - Verify that the tables and initial data is actually there
    99_CleanDatabase.py    - Drop all of our tables
    ORM_models.py          - The python classes the define our tables and objects

**test:**  
unittests and example asset files

**tools:**  
Command-line tools

    add_catalog.py - Add a new catalog to the system
    add_role.py    - Add a new role to the system
    add_user.py    - Add a new user to the system
    search.py      - Search the database for Catalogs, Users, Roles or Assets
    submit.py      - Add a new asset to the system


# Tables

**Catalog**: each database belongs to a catalog group (ie: Reference, ProjectA)  
**Role**: determine what you can do with the assets  
**User**: who are   
**Asset**: an individual piece of art, documentation, or other item  
**Tag**: a short different word or phrase to describe and categorize an asset  
**AccessRecord**: every time someone creates or searches for an asset it should be registered here  
**BeanLog**: every time you want to keep track of something else happening you can create a bean  

This is a new line