"""Test the binary sensors."""
from unittest.mock import Mock

from homeassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR
from homeassistant.components.moonraker.connector import generate_signal
from homeassistant.components.moonraker.const import SIGNAL_UPDATE_PRINT_STATUS
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_PORT, CONF_SSL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import DOMAIN

from tests.common import MockConfigEntry

HOST_NAME = "test_host"


async def setup_component(
    hass: HomeAssistant, entity_name: str
) -> tuple[str, ConfigEntry]:
    """Set up binary sensor component."""
    entity_id = f"{BINARY_SENSOR}.{entity_name}"
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=entity_name,
        title=entity_name,
        data={
            CONF_HOST: f"{HOST_NAME}.local",
            CONF_PORT: 7125,
            CONF_SSL: False,
            CONF_API_KEY: "",
        },
    )

    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    return entity_id, config_entry


async def test_printing_status(hass: HomeAssistant, mock_connector: Mock) -> None:
    """Test the printing status binary sensor."""
    entity_id, entry = await setup_component(hass, f"{HOST_NAME}")
    state = hass.states.get(f"{entity_id}_print_status")
    assert state is not None
    assert state.state == "off"

    signal = generate_signal(SIGNAL_UPDATE_PRINT_STATUS, entry.entry_id)
    async_dispatcher_send(hass, signal, {"state": "printing"})
    await hass.async_block_till_done()
    state = hass.states.get(f"{entity_id}_print_status")
    assert state.state == "on"

    async_dispatcher_send(hass, signal, {"state": "completed"})
    await hass.async_block_till_done()
    state = hass.states.get(f"{entity_id}_print_status")
    assert state.state == "off"

    async_dispatcher_send(hass, signal, {"state": "paused"})
    await hass.async_block_till_done()
    state = hass.states.get(f"{entity_id}_print_status")
    assert state.state == "on"
