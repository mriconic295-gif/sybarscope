import dns.resolver
from typing import List, Dict, Optional

class DNSLookup:
    def __init__(self, domain: str):
        self.domain = domain
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 5
        self.resolver.lifetime = 5

    def lookup_a(self) -> List[str]:
        try:
            answers = self.resolver.resolve(self.domain, 'A')
            return [str(r) for r in answers]
        except Exception as e:
            return [f"Error: {str(e)}"]

    def lookup_aaaa(self) -> List[str]:
        try:
            answers = self.resolver.resolve(self.domain, 'AAAA')
            return [str(r) for r in answers]
        except Exception as e:
            return [f"Error: {str(e)}"]

    def lookup_mx(self) -> List[str]:
        try:
            answers = self.resolver.resolve(self.domain, 'MX')
            return [f"{r.preference} {r.exchange}" for r in answers]
        except Exception as e:
            return [f"Error: {str(e)}"]

    def lookup_ns(self) -> List[str]:
        try:
            answers = self.resolver.resolve(self.domain, 'NS')
            return [str(r) for r in answers]
        except Exception as e:
            return [f"Error: {str(e)}"]

    def lookup_txt(self) -> List[str]:
        try:
            answers = self.resolver.resolve(self.domain, 'TXT')
            return [str(r) for r in answers]
        except Exception as e:
            return [f"Error: {str(e)}"]

    def lookup_cname(self) -> Optional[str]:
        try:
            answers = self.resolver.resolve(self.domain, 'CNAME')
            return str(answers[0])
        except Exception:
            return None

    def lookup_soa(self) -> List[str]:
        try:
            answers = self.resolver.resolve(self.domain, 'SOA')
            soa = answers[0]
            return [f"mname={soa.mname}, rname={soa.rname}, serial={soa.serial}"]
        except Exception as e:
            return [f"Error: {str(e)}"]

    def all_lookups(self) -> dict:
        return {
            "A": self.lookup_a(),
            "AAAA": self.lookup_aaaa(),
            "MX": self.lookup_mx(),
            "NS": self.lookup_ns(),
            "TXT": self.lookup_txt(),
            "CNAME": self.lookup_cname(),
            "SOA": self.lookup_soa()
        }
