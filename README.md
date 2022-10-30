# API

### api_lib.py ###

Represents a complete library for every client code (AI Anna, measurement devices), wich have to communicate with the API and the database.

---

### app.py ###

Represents the server code. Can be run locally or can be deployed on heroku with the following commands:

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.
```
$ heroku login
```
Clone the repository
Use Git to clone hackathon2022fulda's source code to your local machine.
```
$ heroku git:clone -a hackathon2022fulda 
$ cd hackathon2022fulda
```
Deploy your changes
Make some changes to the code you just cloned and deploy them to Heroku using Git.
```
$ git add .
$ git commit -am "make it better"
$ git push heroku master
```
