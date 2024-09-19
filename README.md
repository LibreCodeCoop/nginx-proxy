# Official documentation

Read https://github.com/nginx-proxy/nginx-proxy and https://github.com/nginx-proxy/docker-letsencrypt-nginx-proxy-companion/

## What is it for

Docker environments where all services are on a single host machine. Managed based on environment variables in each service for proxy configuration.

## Installation

* Clone the repo https://github.com/LibreCodeCoop/nginx-proxy/ in `~/projects`
```bash
git clone https://github.com/LibreCodeCoop/nginx-proxy ~/projects/nginx-proxy
```
* Create an external network to plug services that you need to receive a request from proxy
```
docker network create reverse-proxy
```

* Launch the application
```bash
cd ~/projects/nginx-proxy
docker compose up -d
```

## Backup
* You only need to back up the volumes because they contain the SSL certificates of the subdomains

## Update

* Go to the nginx-proxy folder which should be in `~/projects/nginx-proxy`
* Run the `git status` command to see if there were any changes, evaluate if you can discard or if you need to save the change if there were any
* Update the main project
```bash
git pull origin master
```
* Update the images
```bash
docker compose pull
```
* Raise the containers
```bash
docker compose up -d
```

## Service setup

A service setup may require specific configurations, for example if the service runs on a different port or has a different protocol. In these cases, see the nginx-proxy documentation.

### In subdomains
* You will need to add at least these environments to the server:
```bash
VIRTUAL_HOST=
LETSENCRYPT_HOST=
LETSENCRYPT_EMAIL=
```
### In subdomains and paths
* https://github.com/nginx-proxy/nginx-proxy/tree/main/docs#path-based-routing
* You will almost certainly need this:
* https://github.com/nginx-proxy/nginx-proxy/tree/main/docs#per-virtual_host-location-configuration\
Required:\
For pgadmin to work on the /pgadmin path you will need to add these rules to nginx:
```nginx
proxy_set_header X-Script-Name /pgadmin;
proxy_set_header Host $host;
```
