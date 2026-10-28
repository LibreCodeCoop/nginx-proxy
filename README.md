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


## Optional Nextcloud Talk TURNS/TCP443 sharing (LibreCode)

The image already includes Nginx stream and ssl_preread. The container
can run both the TCP/TLS entry listeners and its existing dynamically generated
HTTP/HTTPS virtual hosts in the same Nginx process. The Compose defaults
keep the current behaviour (80:80 and 443:443, without PROXY protocol).

When explicitly enabled by the Ansible role from
LibreCodeCoop/infrastructure-operations:

- NGINX_PROXY_HTTP_CONTAINER_PORT=10080 maps host TCP/80 to the
  stream entry, which forwards to the generated HTTP listener on internal 80.
- NGINX_PROXY_HTTPS_CONTAINER_PORT=10443 maps host TCP/443 to the
  stream entry; ssl_preread routes the TURN hostname to the Eturnal
  private TLS listener, everything else to the generated HTTPS listener
  on internal 443.
- ENABLE_PROXY_PROTOCOL=true, configured in the Ansible override only
  on the opted-in host, makes the generated HTTP/HTTPS listeners
  require PROXY protocol. Stream must always supply
  it for both HTTP and HTTPS. A direct connection to the inner HTTP/HTTPS
  port without PROXY protocol will fail.
- The Ansible-managed Compose override mounts the top-level stream
  configuration, enables PROXY protocol only for the opted-in host and
  pins the current running Nginx/ACME image digests. It also configures
  real-IP trust for the local stream loopback.

Do not enable the three settings without the matching generated Ansible
files and Eturnal TLS listener. Changes to the published target ports
require a controlled Docker Compose service recreation, not a reload.

This relies on clients supplying valid SNI for talk-turn.librecode.coop.
Without SNI the connection defaults to HTTPS. Direct TURN/UDP3478,
TURN/UDP443 and TURNS/TCP5349 remain available independently.

The nginx-proxy ACME companion is unchanged. Its HTTP-01 and certificate
renewal paths must be tested in staging before a production cutover.
The shared-port solution does not address unrelated signaling or
network-path timeouts.
