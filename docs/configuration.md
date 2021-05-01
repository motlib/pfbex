# Configuration

The metrics provided by `pfbex` are defined by YAML configuration files in the
`./conf` directory. When `pfbex` starts, it will load all YAML files found in
this directory.

## Configuration Format

Each YAML file contains a list of metrics. Each metric has general attributes
and a list of data sources, i.e. Service, Action, Attribute names as provided by
the diagnostic interface of the FritzBox.

Here is an commented example of the fritzbox_uptime metric to show the
configuration structure:

```YAML
# This defines the name of the metric.
fritzbox_uptime:

  # type of the metric. Either counter (always increasing) or gauge (can go up
  # or down)
  type: counter

  # Help text put into the output generated for Prometheus
  doc: Fritzbox uptime

  # List of service, action, attribute values to map to this metric.
  items:
      # The service to query
    - service: DeviceInfo1

      # The action to query
      action: GetInfo

      # The attribute to evaluate
      attr: NewUpTime

      # Labels assigned to the metric
      labels: {type: device}
```

## Non-Numeric Values

Some diagnostic data retrieved from the FritzBox is not in numeric format, so it
has to be converted, as Prometheus does only process floating-point values.

That's why you can specify an additional conversion function in the
configuration. Here's another example:

```yaml
fritzbox_ppp_connection_state:
  doc: PPP connection state
  items:
    - service: WANPPPConnection1
      action: GetStatusInfo
      attr: NewConnectionStatus

      # Here's the conversion function
      fct: "lambda x: 1.0 if x == 'Connected' else 0.0"
```

The `fct` attribute is optional. If you specify it, the value must be a Python
lambda expression taking one parameter (the value received from the FritzBox)
and returning a floating point number.

In the example above, the expression is this:

```python
lambda x: 1.0 if x == 'Connected' else 0.0
```

This lambda expression works like a function in Python. It takes one parameter
`x`. If `x` is equal to `Connected`, then it returns `1.0`, otherwise `0.0`.

Take care to always enclose the whole lambda expression in quotation marks
(`"`), so that the YAML parser does not get confused by the `:` characters.

## Configuration Processing

When `pfbex` starts, it will load all YAML files in the `./conf` directory.

When accessing the `/metrics` URL, it will query the FritzBox to retrieve all
diagnostic data defined in the configuration. The queries are optimized, so that
each service and action is only queried once, independent from the metrics where
this data is later used.

If the FritzBox returns valid data, it is provided to Prometheus on the
`./metrics` URL. Diagnostic data is cached for some time, by default for 30s,
before the FritzBox is queried again. This can be configured by `CACHE_TIME`
setting.
