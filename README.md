[![Build Status](https://travis-ci.org/LarryWachira/cp2-bucket-list.svg?branch=master)](https://travis-ci.org/LarryWachira/cp2-bucket-list)

# Chum
Chum is bucketlist app built with a flask API and an Angular 2 frontend. This repository contains the backend which has the following endpoints:

| EndPoint | Functionality 
|----------|---------------
| POST api/v1/auth/login | Logs a user in
| POST api/v1/auth/register | Register a user
| POST api/v1/bucketlists/ | Create a new bucket list
| GET api/v1/bucketlists/ | List all the created bucket lists
| GET api/v1/bucketlists/<id> | Get single bucket list
| PUT api/v1/bucketlists/<id> | Update this bucket list
| DELETE api/v1/bucketlists/<id> | Delete this single bucket list
| POST api/v1/bucketlists/<id>/items/ | Create a new item in bucket list
| PUT api/v1/bucketlists/<id>/items/<item_id> | Update a bucket list item
| DELETE api/v1/bucketlists/<id>/items/<item_id> | Delete an item in a bucket listd
