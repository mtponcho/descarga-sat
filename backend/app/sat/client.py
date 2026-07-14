from satcfdi.models import Signer
from satcfdi.pacs.sat import SAT


class SATClient:

    def __init__(self, cer_path: str, key_path: str, password: str):

        self.signer = Signer.load(
            certificate=open(cer_path, "rb").read(),
            key=open(key_path, "rb").read(),
            password=password,
        )

        self.client = SAT(
            signer=self.signer
        )

    @property
    def rfc(self):
        return self.signer.rfc
