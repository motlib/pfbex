# Changelog for fb_exporter

For more information about fb_exporter, please refer to the [readme](README.md)
file in the same directory.

## Version 0.3.0

* Update and extend documentation (readme file)

* Generate docker image directly from Pipfile / Pipfile.lock.

* Update to Python 3.9 for docker image.

* Handling of SIGTERM to quit pfbex without timeout when container shuts down.

* Improve `service-dumper.py` script

## Version 0.2.0

* Load metrics from YAML files in `./conf` directory.

* Add `service-dumper.py` script to dump all supported services from a FritzBox.

* Keep results in cache for minimum time to prevent sending too many requests to
  fritzbox. Configurable by `CACHE_TIME` setting.

* Add framework to manage settings.

## Version 0.1.1, 0.1.2, 0.1.3

* Work on docker configuration.

## Version 0.1.0

* Initial version.

* Define configuration structure and method to query FritzBox and provide
  metrics. This is based on [fritzbox\_exporter] of Patrick Dreker.

[fritzbox_exporter]: https://github.com/pdreker/fritzbox_exporter
