"""Support for interface with a Gree climate systems."""
import logging
from typing import List

from greeclimate.device import (
    FanSpeed,
    HorizontalSwing,
    Mode,
    TemperatureUnits,
    VerticalSwing,
)

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    FAN_AUTO,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    HVAC_MODE_AUTO,
    HVAC_MODE_COOL,
    HVAC_MODE_DRY,
    HVAC_MODE_FAN_ONLY,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_ECO,
    PRESET_NONE,
    PRESET_SLEEP,
    SUPPORT_FAN_MODE,
    SUPPORT_PRESET_MODE,
    SUPPORT_SWING_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    SWING_BOTH,
    SWING_HORIZONTAL,
    SWING_OFF,
    SWING_VERTICAL,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    PRECISION_WHOLE,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
)
from homeassistant.core import callback
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    COORDINATORS,
    DISPATCH_DEVICE_DISCOVERED,
    DOMAIN,
    FAN_MEDIUM_HIGH,
    FAN_MEDIUM_LOW,
    MAX_TEMP,
    MIN_TEMP,
    TARGET_TEMPERATURE_STEP,
)

_LOGGER = logging.getLogger(__name__)

HVAC_MODES = {
    Mode.Auto: HVAC_MODE_AUTO,
    Mode.Cool: HVAC_MODE_COOL,
    Mode.Dry: HVAC_MODE_DRY,
    Mode.Fan: HVAC_MODE_FAN_ONLY,
    Mode.Heat: HVAC_MODE_HEAT,
}
HVAC_MODES_REVERSE = {v: k for k, v in HVAC_MODES.items()}

PRESET_MODES = [
    PRESET_ECO,  # Power saving mode
    PRESET_AWAY,  # Steady heat, or 8C mode on gree units
    PRESET_BOOST,  # Turbo mode
    PRESET_NONE,  # Default operating mode
    PRESET_SLEEP,  # Sleep mode
]

FAN_MODES = {
    FanSpeed.Auto: FAN_AUTO,
    FanSpeed.Low: FAN_LOW,
    FanSpeed.MediumLow: FAN_MEDIUM_LOW,
    FanSpeed.Medium: FAN_MEDIUM,
    FanSpeed.MediumHigh: FAN_MEDIUM_HIGH,
    FanSpeed.High: FAN_HIGH,
}
FAN_MODES_REVERSE = {v: k for k, v in FAN_MODES.items()}

SWING_MODES = [SWING_OFF, SWING_VERTICAL, SWING_HORIZONTAL, SWING_BOTH]

