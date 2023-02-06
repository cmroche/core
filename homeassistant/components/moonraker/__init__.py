"""The moonraker integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .connector import APIConnector
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up moonraker from a config entry."""
    session = async_get_clientsession(hass)
    connector = APIConnector(hass, session, entry)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = connector

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    await connector.start()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        if connector := hass.data[DOMAIN].pop(entry.entry_id):
            await connector.stop()

    return unload_ok
