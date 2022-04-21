"""Button entities for Moonraker API integration."""
from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .connector import APIConnector
from .const import DATA_CONNECTOR, DOMAIN
from .entity import MoonrakerEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the available Moonraker entities."""
    connector: APIConnector = hass.data[DOMAIN][config_entry.entry_id][DATA_CONNECTOR]
    entities: list[ButtonEntity] = [
        MoonrakerGenericButtonSensor(config_entry, connector, x) for x in BUTTON_TYPES
    ]
    async_add_entities(entities)


@dataclass
class MoonrakerButtonKeysMixin:
    """A class the represents required keys for button description."""

    action: str
    available_when_not_ready: bool


@dataclass
class MoonrakerButtonDescription(ButtonEntityDescription, MoonrakerButtonKeysMixin):
    """A class that describes button entities."""


BUTTON_TYPES = (
    MoonrakerButtonDescription(
        key="emergency_stop",
        name="Emergency Stop",
        action="printer.emergency_stop",
        entity_registry_enabled_default=True,
        available_when_not_ready=True,
        icon="mdi:alert-octagon",
    ),
    MoonrakerButtonDescription(
        key="host_restart",
        name="Host Restart",
        action="printer.restart",
        entity_registry_enabled_default=True,
        available_when_not_ready=True,
        icon="mdi:restart",
    ),
    MoonrakerButtonDescription(
        key="firmware_restart",
        name="Firmware Restart",
        action="printer.firmware_restart",
        entity_registry_enabled_default=True,
        available_when_not_ready=True,
        icon="mdi:restart",
    ),
    MoonrakerButtonDescription(
        key="cancel_print",
        name="Cancel Print",
        action="printer.print.cancel",
        entity_registry_enabled_default=True,
        available_when_not_ready=False,
        icon="mdi:restart",
    ),
)


class MoonrakerGenericButtonSensor(MoonrakerEntity, ButtonEntity):
    """Binary sensor representing printing state."""

    entity_description: MoonrakerButtonDescription

    def __init__(
        self,
        entry: ConfigEntry,
        connector: APIConnector,
        description: MoonrakerButtonDescription,
    ) -> None:
        """Initialize a new printing binary sensor."""
        super().__init__(entry, connector, description.name)
        self.entity_description = description
        self.module_available = True
        self._attr_entity_registry_enabled_default = (
            description.entity_registry_enabled_default
        )

    async def async_press(self) -> None:
        """Call the action associated to the button press."""
        await self.connector.client.call_method(self.entity_description.action)

    @property
    def available(self) -> bool:
        """Return True if the entity is available, False otherwise."""
        return self._attr_available
