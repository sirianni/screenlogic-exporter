import * as ScreenLogic from "node-screenlogic";

const finder = new ScreenLogic.FindUnits();
const units = await finder.searchAsync();
const unit = units[0]
console.log(`Found unit: ${JSON.stringify(unit)}`);

const {
  gatewayName,
  address,
  port
} = unit

const client = new ScreenLogic.UnitConnection();
client.init(gatewayName, address, port);
await client.connectAsync();

console.dir(await client.equipment.getEquipmentStateAsync());
console.dir(await client.pump.getPumpStatusAsync());

// bodies[0] - pool
// bodies[1] - spa


// await client.closeAsync();
