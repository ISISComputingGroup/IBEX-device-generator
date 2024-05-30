import logging
import os

from lxml import etree
from lxml.etree import ElementTree

from paths import OPI_RESOURCES
from utils.device_info import OPI_KEY, DeviceInfo
from utils.templates import DeviceTemplate


class DuplicateOPIKeyError(Exception):
    """OPIs are identified by their keys and so this must be unique. This error indicates that an OPI key already exists."""

    pass


# Following xml entry is used in opi_info.xml which holds the
# collection of available device screens (entries) for the gui.
# fmt: off
template_opi_entry_xml_str = """
<entry>
    <key>@{opi_key}</key>
    <value>
        <type>UNKNOWN</type>
        <path>@{opi_file_name}.opi</path>
        <description>The OPI for the @{device_name}.</description>
        <macros>
            <macro>
            <name>@{ioc_name}</name>
            <description>The @{device_name} PV prefix (e.g. @{ioc_name}_01)</description>
            <default>@{ioc_name}_01</default>
            </macro>
        </macros>
        <categories></categories>
    </value>
</entry>
"""
# fmt: on


def _generate_opi_entry(device: DeviceInfo) -> ElementTree:
    """
    Generates an ElementTree entry for opi info based on a device info

    Args:
        device: The device info representing the new device

    Returns: ElementTree template based on the device info
    """

    concrete_opi_xml_str = DeviceTemplate(template_opi_entry_xml_str).apply(
        device
    )

    return etree.fromstring(
        concrete_opi_xml_str, etree.XMLParser(remove_blank_text=True)
    )


def add_device_opi_to_opi_info(device: DeviceInfo):
    """
    Add some basic template information to the opi_info.xml file

    Args:
        device: Key to identify to OPI to the GUI
    """

    log = logging.getLogger("rich")
    log.info("Adding template information to opi info")

    opi_info_path = os.path.join(OPI_RESOURCES, "opi_info.xml")
    with open(opi_info_path) as f:
        # Remove blank on input or pretty printing won't work later
        opi_xml = etree.parse(f, etree.XMLParser(remove_blank_text=True))

    opis = opi_xml.find("opis")
    opi_key = device[OPI_KEY]
    if any(entry.find("key").text == opi_key for entry in opis):
        raise DuplicateOPIKeyError(f"OPI with key '{opi_key}' already exists.")

    opis.append(_generate_opi_entry(device))
    with open(opi_info_path, "w") as f:
        f.write(
            etree.tostring(
                opi_xml,
                pretty_print=True,
                encoding="UTF-8",
                xml_declaration=True,
                standalone="yes",
            ).decode()
        )
