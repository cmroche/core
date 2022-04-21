"""Test the binary sensors."""
from unittest.mock import Mock, patch

from homeassistant.components.button import DOMAIN as BUTTON
from homeassistant.components.button.const import SERVICE_PRESS
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_API_KEY,
    CONF_HOST,
    CONF_PORT,
    CONF_SSL,
    STATE_UNKNOWN,
)
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import DOMAIN

from tests.common import MockConfigEntry

HOST_NAME = "test_host"


async def setup_component(
    hass: HomeAssistant, entity_name: str
) -> tuple[str, ConfigEntry]:
    """Set up binary sensor component."""
    entity_id = f"{BUTTON}.{entity_name}"
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


async def test_calling_button(hass: HomeAssistant, mock_connector: Mock) -> None:
    """Test calling the button service."""
    entity_id, _ = await setup_component(hass, f"{HOST_NAME}")
    entity_name = f"{entity_id}_emergency_stop"
    state = hass.states.get(entity_name)

    assert state
    assert state.state == STATE_UNKNOWN

    now = dt_util.parse_datetime("2021-01-09 12:00:00+00:00")
    with patch("homeassistant.util.dt.utcnow", return_value=now):
        await hass.services.async_call(
            BUTTON, SERVICE_PRESS, {ATTR_ENTITY_ID: entity_name}, blocking=True
        )

    state = hass.states.get(entity_name)
    assert state
    assert state.state == now.isoformat()
