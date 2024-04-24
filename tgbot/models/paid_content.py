from dataclasses import dataclass


@dataclass
class PaidContent:
    paid_content_id: int
    content_name: str
    url: str
    content_HTML: str
