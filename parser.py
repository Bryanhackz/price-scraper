from html.parser import HTMLParser

class PriceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.price: float | None = None
        self._in_price_tag = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "p":
            attrs_dict = dict(attrs)
            if attrs_dict.get("class") == "price_color":
                self._in_price_tag = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "p" and self._in_price_tag:
            self._in_price_tag = False

    def handle_data(self, data: str) -> None:
        if self._in_price_tag:
            clean_data = "".join(c for c in data if c.isdigit() or c == ".")
            if clean_data:
                self.price = float(clean_data)

def extract_price(html_content: str) -> float:
    parser = PriceParser()
    parser.feed(html_content)
    if parser.price is None:
        raise ValueError("Could not find price in HTML")
    return parser.price