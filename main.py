import asyncio
import argparse
import pprint
import logging

from screenlogicpy import ScreenLogicGateway, discovery

import prometheus_client
from prometheus_client.core import GaugeMetricFamily, StateSetMetricFamily, CounterMetricFamily
from prometheus_client.registry import Collector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

class CustomCollector(Collector):
  def __init__(self):
    self.loop = asyncio.new_event_loop()
    self.gateway = self.loop.run_until_complete(self.connect())

  async def connect(self):
    logger.info("Initializing gateway...")
    hosts = await discovery.async_discover()

    if len(hosts) > 0:
      logger.info(f"Connecting to host {hosts[0]}")
      gateway = ScreenLogicGateway()
      await gateway.async_connect(**hosts[0])
      return gateway
    else:
      logger.warning("No gateways found")

  def collect(self):
    logger.info("Collecting metrics...")
    for m in self.loop.run_until_complete(self.async_collect()):
      yield m

  async def async_collect(self):
    await self.gateway.async_update()

    return [
      *self.collect_misc(),
      *self.collect_body(),
      *self.collect_pump(),
      *self.collect_circuit()
    ]

  def collect_misc(self):
    temp = GaugeMetricFamily('screenlogic_air_temp', 'Air temperature')
    temp.add_metric([], self.gateway.get_data('controller', 'sensor', 'air_temperature', 'value'))

    freeze_mode = GaugeMetricFamily('screenlogic_freeze_mode', 'Freeze mode')
    freeze_mode.add_metric([], self.gateway.get_data('controller', 'sensor', 'freeze_mode', 'value'))

    return [
      temp,
      freeze_mode
    ]

  def collect_circuit(self):
    circuit_state = GaugeMetricFamily('screenlogic_circuit_state', 'Circuit state', labels=['name'])

    for circuit in self.gateway.get_data('circuit').values():
      if circuit['name'].startswith('Feature'):
        continue
      circuit_state.add_metric([circuit['name']], circuit['value'])

    return [
      circuit_state
    ]

  def collect_body(self):
    temp = GaugeMetricFamily('screenlogic_body_temp', 'Body temperature', labels=['name'])
    heat_setpoint = GaugeMetricFamily('screenlogic_body_heat_setpoint', 'Body temperature setpoint', labels=['name'])
    heat_state = StateSetMetricFamily('screenlogic_body_heat_state', 'Body heat state', labels=['name'])
    heat_mode = StateSetMetricFamily('screenlogic_body_heat_mode', 'Body heat mode', labels=['name'])

    for body in self.gateway.get_data('body').values():
      labels = [body['name']]
      temp.add_metric(labels, body['last_temperature']['value'])
      heat_setpoint.add_metric(labels, body['heat_setpoint']['value'])

      heat_state.add_metric(labels, {
        val: body['heat_state']['value'] == index
        for index, val in enumerate(body['heat_state']['enum_options'])
      })

      heat_mode.add_metric(labels, {
        val: body['heat_mode']['value'] == index
        for index, val in enumerate(body['heat_mode']['enum_options'])
      })

    return [
      temp,
      heat_setpoint,
      heat_state,
      heat_mode
    ]

  def collect_pump(self):
    pump = self.gateway.get_data('pump', 0)
    metrics = []
    for i in ['watts', 'rpm', 'gpm']:
      gauge = GaugeMetricFamily(f'screenlogic_pump_{i}', f'Pump {i}')
      gauge.add_metric([], pump[f'{i}_now']['value'])
      metrics.append(gauge)
    return metrics

parser = argparse.ArgumentParser(description="Start the exporter")
parser.add_argument('-p', '--port', type=int, default=9199, help='The port to start the server on.')
args = parser.parse_args()

prometheus_client.REGISTRY.register(CustomCollector())

server, t = prometheus_client.start_http_server(args.port)

t.join()