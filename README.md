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
        ca: /etc/servitor/tls-ca.pem
        cert: /etc/servitor/tls-swarm.pem
        key: /etc/servitor/tls-swarm.pem
```
