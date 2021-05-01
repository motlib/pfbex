# pfbex

`pfbex` (Prometheus FritzBox Exporter) queries the TR-064 services of a FritzBox
and provides metrics in a format to be processed by [Prometheus]. This exporter
is initially based on the exporter developed by Patrick Dreker.

## Usage

The preferred way is to run `pfbex` as a Docker container.

First you need to create an environment file `user.env` containing settings for
running the exporter. At least you need to provide the username and password of
the user to log in to the FritzBox:

```
FRITZ_USER=api
FRITZ_PASS=api123api
```

Then fire up the container with docker-compose `docker-compose up --build`. To
run it in background, use `docker-compose up --build -d`.

To check if the container is up and running correctly, you can use a web browser
to open http://localhost:8765/metrics.

Now you can configure Prometheus to scrape data from the exporter and
e.g. [Grafana] to show it in a dashboard.

## Supported FritzBox Models

The exporter is tested against a FritzBox 6591 Cable with firmware version
7.22. Currently I do not know how much the API differs between FritzBox models
and firmware versions.

## Development

Contributions in any form are very welcome. Feel free to create issues on github
with feedback and suggestions for improvement and pull requests to improve and
extend the implementation.

[Prometheus]: https://www.prometheus.io
[Grafana]: https://www.grafana.com
