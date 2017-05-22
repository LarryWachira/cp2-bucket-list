[![Build Status](https://travis-ci.org/LarryWachira/cp2-bucket-list.svg?branch=master)](https://travis-ci.org/LarryWachira/cp2-bucket-list)
[![Coverage Status](https://coveralls.io/repos/github/LarryWachira/cp2-bucket-list/badge.svg?branch=master)](https://coveralls.io/github/LarryWachira/cp2-bucket-list?branch=master)

# Chum
Chum is bucketlist app built with a flask API and an Angular 2 frontend. This repository contains the backend which has the following endpoints:

| EndPoint | Functionality 
|----------|---------------
| POST api/v1/auth/login | Logs a user in
| POST api/v1/auth/register | Register a user
| POST api/v1/bucketlists/ | Create a new bucket list
| GET api/v1/bucketlists/ | List all the created bucket lists
| GET api/v1/bucketlists/<bucketlist_id> | Get single bucket list
| PUT api/v1/bucketlists/<bucketlist_id> | Update this bucket list
| DELETE api/v1/bucketlists/<bucketlist_id> | Delete this single bucket list
| POST api/v1/bucketlists/<bucketlist_id>/items/ | Create a new item in bucket list
| PUT api/v1/bucketlists/<bucketlist_id>/items/<item_id> | Update a bucket list item
| DELETE api/v1/bucketlists/<bucketlist_id>/items/<item_id> | Delete an item in a bucket listd

## Setting up Chum's backend

Chum's has a number of dependencies as detailed in the requirements.txt file. To run it, you'll need to install [Python 3.6](http://python.org) from Python's website or via [Homebrew](https://brew.sh/) package manager(recommended) if you're on MacOS and setup a virtual environment as illustrated [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/). Dependencies that are built into Python have not been included.
______

1. The first thing you need to do is to clone the repo by running the following command: (If you do not have git, you can download the entire project on the link at the top right download of the repo provided by github.)


        `$ git clone https://github.com/LarryWachira/cp2-bucket-list.git`

2. Activate the virtual environment, navigate to the project folder and then run the following command to install all the requirements in one go: (Make sure the command is run at the root of the project folder.)


        `$ pip install -r requirements.txt`

3. The next step is to set up a database for the backend. By default, it uses an SQlite database but set up a custom Postgres database, all you need to do is set a database URI environment variable eg:


        `$ export SQLALCHEMY_DATABASE_URI='postgresql://user:password@localhost:5432/db_name'`

4. Run migrations:


        `$ python run.py migrations`

5. For token authentication, the backend also has a default secret key in the configuration settings. To override it (recommended), run the following command to set a custom SECRET_KEY:


        `$ export SECRET_KEY='your_secret'`

6. You're now ready to start calling the api endpoints. Run this command to begin:


        `$ python run.py runserver`

7. Pat yourself on the back if you get the following terminal output:


        `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

______

Running tests has also been simplified, just run the following command:
   
        `$python run.py tests`
