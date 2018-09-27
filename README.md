# Servitor
__Tiny webhook for pushing image updates to docker stack services__

## Configuration

### Environment
*Required*
* `TOKEN` - authentication secret

*Optional*
* `CONFIG_FILE` - default: "/etc/servitor/config.yaml"
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
        cert: /etc/servitor/tls-swarm.crt
        key: /etc/servitor/tls-swarm.pem
```
