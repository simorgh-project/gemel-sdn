import re

from requests import HTTPError

from utils.rest import vtn_api_post, odl_api_get, odl_api_post
from utils.log import get_logger


logger = get_logger("vtn")


def setup_vtn(vtn_name, bridge_name):
    """
    Creates a new virtual tenant network with given name
    instantiates a vBridge inside it with given name
    :param vtn_name:
    :param bridge_name:
    :return:
    """

    vtn_api_post("/vtn:update-vtn", {
        "input": {
            "tenant-name": vtn_name
        }
    })

    vtn_api_post("/vtn-vbridge:update-vbridge", data={
        "input": {
            "tenant-name": vtn_name,
            "bridge-name": bridge_name
        }
    })


def _get_topology():
    """
    Receives network topology maintained by ODL based
    on SDN host-tracker and LLDM
    """
    return odl_api_get("/network-topology:network-topology/")


def get_switch_ofid(host_mac):
    """
    Finds the entry switch of the given host and returns its
    OpenFlow ID and the number of the port on which the host
    is connected
    """

    # fetch topology
    topology = _get_topology()["network-topology"]["topology"][0]

    # find host
    host = [n for n in topology["node"] if n["node-id"] == "host:%s" % host_mac][0]

    # find switch
    attached_switch_port = host["host-tracker-service:attachment-points"][0]["tp-id"]
    m = re.match(r"(.+:.+):(.+)", attached_switch_port)
    switch_id = m.group(1)
    switch_port_id = m.group(2)

    return switch_id, switch_port_id


def _new_iface_name(vtn_name):
    """
    Determines what the next interface name should be in
    a given VTN
    """

    vtn = _get_vtn_info(vtn_name)

    # get interface names
    interface_names = [i["name"] for i in vtn["vbridge"][0].get("vinterface", [{"name": "vtn0i0"}])]

    # get max interface number in names
    _max = max([int(re.match(r"[\d\w]+\w(\d+)", name).group(1)) for name in interface_names])

    # generate name in the format: "<VTN NAME>i<incremental number>"
    return "%si%d" % (vtn_name, _max + 1)


def _get_vtn_info(vtn_name):
    """
    Returns the info dictionary of a given VTN
    containing the virtual topology
    """

    # fetch vnet structure
    vnets = odl_api_get("/vtn:vtns/")

    # find desired vtn
    vtn = [d for d in vnets["vtns"]["vtn"] if d["name"] == vtn_name][0]

    return vtn


def _get_current_interface(host_mac):
    """
    Returns the current virtual net, interface and bridge
    to which a given host is connected
    """

    switch_id, port_id = get_switch_ofid(host_mac)
    ofname = "%s:%s" % (switch_id, port_id)

    vnets = odl_api_get("/vtn:vtns/")["vtns"]["vtn"]

    for vnet in vnets:
        for interface in vnet.get("vbridge", [{}])[0].get("vinterface", []):
            if interface.get("vinterface-status", {}).get("mapped-port", None) == ofname:
                return vnet["name"], interface["name"], vnet["vbridge"][0]["name"]

    return None


def remove_from_vtn(host_mac):
    """
    Removes a given host from the VTN to which it is
    connected
    """

    vtn, iface, vbr = _get_current_interface(host_mac)
    logger.info("Host currently connected to %s (iface %s on %s)", vtn, iface, vbr)

    vtn_api_post("/vtn-vinterface:remove-vinterface", data={
        "input": {
            "tenant-name": vtn,
            "bridge-name": vbr,
            "interface-name": iface
        }
    })

    logger.info("Successfully removed %s from %s", host_mac, vtn)

    return vtn


def connect_to_vtn(host_mac, vtn):
    """
    Connects the given host to the given VTN
    """

    # get bridge name
    bridge_name = _get_vtn_info(vtn)["vbridge"][0]["name"]

    # get connected switch id
    switch_id, port_id = get_switch_ofid(host_mac)
    logger.info("Entry switch: %s port %s", switch_id, port_id)

    # generate new incremental name
    iface_name = _new_iface_name(vtn)

    vtn_api_post("/vtn-vinterface:update-vinterface", data={
        "input": {
            "tenant-name": vtn,
            "bridge-name": bridge_name,
            "interface-name": iface_name
        }
    })

    logger.info("Created interface %s on %s", iface_name, vtn)

    vtn_api_post("/vtn-port-map:set-port-map", data={
        "input": {
            "tenant-name": vtn,
            "bridge-name": bridge_name,
            "interface-name": iface_name,
            "node": switch_id,
            "port-id": port_id
        }
    })

    logger.info("Successfully connected %s to %s", host_mac, vtn)


def reassign_vtn(host_mac, new_vtn_name, safe=False):
    if safe:
        if _get_current_interface(host_mac):
            remove_from_vtn(host_mac)
        else:
            logger.info("Host %s not assigned to any VTNs", host_mac)
    else:
        remove_from_vtn(host_mac)
    connect_to_vtn(host_mac, new_vtn_name)


if __name__ == "__main__":
    # reassign_vtn("1a:e1:a2:ca:cc:30", "vnet2")
    # print(get_new_iface_name("vnet1"))
    # print(_get_current_interface("1a:e1:a2:ca:cc:30"))
    # remove_from_vtn("1a:e1:a2:ca:cc:30")
    # connect_to_vtn("1a:e1:a2:ca:cc:30", "vnet1")
    reassign_vtn("1a:e1:a2:ca:cc:30", "vnet2", safe=True)


