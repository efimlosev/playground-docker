# The New Project here
I will use this project as a playground to develop skills needed to find a new job

The current state the project:
- app that fetch data from  oxford dictionary and then store that data in the dockerized redis instance
- a couple Docker files to for the app and the redis host
- a docker compose file

Tests are not written so far

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
- Time to put everything together. Create .env file in the root the project with the simular context
```bash
APP_ID="Your Oxford  APP_ID"
APP_KEY="Your Oxford  APP_KEY"
SECRET_KEY="The string you generated on the previous step"
```
- Finally
```bash
docker-compose up
 ```
