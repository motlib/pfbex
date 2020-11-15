# TODO List

* Load config from yaml file / files

* Watch for changed config files

* Disable service access after a few failed attempts

  -> No, so that after change of the FritzBox, the exporter can immediately
  adapt to the new model.

* Keep results in cache for minimum time (e.g. 1 minute) to prevent sending too
  many requests to fritzbox
