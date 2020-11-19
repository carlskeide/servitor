![Python Package](https://github.com/carlskeide/servitor/workflows/Docker%20build/badge.svg)

# Servitor
__Tiny webhook for pushing image updates to docker swarm stacks/services__

## Configuration

### Environment
*Required*
* `AUTH_TOKEN` - API access token

*Optional*
* `CONFIG_FILE` - default: "/servitor.yaml"
* `LOG_LEVEL` - default: INFO

### Config File Format
```
swarm:
  some-swarm:
    url: "swarm-addr:2375"
    tls: false

  some-tls-swarm:
    url: "tls-swarm-addr:2376"
    tls:
        ca_cert: /etc/servitor/tls-ca.pem
        client_cert: /etc/servitor/tls-swarm.pem
        client_key: /etc/servitor/tls-swarm.pem
```
