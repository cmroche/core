"""Handle Moonraker service calls."""
from __future__ import annotations

import logging

from homeassistant.const import CONF_DEVICE_ID
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import device_registry

from .const import DATA_CONNECTOR, DOMAIN

_LOGGER = logging.getLogger(__name__)


def async_register_services(hass: HomeAssistant) -> None:
    """Register service for Moonraker."""

    async def run_gcode_command(call: ServiceCall, skip_reload=True):
        device_id: str | None = call.data.get(CONF_DEVICE_ID)
        gcode: str | None = call.data.get("gcode")

        assert device_id
        if not (device := device_registry.async_get(hass).async_get(device_id)):
            _LOGGER.error("Could not find a device for id: %s", device_id)
            return

        entries = device.config_entries.copy()
        for entry in entries.pop():
            connector = hass.data[DOMAIN][entry][DATA_CONNECTOR]
            connector.client.call_method("printer.gcode.script", script=gcode)

    hass.services.async_register(DOMAIN, "run_gcode", run_gcode_command)
