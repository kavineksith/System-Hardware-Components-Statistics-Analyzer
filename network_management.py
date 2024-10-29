import json
import psutil
import socket
import netifaces
import sys
from report_signatures import TimeStampGenerator


class NetworkManager:
    def __init__(self):
        self.data = {
            "interface_stats": {},
            "interface_addrs": {},
            "connections": {}
        }

    @staticmethod
    # Function to check localhost connectivity
    def check_localhost_connectivity():
        try:
            socket.gethostbyname('127.0.0.1')
            status = "PC is connected to localhost."
        except socket.gaierror:
            status = "PC isn't connected to localhost."
        finally:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).close()

        return status

    @staticmethod
    # Function to check network connectivity
    def check_network_connectivity():
        try:
            socket.gethostbyname('www.google.com')
            status = "PC is connected to the internet."
        except socket.gaierror:
            status = "PC isn't connected to the internet."
        finally:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).close()

        return status

    @staticmethod
    # Function to monitor network traffic
    def monitor_network_traffic():
        try:
            network = psutil.net_io_counters()
            return {
                'Network Traffic Information': {
                    'Send': f'{network.bytes_sent / (1024 ** 2):.2f} Mbps',
                    'Received': f'{network.bytes_recv / (1024 ** 2):.2f} Mbps',
                },
                'Extra Information': {
                    'Packets Sent': f'{network.packets_sent}',
                    'Packet Received': f'{network.packets_recv}',
                    'ErrorIn': f'{network.errin}',
                    'ErrorOut': f'{network.errout}',
                    'DropIn': f'{network.dropin}',
                    'DropOut': f'{network.dropout}'
                }
            }
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    def gather_interface_stats(self):
        """Gathers network interface statistics."""
        try:
            stats = psutil.net_if_stats()
            for iface, info in stats.items():
                self.data["interface_stats"][iface] = {
                    "isup": info.isup,
                    "duplex": self._get_duplex_name(info.duplex),
                    "speed": info.speed,
                    "mtu": info.mtu,
                    "flags": info.flags
                }
        except Exception as e:
            print(f"Error gathering interface stats: {e}")

    def gather_interface_addrs(self):
        """Gathers network interface addresses."""
        try:
            addrs = psutil.net_if_addrs()
            for iface, info_list in addrs.items():
                self.data["interface_addrs"][iface] = []
                for info in info_list:
                    self.data["interface_addrs"][iface].append({
                        "family": self._get_family_name(info.family),
                        "address": info.address,
                        "netmask": info.netmask,
                        "broadcast": info.broadcast,
                        "ptp": info.ptp
                    })
        except Exception as e:
            print(f"Error gathering interface addresses: {e}")

    def gather_connections(self, kind: str):
        """Gathers network connections of a specific kind."""
        try:
            connections = psutil.net_connections(kind=kind)
            self.data["connections"][kind] = []
            for conn in connections:
                self.data["connections"][kind].append({
                    "fd": conn.fd,
                    "family": self._get_family_name(conn.family),
                    "type": self._get_socket_type_name(conn.type),
                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "None",
                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "None",
                    "status": conn.status,
                    "pid": conn.pid if conn.pid is not None else 'None'
                })
        except Exception as e:
            print(f"Error gathering connections for kind='{kind}': {e}")

    def gather_all_info(self):
        """Gathers all network-related information."""
        self.gather_interface_stats()
        self.gather_interface_addrs()
        kinds = [
            "inet",  # IPv4 and IPv6
            "inet4", # IPv4
            "inet6", # IPv6
            "tcp",   # TCP
            "tcp4",  # TCP over IPv4
            "tcp6",  # TCP over IPv6
            "udp",   # UDP
            "udp4",  # UDP over IPv4
            "udp6",  # UDP over IPv6
            # "unix",  # UNIX socket (both UDP and TCP protocols)
            "all"    # All types
        ]
        for kind in kinds:
            self.gather_connections(kind)

    def _get_duplex_name(self, duplex):
        """Safely get the name of the duplex type."""
        try:
            return duplex.name
        except AttributeError:
            return str(duplex)

    def _get_family_name(self, family):
        """Safely get the name of the address family."""
        try:
            return family.name
        except AttributeError:
            return str(family)

    def _get_socket_type_name(self, socket_type):
        """Safely get the name of the socket type."""
        try:
            return socket_type.name
        except AttributeError:
            return str(socket_type)

    def to_json(self) -> str:
        """Returns the gathered data as a JSON string."""
        return json.dumps(self.data, indent=4)

    @staticmethod
    def get_network_info():
        """Gathers detailed network interface information.

        Returns:
            A dictionary containing network interface information.
        """

        # Mapping of address family integers to human-readable names
        addr_family_map = {
            netifaces.AF_INET: 'IPv4',
            netifaces.AF_INET6: 'IPv6',
            netifaces.AF_LINK: 'MAC'
        }

        network_info = {}

        try:
            interfaces = netifaces.interfaces()
            gateways = netifaces.gateways()  # Get the gateways information

            for interface in interfaces:
                addrs = netifaces.ifaddresses(interface)
                interface_info = {
                    'interface_name': interface,  # More meaningful key
                    'mac_address': None,  # Initialize MAC address as None
                    'default_gateway': None,  # Initialize gateway address as None
                    'ip_addresses': []  # Initialize a list to hold address info
                }
                
                # Get the MAC address if available
                if netifaces.AF_LINK in addrs:
                    mac_info = addrs[netifaces.AF_LINK][0]  # Get the first entry for the MAC address
                    interface_info['mac_address'] = mac_info.get('addr')  # Store the MAC address

                # Get the gateway address for the interface if available
                if 'default' in gateways:
                    for key, value in gateways['default'].items():
                        if value[1] == interface:  # Check if the interface matches
                            interface_info['default_gateway'] = value[0]  # Get the gateway address
                            break  # Exit the loop once the gateway is found

                # Replace None with "None" for gateway
                if interface_info['default_gateway'] is None:
                    interface_info['default_gateway'] = "None"

                for addr_family, addr_info in addrs.items():
                    for addr in addr_info:
                        # Translate addr_family to human-readable version
                        family_name = addr_family_map.get(addr_family, 'Unknown')
                        address_details = {
                            'address_family': family_name,  # More meaningful key
                            'ip_address': addr.get('addr') if addr.get('addr') is not None else "None",  # Replace None with "None"
                            'subnet_mask': addr.get('netmask') if addr.get('netmask') is not None else "None",  # Replace None with "None"
                            'broadcast_address': addr.get('broadcast') if addr.get('broadcast') is not None else "None",  # Replace None with "None"
                            'peer_address': addr.get('peer') if addr.get('peer') is not None else "None"  # Replace None with "None"
                        }
                        interface_info['ip_addresses'].append(address_details)  # Append address details to the list
                
                network_info[interface] = interface_info

            return network_info

        except Exception as e:
            # Log the error or handle it appropriately for your application
            print(f"Error getting network information: {str(e)}")

    @staticmethod
    # Function to manage network statistics
    def network_report():
        try:
            # Network Usage Statistics
            localhost_connectivity = NetworkManager().check_localhost_connectivity()
            network_connectivity = NetworkManager().check_network_connectivity()
            network_traffic = NetworkManager().monitor_network_traffic()

            statistics = {
                'Network Usage Statistics': {
                    'Localhost Connectivity': localhost_connectivity,
                    'Network Connectivity': network_connectivity,
                    'Network Traffic': network_traffic,
                    'Generated Time & Date': f'{TimeStampGenerator().generate_report()}'
                }
            }

            statistics_report = json.dumps(statistics, indent=4)
            deep_analyzer = NetworkManager()
            deep_analyzer.gather_all_info()
            deep_analyzed_report = deep_analyzer.to_json()

            network_interface_report = json.dumps(NetworkManager().get_network_info(), indent=4)

            # Combine the dictionaries instead of using update on JSON string
            combined_report = dict(json.loads(statistics_report), **json.loads(deep_analyzed_report), **json.loads(network_interface_report))

            result = json.dumps(combined_report, indent=4)
            json_output = json.loads(result)
            return json_output  # Return the JSON output as a string
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
