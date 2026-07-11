from cryptography import x509
from cryptography.hazmat.backends import default_backend


def read_certificate(path: str) -> dict:
    with open(path, "rb") as f:
        data = f.read()

    cert = x509.load_der_x509_certificate(data, default_backend())

    return {
        "serial_number": str(cert.serial_number),
        "subject": cert.subject.rfc4514_string(),
        "issuer": cert.issuer.rfc4514_string(),
        "not_before": cert.not_valid_before_utc.isoformat(),
        "not_after": cert.not_valid_after_utc.isoformat(),
    }
