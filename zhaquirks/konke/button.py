""" Konke button. """

import zigpy.types as t
from zigpy.profiles import zha
from zigpy.zcl.clusters.general import Basic, Identify, Groups, Scenes, OnOff, PowerConfiguration
from zigpy.quirks import CustomCluster, CustomDevice

from . import KONKE
from .. import PowerConfigurationCluster
from ..const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)

KONKE_CLUSTER_ID = 0xFCC0

class KonkeButtonEvent(t.enum8):
    SINGLE = 0x80
    LONG = 0x81
    DOUBLE = 0x82


class KonkeOnOff(CustomCluster, OnOff):
    cluster_id = OnOff.cluster_id

    attributes = OnOff.attributes.copy()
    attributes[0x0000] = ("on_off", KonkeButtonEvent)

    def _update_attribute(self, attrid, value):
        if attrid != 0x0000:
            return super()._update_attribute(attrid, value)

        # Call `self.listener_event` or something?


class KonkeButton(CustomDevice):
    """Custom device representing konke magnet sensors."""

    signature = {
        # <SimpleDescriptor endpoint=1 profile=260 device_type=2
        # device_version=0
        # input_clusters=[0, 1, 3, 4, 5, 6, 64704]
        # output_clusters=[3, 64704]>
        MODELS_INFO: [(KONKE, "3AFE170100510001")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_OUTPUT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    KONKE_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [Identify.cluster_id, KONKE_CLUSTER_ID],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_OUTPUT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    KonkeOnOff,
                    KONKE_CLUSTER_ID,
                ],
                OUTPUT_CLUSTERS: [Identify.cluster_id, KONKE_CLUSTER_ID],
            }
        }
    }
