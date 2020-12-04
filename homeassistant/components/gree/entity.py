"""Entity object for shared properties of Gree entities."""
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .bridge import DeviceDataUpdateCoordinator
from .const import DOMAIN


class GreeEntity(CoordinatorEntity):
    """Generic Gree entity (base class)."""

    def __init__(self, device: DeviceDataUpdateCoordinator, desc: str) -> None:
        """Initialize the entity."""
        super().__init__(device)
        self.device = device
        self._desc = desc
        self._name = f"{self.device.device_info.name}"
        self._mac = device.device_info.mac

    @property
    def name(self):
        """Return the name of the node."""
        return f"{self._name} {self._desc}"

    @property
    def unique_id(self):
        """Return the unique id based for the node."""
        return f"{self._mac}_{self._desc}"

    @property
    def device_info(self):
        """Return info about the device."""
        return {
            "identifiers": {(DOMAIN, self._mac)},
            "name": self._name,
            "manufacturer": "Gree",
            "connections": {(CONNECTION_NETWORK_MAC, self._mac)},
        }
