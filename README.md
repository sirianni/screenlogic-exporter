# screenlogic-exporter

Prometheus exporter for Pentair ScreenLogic pool controller.

Built using [screenlogic.py](https://github.com/dieselrabbit/screenlogicpy)

# Usage
```
docker run --net=host sirianni/screenlogic-exporter
```

Example output:
```
$ curl http://localhost:9199/metrics
# HELP screenlogic_air_temp Air temperature
# TYPE screenlogic_air_temp gauge
screenlogic_air_temp 71.0
# HELP screenlogic_freeze_mode Freeze mode
# TYPE screenlogic_freeze_mode gauge
screenlogic_freeze_mode 0.0
# HELP screenlogic_body_temp Body temperature
# TYPE screenlogic_body_temp gauge
screenlogic_body_temp{name="Pool"} 83.0
screenlogic_body_temp{name="Spa"} 83.0
# HELP screenlogic_body_heat_setpoint Body temperature setpoint
# TYPE screenlogic_body_heat_setpoint gauge
screenlogic_body_heat_setpoint{name="Pool"} 84.0
screenlogic_body_heat_setpoint{name="Spa"} 98.0
# HELP screenlogic_body_heat_state Body heat state
# TYPE screenlogic_body_heat_state gauge
screenlogic_body_heat_state{name="Pool",screenlogic_body_heat_state="Both"} 0.0
screenlogic_body_heat_state{name="Pool",screenlogic_body_heat_state="Heater"} 0.0
screenlogic_body_heat_state{name="Pool",screenlogic_body_heat_state="Off"} 1.0
screenlogic_body_heat_state{name="Pool",screenlogic_body_heat_state="Solar"} 0.0
screenlogic_body_heat_state{name="Spa",screenlogic_body_heat_state="Both"} 0.0
screenlogic_body_heat_state{name="Spa",screenlogic_body_heat_state="Heater"} 0.0
screenlogic_body_heat_state{name="Spa",screenlogic_body_heat_state="Off"} 1.0
screenlogic_body_heat_state{name="Spa",screenlogic_body_heat_state="Solar"} 0.0
# HELP screenlogic_body_heat_mode Body heat mode
# TYPE screenlogic_body_heat_mode gauge
screenlogic_body_heat_mode{name="Pool",screenlogic_body_heat_mode="Don't Change"} 0.0
screenlogic_body_heat_mode{name="Pool",screenlogic_body_heat_mode="Heater"} 0.0
screenlogic_body_heat_mode{name="Pool",screenlogic_body_heat_mode="Off"} 1.0
screenlogic_body_heat_mode{name="Pool",screenlogic_body_heat_mode="Solar"} 0.0
screenlogic_body_heat_mode{name="Pool",screenlogic_body_heat_mode="Solar Preferred"} 0.0
screenlogic_body_heat_mode{name="Spa",screenlogic_body_heat_mode="Don't Change"} 0.0
screenlogic_body_heat_mode{name="Spa",screenlogic_body_heat_mode="Heater"} 0.0
screenlogic_body_heat_mode{name="Spa",screenlogic_body_heat_mode="Off"} 1.0
screenlogic_body_heat_mode{name="Spa",screenlogic_body_heat_mode="Solar"} 0.0
screenlogic_body_heat_mode{name="Spa",screenlogic_body_heat_mode="Solar Preferred"} 0.0
# HELP screenlogic_pump_watts Pump watts
# TYPE screenlogic_pump_watts gauge
screenlogic_pump_watts 633.0
# HELP screenlogic_pump_rpm Pump rpm
# TYPE screenlogic_pump_rpm gauge
screenlogic_pump_rpm 2450.0
# HELP screenlogic_pump_gpm Pump gpm
# TYPE screenlogic_pump_gpm gauge
screenlogic_pump_gpm 26.0
# HELP screenlogic_circuit_state Circuit state
# TYPE screenlogic_circuit_state gauge
screenlogic_circuit_state{name="Spa"} 0.0
screenlogic_circuit_state{name="Lights"} 1.0
screenlogic_circuit_state{name="Cleaner"} 0.0
screenlogic_circuit_state{name="Spillway"} 0.0
screenlogic_circuit_state{name="Pool"} 1.0
screenlogic_circuit_state{name="Jets"} 0.0
```

# Example Prometheus scrape config
```yaml
scrape_configs:
- job_name: screenlogic
  scrape_interval: 1m
  static_configs:
  - targets: ['localhost:9199']
```