SUPPORTED_FEATURES = (
    SUPPORT_TARGET_TEMPERATURE
    | SUPPORT_FAN_MODE
    | SUPPORT_PRESET_MODE
    | SUPPORT_SWING_MODE
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Gree HVAC device from a config entry."""

    @callback
    def init_device(coordinator):
        """Register the device."""
        async_add_entities([GreeClimateEntity(coordinator)])

    [init_device(coordinator) for coordinator in hass.data[DOMAIN].get(COORDINATORS)]
    async_dispatcher_connect(hass, DISPATCH_DEVICE_DISCOVERED, init_device)


class GreeClimateEntity(CoordinatorEntity, ClimateEntity):
    """Representation of a Gree HVAC device."""

    def __init__(self, device):
        """Initialize the Gree device."""
        super().__init__(device)
        self._device = device
        self._name = device.device_info.name
        self._mac = device.device_info.mac

    @property
    def name(self) -> str:
        """Return the name of the device."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique id for the device."""
        return self._mac

    @property
    def device_info(self):
        """Return device specific attributes."""
        return {
            "name": self._name,
            "identifiers": {(DOMAIN, self._mac)},
            "manufacturer": "Gree",
            "connections": {(CONNECTION_NETWORK_MAC, self._mac)},
        }

    @property
    def temperature_unit(self) -> str:
        """Return the temperature units for the device."""
        units = self._device.temperature_units
        return TEMP_CELSIUS if units == TemperatureUnits.C else TEMP_FAHRENHEIT

    @property
    def precision(self) -> float:
        """Return the precision of temperature for the device."""
        return PRECISION_WHOLE

    @property
    def current_temperature(self) -> float:
        """Return the target temperature, gree devices don't provide internal temp."""
        return self.target_temperature

    @property
    def target_temperature(self) -> float:
        """Return the target temperature for the device."""
        return self._device.target_temperature

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        if ATTR_TEMPERATURE not in kwargs:
            raise ValueError(f"Missing parameter {ATTR_TEMPERATURE}")

        temperature = kwargs[ATTR_TEMPERATURE]
        _LOGGER.debug(
            "Setting temperature to %d for %s",
            temperature,
            self._name,
        )

        self._device.target_temperature = round(temperature)
        await self._device.push_state_update()
        self.async_write_ha_state()

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature supported by the device."""
        return MIN_TEMP

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature supported by the device."""
        return MAX_TEMP

    @property
    def target_temperature_step(self) -> float:
        """Return the target temperature step support by the device."""
        return TARGET_TEMPERATURE_STEP

    @property
    def hvac_mode(self) -> str:
        """Return the current HVAC mode for the device."""
        if not self._device.power:
            return HVAC_MODE_OFF

        return HVAC_MODES.get(self._device.mode)

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        if hvac_mode not in self.hvac_modes:
            raise ValueError(f"Invalid hvac_mode: {hvac_mode}")

        _LOGGER.debug(
            "Setting HVAC mode to %s for device %s",
            hvac_mode,
            self._name,
        )

        if hvac_mode == HVAC_MODE_OFF:
            self._device.power = False
            await self._device.push_state_update()
            self.async_write_ha_state()
            return

        if not self._device.power:
            self._device.power = True

        self._device.mode = HVAC_MODES_REVERSE.get(hvac_mode)
        await self._device.push_state_update()
        self.async_write_ha_state()

    @property
    def hvac_modes(self) -> List[str]:
        """Return the HVAC modes support by the device."""
        modes = [*HVAC_MODES_REVERSE]
        modes.append(HVAC_MODE_OFF)
        return modes

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode for the device."""
        if self._device.steady_heat:
            return PRESET_AWAY
        if self._device.power_save:
            return PRESET_ECO
        if self._device.sleep:
            return PRESET_SLEEP
        if self._device.turbo:
            return PRESET_BOOST
        return PRESET_NONE

    async def async_set_preset_mode(self, preset_mode):
        """Set new preset mode."""
        if preset_mode not in PRESET_MODES:
            raise ValueError(f"Invalid preset mode: {preset_mode}")

        _LOGGER.debug(
            "Setting preset mode to %s for device %s",
            preset_mode,
            self._name,
        )

        self._device.steady_heat = False
        self._device.power_save = False
        self._device.turbo = False
        self._device.sleep = False

        if preset_mode == PRESET_AWAY:
            self._device.steady_heat = True
        elif preset_mode == PRESET_ECO:
            self._device.power_save = True
        elif preset_mode == PRESET_BOOST:
            self._device.turbo = True
        elif preset_mode == PRESET_SLEEP:
            self._device.sleep = True

        await self._device.push_state_update()
        self.async_write_ha_state()

    @property
    def preset_modes(self) -> List[str]:
        """Return the preset modes support by the device."""
        return PRESET_MODES

    @property
    def fan_mode(self) -> str:
        """Return the current fan mode for the device."""
        speed = self._device.fan_speed
        return FAN_MODES.get(speed)

    async def async_set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        if fan_mode not in FAN_MODES_REVERSE:
            raise ValueError(f"Invalid fan mode: {fan_mode}")

        self._device.fan_speed = FAN_MODES_REVERSE.get(fan_mode)
        await self._device.push_state_update()
        self.async_write_ha_state()

    @property
    def fan_modes(self) -> List[str]:
        """Return the fan modes support by the device."""
        return [*FAN_MODES_REVERSE]

    @property
    def swing_mode(self) -> str:
        """Return the current swing mode for the device."""
        h_swing = self._device.horizontal_swing == HorizontalSwing.FullSwing
        v_swing = self._device.vertical_swing == VerticalSwing.FullSwing

        if h_swing and v_swing:
            return SWING_BOTH
        if h_swing:
            return SWING_HORIZONTAL
        if v_swing:
            return SWING_VERTICAL
        return SWING_OFF

    async def async_set_swing_mode(self, swing_mode):
        """Set new target swing operation."""
        if swing_mode not in SWING_MODES:
            raise ValueError(f"Invalid swing mode: {swing_mode}")

        _LOGGER.debug(
            "Setting swing mode to %s for device %s",
            swing_mode,
            self._name,
        )

        self._device.horizontal_swing = HorizontalSwing.Center
        self._device.vertical_swing = VerticalSwing.FixedMiddle
        if swing_mode in (SWING_BOTH, SWING_HORIZONTAL):
            self._device.horizontal_swing = HorizontalSwing.FullSwing
        if swing_mode in (SWING_BOTH, SWING_VERTICAL):
            self._device.vertical_swing = VerticalSwing.FullSwing

        await self._device.push_state_update()
        self.async_write_ha_state()

    @property
    def swing_modes(self) -> List[str]:
        """Return the swing modes currently supported for this device."""
        return SWING_MODES

    @property
    def supported_features(self) -> int:
        """Return the supported features for this device integration."""
        return SUPPORTED_FEATURES
