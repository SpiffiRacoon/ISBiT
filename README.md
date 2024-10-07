# ISBiT

# Deploy
Make sure docker (and docker compose) are installed on the system.

To deploy the app simply type:
```yml
sudo docker compose -f docker-compose.yml up
```

To deploy the app after changes, use the following command:
```yml
sudo docker compose -f docker-compose.yml up --build
```
> This will run the dockerfiles again, and then copy the new code etc...

