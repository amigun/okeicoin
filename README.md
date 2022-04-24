# OkEiC0inS - digital currency of college

OkEiC0inSB0T - is a bot which can transfer okeicoins between students

This repository is a source code for OkEiC0inSB0T. Follow the steps below to run and use this bot

## The steps.
To create a temporary database for FSM: 
```bash
systemctl start docker
```
```bash
docker run --rm --name redis_fsm -p 127.0.0.1:6379:6379 -d redis
```
To stop a container:
```bash
docker stop $(docker ps -aq)
```
To check a work of container:
```bash
docker exec -it redis_fsm redis-cli
```
