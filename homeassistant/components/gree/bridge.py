"""Helper and wrapper classes for Gree module."""
from time import monotonic
from typing import List

from greeclimate.device import Device, DeviceInfo
from greeclimate.discovery import Discovery
from greeclimate.exceptions import DeviceNotBoundError

from homeassistant import exceptions

from .const import DISCOVERY_REFRESH_TIME


class DeviceHelper:
    """Device search and bind wrapper for Gree platform."""

    next_discovery_time = 0.0
    last_discovered_devices = []

    @staticmethod
    async def try_bind_device(device_info: DeviceInfo) -> Device:
        """Try and bing with a discovered device.

        Note the you must bind with the device very quickly after it is discovered, or the
        process may not be completed correctly, raising a `CannotConnect` error.
        """
        device = Device(device_info)
        try:
            await device.bind()
        except DeviceNotBoundError as exception:
            raise CannotConnect from exception
        return device

    @staticmethod
    async def find_devices(force_update: bool = False) -> List[DeviceInfo]:
        """Gather a list of device infos from the local network."""

        if force_update or monotonic() >= DeviceHelper.next_discovery_time:
            DeviceHelper.next_discovery_time = monotonic() + DISCOVERY_REFRESH_TIME
            DeviceHelper.last_discovered_devices = await Discovery.search_devices()

        return DeviceHelper.last_discovered_devices


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
