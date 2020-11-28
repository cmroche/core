"""The Gree Climate integration."""
import asyncio
from datetime import timedelta
import logging

from homeassistant.components.climate import DOMAIN as CLIMATE_DOMAIN
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_interval

from .bridge import DiscoveryService
from .const import (
    COORDINATORS,
    DATA_DISCOVERY_INTERVAL,
    DATA_DISCOVERY_SERVICE,
    DISCOVERY_SCAN_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

PARALLEL_UPDATES = 0


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Gree Climate component."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Gree Climate from a config entry."""
    gree_discovery = DiscoveryService(hass)
    hass.data[DATA_DISCOVERY_SERVICE] = gree_discovery

    @callback
    def shutdown_event(_: Event) -> None:
        if hass.data[DOMAIN].get(DATA_DISCOVERY_INTERVAL) is not None:
            hass.data[DOMAIN][DATA_DISCOVERY_INTERVAL]()
            hass.data[DOMAIN].pop(DATA_DISCOVERY_INTERVAL)

        if hass.data.get(DATA_DISCOVERY_SERVICE) is not None:
            del hass.data[DATA_DISCOVERY_SERVICE]

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, shutdown_event)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, CLIMATE_DOMAIN)
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, SWITCH_DOMAIN)
    )

    _LOGGER.debug("Scanning network for Gree devices")
    await gree_discovery.discovery.scan()

    async def _async_scan_update(now):
        await gree_discovery.discovery.scan()

    hass.data[DOMAIN][DATA_DISCOVERY_INTERVAL] = async_track_time_interval(
        hass, _async_scan_update, timedelta(seconds=DISCOVERY_SCAN_INTERVAL)
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    if hass.data[DOMAIN].get(DATA_DISCOVERY_INTERVAL) is not None:
        hass.data[DOMAIN][DATA_DISCOVERY_INTERVAL]()
        hass.data[DOMAIN].pop(DATA_DISCOVERY_INTERVAL)

    if hass.data.get(DATA_DISCOVERY_SERVICE) is not None:
        del hass.data[DATA_DISCOVERY_SERVICE]

    results = asyncio.gather(
        hass.config_entries.async_forward_entry_unload(entry, CLIMATE_DOMAIN),
        hass.config_entries.async_forward_entry_unload(entry, SWITCH_DOMAIN),
    )

    unload_ok = False not in await results
    if unload_ok:
        hass.data[DOMAIN].pop(COORDINATORS, None)

    return unload_ok
