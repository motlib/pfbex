# Changelog for fb_exporter

For more information about fb_exporter, please refer to the `README.md` file in
the same directory.

## Work In Progress

* Keep results in cache for minimum time to prevent sending too many requests to
  fritzbox. Configurable by `CACHE_TIME` setting.

* Add framework to manage settings.

## 0.1.0

* Initial version.

* Define configuration structure and method to query FritzBox and provide
  metrics. This is based on [fritzbox\_exporter] of Patrick Dreker.

[fritzbox_exporter]: https://github.com/pdreker/fritzbox_exporter
