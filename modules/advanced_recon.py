import socket
import requests
import dns.resolver
from concurrent.futures import ThreadPoolExecutor

class AdvancedRecon:
    def __init__(self, domain: str):
        self.domain = domain.replace("https://", "").replace("http://", "").strip("/")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def get_subdomains(self):
        """CRT.sh Certificate Logs માંથી સાઈટના બધા જ Subdomains શોધી લાવશે"""
        subdomains = set()
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for entry in data[:30]:
                    name = entry.get('name_value')
                    if name:
                        for sub in name.split('\n'):
                            if not sub.startswith("*."):
                                subdomains.add(sub.strip())
        except Exception:
            pass
        return list(subdomains)[:20]

    def find_real_ip(self, current_ip: str):
        """Direct Subdomains અને Direct MX Records ચેક કરીને રિયલ IP શોધશે"""
        potential_ips = set()
        
        # Direct MX records ચેક કરવા
        try:
            answers = dns.resolver.resolve(self.domain, 'MX')
            for rdata in answers:
                mx_host = str(rdata.exchange).rstrip('.')
                ip = socket.gethostbyname(mx_host)
                if ip and ip != current_ip:
                    potential_ips.add(f"{ip} (via MX: {mx_host})")
        except Exception:
            pass

        # Direct subdomains (ftp, cpanel, direct, mail) ચેક કરવા
        direct_subs = ['mail', 'ftp', 'cpanel', 'direct', 'direct-connect', 'dev', 'stage']
        for sub in direct_subs:
            try:
                sub_domain = f"{sub}.{self.domain}"
                ip = socket.gethostbyname(sub_domain)
                if ip and ip != current_ip:
                    potential_ips.add(f"{ip} (via {sub_domain})")
            except Exception:
                pass

        return list(potential_ips) if potential_ips else ["No Origin IP Discovered (Protected by CDN)"]

    def scan_port(self, ip, port):
        """પોર્ટ ખુલ્લો છે કે બંધ તે ચેક કરશે"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.2)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                return port
        except:
            pass
        return None

    def fast_port_scan(self, ip):
        """મુખ્ય પોર્ટ્સ સુપર-ફાસ્ટ મલ્ટી-થ્રેડીંગથી સ્કેન કરશે"""
        common_ports = [21, 22, 25, 53, 80, 110, 143, 443, 465, 993, 3306, 8080, 8443]
        open_ports = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(lambda p: self.scan_port(ip, p), common_ports)
            for port in results:
                if port:
                    open_ports.append(port)
        return open_ports if open_ports else ["No Open Ports Detected"]

    def run_all(self, current_ip: str = None):
        """બધો ડેટા એકસાથે ભેગો કરશે"""
        subdomains = self.get_subdomains()
        real_ips = self.find_real_ip(current_ip) if current_ip else []
        open_ports = self.fast_port_scan(current_ip) if current_ip else []

        return {
            "Subdomains Found": subdomains if subdomains else ["No Subdomains Found"],
            "Potential Real Origin IPs": real_ips,
            "Open Services & Ports": open_ports
        }
