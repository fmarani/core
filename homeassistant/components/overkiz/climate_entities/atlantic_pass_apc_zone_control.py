"""Support for Atlantic Pass APC Zone Control."""
from typing import cast

from pyoverkiz.enums import OverkizCommand, OverkizCommandParam, OverkizState

from homeassistant.components.climate import ClimateEntity, HVACMode
from homeassistant.components.overkiz.entity import OverkizEntity
from homeassistant.const import TEMP_CELSIUS

OVERKIZ_TO_HVAC_MODE: dict[str, str] = {
    OverkizCommandParam.HEATING: HVACMode.HEAT,
    OverkizCommandParam.DRYING: HVACMode.DRY,
    OverkizCommandParam.COOLING: HVACMode.COOL,
    OverkizCommandParam.STOP: HVACMode.OFF,
}

HVAC_MODE_TO_OVERKIZ = {v: k for k, v in OVERKIZ_TO_HVAC_MODE.items()}


class AtlanticPassAPCZoneControl(OverkizEntity, ClimateEntity):
    """Representation of Atlantic Pass APC Zone Control."""

    _attr_hvac_modes = [*HVAC_MODE_TO_OVERKIZ]
    _attr_temperature_unit = TEMP_CELSIUS

    @property
    def hvac_mode(self) -> str:
        """Return hvac operation ie. heat, cool mode."""
        return OVERKIZ_TO_HVAC_MODE[
            cast(
                str, self.executor.select_state(OverkizState.IO_PASS_APC_OPERATING_MODE)
            )
        ]

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""
        await self.executor.async_execute_command(
            OverkizCommand.SET_PASS_APC_OPERATING_MODE, HVAC_MODE_TO_OVERKIZ[hvac_mode]
        )
