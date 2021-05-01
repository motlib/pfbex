# pfbex

`pfbex` (Prometheus FritzBox Exporter) queries the TR-064 services of a FritzBox
and provides metrics in a format to be processed by [Prometheus]. This exporter
is initially based on the exporter developed by Patrick Dreker.

## Usage

The preferred way is to run `pfbex` as a Docker container.

First you need to create an environment file `user.env` containing the settings
for running the exporter. At least you need to provide the username and password
of the user to log in to the FritzBox:

```
FRITZ_USER=api
FRITZ_PASS=api123api
```

Then you can start the container with `docker-compose up --build`. To run it in
background, use `docker-compose up --build -d`.

To check if the container is up and running correctly, you can use a web browser
to open http://localhost:8765/metrics.

Now you can configure Prometheus to scrape data from the exporter and
e.g. use [Grafana] to show it in a dashboard.

## Supported FritzBox Models

The exporter is tested against a FritzBox 6591 Cable with firmware version
7.22. Currently I do not yet know how much about how the API differs between
FritzBox models and firmware versions. 

You can check the `Configuration` section to learn how to extend `pfbex` to add
support for further FritzBox models or versions. 

## Development

Contributions in any form are very welcome. Feel free to create issues on github
with feedback and suggestions for improvement and pull requests to improve and
extend the implementation.

## Configuration

All diagnostic values provided by `pfbex` are defined in configuration files in
the `conf` directory. You can add additional metrics by editing these
files. Check [configuration](./docs/configuration.md) for detailed information. 

If you find additional data provided by any FritzBox model, it would be nice if
you can share this information, either by creating a pull request or by creating
an issue on Github.

[Prometheus]: https://www.prometheus.io
[Grafana]: https://www.grafana.com
