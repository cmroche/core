"""Tests for gree component."""
from datetime import timedelta

from greeclimate.exceptions import DeviceTimeoutError
import pytest

from homeassistant.components.gree.const import DOMAIN as GREE_DOMAIN
from homeassistant.components.switch import DOMAIN
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_FRIENDLY_NAME,
    SERVICE_TOGGLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
)
from homeassistant.setup import async_setup_component
import homeassistant.util.dt as dt_util

from tests.async_mock import patch
from tests.common import MockConfigEntry, async_fire_time_changed

ENTITY_ID_LIGHT_PANEL = f"{DOMAIN}.fake_device_1_panel_light"
ENTITY_ID_QUIET = f"{DOMAIN}.fake_device_1_quiet"
ENTITY_ID_FRESH_AIR = f"{DOMAIN}.fake_device_1_fresh_air"
ENTITY_ID_XFAN = f"{DOMAIN}.fake_device_1_xfan"
ENTITY_ID_TURBO = f"{DOMAIN}.fake_device_1_turbo"


@pytest.fixture
def mock_now():
    """Fixture for dtutil.now."""
    return dt_util.utcnow()


async def async_setup_gree(hass):
    """Set up the gree switch platform."""
    MockConfigEntry(domain=GREE_DOMAIN).add_to_hass(hass)
    await async_setup_component(hass, GREE_DOMAIN, {GREE_DOMAIN: {DOMAIN: {}}})
    await hass.async_block_till_done()


@pytest.mark.parametrize(
    "entity",
    [
        ENTITY_ID_LIGHT_PANEL,
        ENTITY_ID_QUIET,
        ENTITY_ID_FRESH_AIR,
        ENTITY_ID_XFAN,
        ENTITY_ID_TURBO,
    ],
)
async def test_send_switch_on(hass, mock_now, entity):
    """Test for sending power on command to the device."""
    await async_setup_gree(hass)

    next_update = mock_now + timedelta(minutes=5)
    with patch("homeassistant.util.dt.utcnow", return_value=next_update):
        async_fire_time_changed(hass, next_update)
    await hass.async_block_till_done()

    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_ON


@pytest.mark.parametrize(
    "entity",
    [
        ENTITY_ID_LIGHT_PANEL,
        ENTITY_ID_QUIET,
        ENTITY_ID_FRESH_AIR,
        ENTITY_ID_XFAN,
        ENTITY_ID_TURBO,
    ],
)
async def test_send_switch_on_device_timeout(hass, device, mock_now, entity):
    """Test for sending power on command to the device with a device timeout."""
    device().push_state_update.side_effect = DeviceTimeoutError

    await async_setup_gree(hass)

    next_update = mock_now + timedelta(minutes=5)
    with patch("homeassistant.util.dt.utcnow", return_value=next_update):
        async_fire_time_changed(hass, next_update)
    await hass.async_block_till_done()

    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_ON


@pytest.mark.parametrize(
    "entity",
    [
        ENTITY_ID_LIGHT_PANEL,
        ENTITY_ID_QUIET,
        ENTITY_ID_FRESH_AIR,
        ENTITY_ID_XFAN,
        ENTITY_ID_TURBO,
    ],
)
async def test_send_switch_off(hass, mock_now, entity):
    """Test for sending power on command to the device."""
    await async_setup_gree(hass)

    next_update = mock_now + timedelta(minutes=5)
    with patch("homeassistant.util.dt.utcnow", return_value=next_update):
        async_fire_time_changed(hass, next_update)
    await hass.async_block_till_done()

    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TURN_OFF,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_OFF


@pytest.mark.parametrize(
    "entity",
    [
        ENTITY_ID_LIGHT_PANEL,
        ENTITY_ID_QUIET,
        ENTITY_ID_FRESH_AIR,
        ENTITY_ID_XFAN,
        ENTITY_ID_TURBO,
    ],
)
async def test_send_switch_toggle(hass, mock_now, entity):
    """Test for sending power on command to the device."""
    await async_setup_gree(hass)

    next_update = mock_now + timedelta(minutes=5)
    with patch("homeassistant.util.dt.utcnow", return_value=next_update):
        async_fire_time_changed(hass, next_update)
    await hass.async_block_till_done()

    # Turn the service on first
    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_ON

    # Toggle it off
    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TOGGLE,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_OFF

    # Toggle is back on
    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TOGGLE,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_ON


@pytest.mark.parametrize(
    "entity,name",
    [
        (ENTITY_ID_LIGHT_PANEL, "Panel Light"),
        (ENTITY_ID_QUIET, "Quiet"),
        (ENTITY_ID_FRESH_AIR, "Fresh Air"),
        (ENTITY_ID_XFAN, "XFan"),
        (ENTITY_ID_TURBO, "Turbo"),
    ],
)
async def test_entity_name(hass, entity, name):
    """Test for name property."""
    await async_setup_gree(hass)
    state = hass.states.get(entity)
    assert state.attributes[ATTR_FRIENDLY_NAME] == f"fake-device-1 {name}"
