# pfbex

`pfbex` (Prometheus FritzBox Exporter) queries the TR-064 services of a FritzBox
and provides metrics in a format to be processed by [Prometheus]. This exporter
is initially based on the exporter developed by Patrick Dreker.

## Usage

The preferred way is to run the exporter as a Docker container. 

First you need to create an environment file containing settings for running the
exporter. At least you need to provide the username and password of the user to
log in to the FritzBox:

```
FRITZ_USER=api
FRITZ_PASS=api123api
```

Then fire up the container with docker-compose:

```
docker-compose up
```


[Prometheus]: https://www.prometheus.io
