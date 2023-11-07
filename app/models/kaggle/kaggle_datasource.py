import re


class KaggleDatasource:
    def __init__(self, slug, file_name, url: str = None):
        self.slug = slug
        self.file_name = file_name
        self.url = url
        extension = re.search(r"\.(\w+)$", file_name)
        self.file_ext = extension.group(1) if extension else False

    def to_dict(self, rel: dict = None) -> dict:
        return {
            "slug": self.slug,
            "file_name": self.file_name,
            "file_ext": self.file_ext,
            "file_url": self.url,
        }
