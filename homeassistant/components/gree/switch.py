"""Support for interface with a Gree climate systems."""
import logging
from typing import Optional

from homeassistant.components.switch import DEVICE_CLASS_SWITCH, SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import COORDINATORS, DISPATCH_DEVICE_DISCOVERED, DOMAIN
from .entity import GreeEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Gree HVAC device from a config entry."""

    @callback
    def init_device(coordinator):
        """Register the device."""
        async_add_entities(
            [
                GreePanelLightSwitchEntity(coordinator),
                GreeQuietModeSwitchEntity(coordinator),
                GreeFreshAirSwitchEntity(coordinator),
                GreeXFanSwitchEntity(coordinator),
                GreeTurboSwitchEntity(coordinator),
            ]
        )

    [init_device(x) for x in hass.data[DOMAIN][COORDINATORS]]
    async_dispatcher_connect(hass, DISPATCH_DEVICE_DISCOVERED, init_device)


class GreePanelLightSwitchEntity(GreeEntity, SwitchEntity):
    """Representation of the front panel light on the device."""

    def __init__(self, device):
        """Initialize the Gree device."""
        super().__init__(device, "Panel Light")

    @property
    def icon(self) -> Optional[str]:
        """Return the icon for the device."""
        return "mdi:lightbulb"

    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> bool:
        """Return if the light is turned on."""
        return self.device.light

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        self.device.light = True
        await self.device.push_state_update()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        self.device.light = False
        await self.device.push_state_update()
        self.async_write_ha_state()


class GreeQuietModeSwitchEntity(GreeEntity, SwitchEntity):
    """Representation of the quiet mode state of the device."""

    def __init__(self, device):
        """Initialize the Gree device."""
        super().__init__(device, "Quiet")

    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> bool:
        """Return if the state is turned on."""
        return self.device.quiet

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        self.device.quiet = True
        await self.device.push_state_update()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        self.device.quiet = False
        await self.device.push_state_update()
        self.async_write_ha_state()


class GreeFreshAirSwitchEntity(GreeEntity, SwitchEntity):
    """Representation of the fresh air mode state of the device."""

    def __init__(self, device):
        """Initialize the Gree device."""
        super().__init__(device, "Fresh Air")

    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> bool:
        """Return if the state is turned on."""
        return self.device.fresh_air

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        self.device.fresh_air = True
        await self.device.push_state_update()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        self.device.fresh_air = False
        await self.device.push_state_update()
        self.async_write_ha_state()


class GreeXFanSwitchEntity(GreeEntity, SwitchEntity):
    """Representation of the extra fan mode state of the device."""

    def __init__(self, device):
        """Initialize the Gree device."""
        super().__init__(device, "XFan")

    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> bool:
        """Return if the state is turned on."""
        return self.device.xfan

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        self.device.xfan = True
        await self.device.push_state_update()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        self.device.xfan = False
        await self.device.push_state_update()
        self.async_write_ha_state()


class GreeTurboSwitchEntity(GreeEntity, SwitchEntity):
    """Representation of the turbo mode state of the device."""

    def __init__(self, device):
        """Initialize the Gree device."""
        super().__init__(device, "Turbo")

    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return DEVICE_CLASS_SWITCH

    @property
    def is_on(self) -> bool:
        """Return if the state is turned on."""
        return self.device.turbo

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        self.device.turbo = True
        await self.device.push_state_update()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        self.device.turbo = False
        await self.device.push_state_update()
        self.async_write_ha_state()
