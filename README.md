# date: 09/18/2022 Update 
I made a  functional kubernetes deployment, that reside in **k8s** folder.


# The New Project here
I will use this project as a playground to develop skills needed to find a new job

The current state of the project:
- an app that fetches data from  Oxford dictionary and then stores that data in the dockerized Redis instance
- a couple of Docker files to for the app and the Redis host
- a docker-compose file
- a fully functional Kubernetes deploynent 

~~tests are not written so far~~. Wrote some tests

**First call**

![word search example](/images/real-call.png)

**Second call**

![word search from cache](/images/call-from-cache.png)


# How to run this project?

- I suppose you know you need have git, docker and docker compose installed.
So it would be the first step. Additionally do 
```bash
git clone git@github.com:efimlosev/playground-docker.git
cd playground-docker
```
- The second thing you need your own api keys, so go (https://developer.oxforddictionaries.com) and get your keys.
- Then  generate keys for the app
``` bash 
python3 -c 'import secrets; print(secrets.token_hex())'
```
- Time to put everything together. Create .env file in the root of the project with the simular context
```bash
APP_ID="Your Oxford  APP_ID"
APP_KEY="Your Oxford  APP_KEY"
SECRET_KEY="The string you generated on the previous step"
```
- Finally
```bash
docker-compose up
 ```
