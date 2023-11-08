import requests
from html.parser import HTMLParser

allowed_tags = ()

class PageParser(HTMLParser):
    parsed = [];
    tag = ""
    def handle_starttag(self, tag, attrs):
        self.tag = tag
    def handle_data(self, data):
        if self.tag not in allowed_tags:
            return;
        self.parsed.append(data);
    def handle_endtag(self, tag):
        self.tag = ""

class TagExtractor:
    def __init__(self):
        self.parser = PageParser();
    def get_html_page(self, link: str):
        assert link.startswith("http"), f"{link} doesn't start with http."
        return requests.get(link, auth = ("user", "pass"))

    def parse_tags(self, link: str):
        r = self.get_html_page(link)
        html = r.text;

        self.parser.data = ""
        self.parser.feed(html)
        
        return self.parser.parsed
    def tags(self, tags = ()):
        global allowed_tags
        allowed_tags = tags

tagger = TagExtractor()
tagger.tags(["p", "h1"])
data = tagger.parse_tags("https://python.org");
