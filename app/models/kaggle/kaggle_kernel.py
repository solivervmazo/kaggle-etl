class KaggleKernel:
    def __init__(self, ref, title):
        self.ref = ref
        self.title = title

    def to_dict(self, rel: dict = None) -> dict:
        return {
            "ref": self.ref,
            "title": self.title,
        }
