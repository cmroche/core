"""Binary sensors for Moonraker API integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_RUNNING,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .connector import APIConnector, generate_signal
from .const import DATA_CONNECTOR, DOMAIN, SIGNAL_UPDATE_PRINT_STATUS
from .entity import MoonrakerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the available Moonraker entities."""
    connector: APIConnector = hass.data[DOMAIN][config_entry.entry_id][DATA_CONNECTOR]
    entities: list[BinarySensorEntity] = [
        MoonrakerGenericBinarySensor(config_entry, connector, BINARY_SENSOR_TYPES)
    ]
    async_add_entities(entities)


@dataclass
class MoonrakerBinarySensorKeysMixin:
    """A class that describes binary sensor required keys."""

    value: Callable[[Any], bool] | None
    signal: str


@dataclass
class MoonrakerBinarySensorDescription(
    BinarySensorEntityDescription, MoonrakerBinarySensorKeysMixin
):
    """A class that describes binary sensor entities."""


BINARY_SENSOR_TYPES = MoonrakerBinarySensorDescription(
    key="is_printing",
    name="Print Status",
    signal=SIGNAL_UPDATE_PRINT_STATUS,
    value=lambda params: params["state"] in ["printing", "paused"],
    entity_registry_enabled_default=True,
    device_class=DEVICE_CLASS_RUNNING,
)


class MoonrakerGenericBinarySensor(MoonrakerEntity, BinarySensorEntity):
    """Binary sensor representing printing state."""

    entity_description: MoonrakerBinarySensorDescription

    def __init__(
        self,
        entry: ConfigEntry,
        connector: APIConnector,
        description: MoonrakerBinarySensorDescription,
    ) -> None:
        """Initialize a new printing binary sensor."""
        super().__init__(entry, connector, description.name)
        self.entity_description = description
        self.module_available = True
        self._attr_is_on = False
        self._attr_entity_registry_enabled_default = (
            description.entity_registry_enabled_default
        )

    async def async_added_to_hass(self) -> None:
        """Configure entity update handlers."""
        await super().async_added_to_hass()

        @callback
        def update_state(params: Any) -> None:
            """Entity state update."""
            try:
                if self.entity_description.value:
                    self._attr_is_on = self.entity_description.value(params)
                self.module_available = True
            except KeyError:
                pass
            else:
                self.async_write_ha_state()

        signal = generate_signal(self.entity_description.signal, self.entry.entry_id)
        self.async_on_remove(async_dispatcher_connect(self.hass, signal, update_state))
