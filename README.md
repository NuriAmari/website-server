This repository contains source code and configuration for a series of tools that support my [new website](https://nuriamari.dev). More information about the client side can be found [here](https://github.com/NuriAmari/website).

## Hosting

This entire system is currently run on an Ubuntu machine provided by [AWS](https://aws.amazon.com/ec2/instance-types/). Static files are served using an [NGINX](https://www.nginx.com/) proxy, behind which a small [Tornado](https://www.tornadoweb.org/en/stable/) webserver operates.
The webserver currently supports the site's Chess functionality, communicating over regular HTTP and Websockets. SSL certs are generated using [Let's Encrypt](https://letsencrypt.org/) and the entire system, aside from domain registration, is free.

## Persistance

In order to persist game state during maintenance or after downtime of any sort, site information (mostly chess game state) is stored in Redis, running on the same machine. Redis was chosen for its speed and convenient data structures. [Redis-py](https://github.com/andymccurdy/redis-py) is used to communicate with the Redis instance.

## Tornado Service

For convenience, the Tornado webserver is configured to be managed by [systemd](https://en.wikipedia.org/wiki/Systemd).

In the future, I think it would be interesting to add health checks and metric collection using tools like [collectd](https://collectd.org/) and [Grafana](https://grafana.com/)
