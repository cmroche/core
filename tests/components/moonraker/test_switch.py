"""Test moonraker switches."""
from unittest.mock import Mock

import pytest

from homeassistant.components.moonraker.connector import generate_signal
from homeassistant.components.moonraker.const import SIGNAL_UPDATE_PRINT_STATUS
from homeassistant.components.switch import DOMAIN as SWITCH
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_API_KEY,
    CONF_HOST,
    CONF_PORT,
    CONF_SSL,
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import DOMAIN

from tests.common import MockConfigEntry

HOST_NAME = "test_host"


async def setup_component(
    hass: HomeAssistant, entity_name: str
) -> tuple[str, ConfigEntry]:
    """Set up sensor component."""
    entity_id = f"{SWITCH}.{entity_name}"
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


@pytest.mark.parametrize(
    "name,signal,key,value_on,value_off",
    [
        ("pause_print", SIGNAL_UPDATE_PRINT_STATUS, "state", "paused", "printing"),
    ],
)
async def test_generice_switches(
    hass: HomeAssistant,
    mock_connector: Mock,
    name: str,
    signal: str,
    key: str,
    value_on: str,
    value_off: str,
) -> None:
    """Test the generic switches."""
    entity_id, entry = await setup_component(hass, f"{HOST_NAME}")
    state = hass.states.get(f"{entity_id}_{name}")
    assert state
    assert state.state == STATE_UNAVAILABLE

    entry_signal = generate_signal(signal, entry.entry_id)
    async_dispatcher_send(hass, entry_signal, {key: value_on})
    await hass.async_block_till_done()
    state = hass.states.get(f"{entity_id}_{name}")
    assert state.state == STATE_ON

    entry_signal = generate_signal(signal, entry.entry_id)
    async_dispatcher_send(hass, entry_signal, {key: value_off})
    await hass.async_block_till_done()
    state = hass.states.get(f"{entity_id}_{name}")
    assert state.state == STATE_OFF
