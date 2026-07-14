from satcfdi.models import Signer


class SATClient:

    @staticmethod
    def load_signer(cer_path: str, key_path: str, password: str):

        signer = Signer.load(
            certificate=open(cer_path, "rb").read(),
            key=open(key_path, "rb").read(),
            password=password,
        )

        return signer
