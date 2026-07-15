import ssl, socket, OpenSSL
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import datetime

class SSLCertificate:
    def __init__(self, hostname: str, port=443):
        self.hostname = hostname
        self.port = port

    def get_cert_info(self) -> dict:
        try:
            cert = ssl.get_server_certificate((self.hostname, self.port))
            x509_cert = x509.load_pem_x509_certificate(cert.encode(), default_backend())
            issuer = x509_cert.issuer.rfc4514_string()
            subject = x509_cert.subject.rfc4514_string()
            not_before = x509_cert.not_valid_before_utc
            not_after = x509_cert.not_valid_after_utc
            serial_number = x509_cert.serial_number
            # Get SAN
            san = x509_cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
            san_list = san.value.get_values_for_type(x509.DNSName)
            return {
                "issuer": issuer,
                "subject": subject,
                "valid_from": str(not_before),
                "valid_to": str(not_after),
                "serial_number": serial_number,
                "san": san_list,
                "days_remaining": (not_after - datetime.datetime.utcnow()).days
            }
        except Exception as e:
            return {"error": str(e)}
