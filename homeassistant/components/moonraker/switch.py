"""Switches for Moonraker API integration."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .connector import APIConnector, generate_signal
from .const import DATA_CONNECTOR, DOMAIN, SIGNAL_UPDATE_PRINT_STATUS
from .entity import MoonrakerEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the available Moonraker entities."""
    connector: APIConnector = hass.data[DOMAIN][config_entry.entry_id][DATA_CONNECTOR]
    entities: list[SwitchEntity] = [
        MoonrakerGenericSwitch(config_entry, connector, x) for x in SENSOR_TYPES
    ]
    async_add_entities(entities)


@dataclass
class MoonrakerSwitchKeysMixin:
    """A class that describes switch required keys."""

    action_on: str
    action_off: str
    value: Callable[[Any], Any] | None
    signal: str


@dataclass
class MoonrakerSwitchDescription(SwitchEntityDescription, MoonrakerSwitchKeysMixin):
    """A class that describes switches."""


SENSOR_TYPES = (
    MoonrakerSwitchDescription(
        key="pause_print",
        name="Pause Print",
        action_on="printer.print.pause",
        action_off="printer.print.resume",
        signal=SIGNAL_UPDATE_PRINT_STATUS,
        value=lambda params: params["state"] == "paused",
        entity_registry_enabled_default=True,
        icon="mdi:pause-octagon-outline",
    ),
)


class MoonrakerGenericSwitch(MoonrakerEntity, SwitchEntity):
    """Switches representing printing state."""

    entity_description: MoonrakerSwitchDescription

    def __init__(
        self,
        entry: ConfigEntry,
        connector: APIConnector,
        description: MoonrakerSwitchDescription,
    ) -> None:
        """Initialize a new printing switch."""
        super().__init__(entry, connector, description.name)
        self.entity_description = description
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
                    self._attr_is_on = bool(self.entity_description.value(params))
                self.module_available = True
            except KeyError:
                pass
            else:
                self.async_write_ha_state()

        signal = generate_signal(self.entity_description.signal, self.entry.entry_id)
        self.async_on_remove(async_dispatcher_connect(self.hass, signal, update_state))

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.connector.client.call_method(self.entity_description.action_on)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.connector.client.call_method(self.entity_description.action_off)
