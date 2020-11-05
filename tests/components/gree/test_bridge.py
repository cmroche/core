"""Tests for the Gree Integration."""

from homeassistant.components.gree.bridge import DeviceHelper
from homeassistant.components.gree.const import DISCOVERY_REFRESH_TIME

from .common import build_device_mock

from tests.async_mock import patch


async def test_discovery_returns_devices(hass, discovery):
    """Test that the helper returns info for the discovered devices."""
    MockDevice1 = build_device_mock(
        name="fake-device-1", ipAddress="1.1.1.1", mac="aabbcc112233"
    )
    MockDevice2 = build_device_mock(
        name="fake-device-2", ipAddress="2.2.2.2", mac="bbccdd223344"
    )

    discovery.return_value = [MockDevice1.device_info, MockDevice2.device_info]

    DeviceHelper.next_discovery_time = 0.0
    infos = await DeviceHelper.find_devices()
    assert len(infos) == 2
    assert discovery.call_count == 1


async def test_discovery_caches_devices(hass, discovery):
    """Test that the helper caches discovered devices."""
    MockDevice1 = build_device_mock(
        name="fake-device-1", ipAddress="1.1.1.1", mac="aabbcc112233"
    )
    MockDevice2 = build_device_mock(
        name="fake-device-2", ipAddress="2.2.2.2", mac="bbccdd223344"
    )
    MockDevice3 = build_device_mock(
        name="fake-device-3", ipAddress="3.3.3.3", mac="aabbcc112244"
    )
    MockDevice4 = build_device_mock(
        name="fake-device-4", ipAddress="4.4.4.4", mac="bbccdd223355"
    )

    discovery.return_value = [MockDevice1.device_info, MockDevice2.device_info]
    DeviceHelper.next_discovery_time = 0.0

    with patch("homeassistant.components.gree.bridge.monotonic") as monotonic_mock:
        monotonic_mock.return_value = 0.0
        infos1 = await DeviceHelper.find_devices()
        assert len(infos1) == 2
        assert discovery.call_count == 1

    discovery.return_value = [MockDevice3.device_info, MockDevice4.device_info]

    # The results should still be cached
    with patch("homeassistant.components.gree.bridge.monotonic") as monotonic_mock:
        monotonic_mock.return_value = 1.0

        infos2 = await DeviceHelper.find_devices()
        assert len(infos2) == 2
        assert infos2 == [MockDevice1.device_info, MockDevice2.device_info]
        assert discovery.call_count == 1

    # The cache should expire and results be updated
    with patch("homeassistant.components.gree.bridge.monotonic") as monotonic_mock:
        monotonic_mock.return_value = DISCOVERY_REFRESH_TIME

        infos3 = await DeviceHelper.find_devices()
        assert len(infos3) == 2
        assert infos3 == [MockDevice3.device_info, MockDevice4.device_info]
        assert discovery.call_count == 2


async def test_discovery_forces_update_of_devices(hass, discovery):
    """Test that the helper caches discovered devices."""
    MockDevice1 = build_device_mock(
        name="fake-device-1", ipAddress="1.1.1.1", mac="aabbcc112233"
    )
    MockDevice2 = build_device_mock(
        name="fake-device-2", ipAddress="2.2.2.2", mac="bbccdd223344"
    )
    MockDevice3 = build_device_mock(
        name="fake-device-3", ipAddress="3.3.3.3", mac="aabbcc112244"
    )
    MockDevice4 = build_device_mock(
        name="fake-device-4", ipAddress="4.4.4.4", mac="bbccdd223355"
    )

    discovery.return_value = [MockDevice1.device_info, MockDevice2.device_info]
    DeviceHelper.next_discovery_time = 0.0

    with patch("homeassistant.components.gree.bridge.monotonic") as monotonic_mock:
        monotonic_mock.return_value = 0.0
        infos1 = await DeviceHelper.find_devices()
        assert len(infos1) == 2
        assert discovery.call_count == 1

    discovery.return_value = [MockDevice3.device_info, MockDevice4.device_info]

    # The results should still be cached
    with patch("homeassistant.components.gree.bridge.monotonic") as monotonic_mock:
        monotonic_mock.return_value = 1.0

        infos2 = await DeviceHelper.find_devices(force_update=True)
        assert len(infos2) == 2
        assert infos2 == [MockDevice3.device_info, MockDevice4.device_info]
        assert discovery.call_count == 2

    # The cache should expire and results be updated
    with patch("homeassistant.components.gree.bridge.monotonic") as monotonic_mock:
        monotonic_mock.return_value = 2.0

        infos3 = await DeviceHelper.find_devices()
        assert len(infos3) == 2
        assert infos3 == [MockDevice3.device_info, MockDevice4.device_info]
        assert discovery.call_count == 2
