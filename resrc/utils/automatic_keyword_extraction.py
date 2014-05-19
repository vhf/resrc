from readability.readability import Document
from lxml.html import fragment_fromstring


def get_relevant(raw):
    raw = clean(raw)
    try:
        cleaned = Document(raw).summary(True)
        et = fragment_fromstring(cleaned)

        return ' '.join(x.text for
                        x in et.getiterator()
                        if x.text).strip()
    except Exception as e:
        print(e)
        return ''


def clean(text):
    from lxml import etree
    from lxml.etree import strip_elements, tostring
    tree = etree.fromstring(text, parser=etree.HTMLParser())
    code_tags = ['pre', 'code']
    strip_elements(tree, *code_tags)
    return tostring(tree, with_tail=False)


def get_readable_text(url):
    import urllib2
    opener = urllib2.build_opener()
    opener.addheaders = [('Accept-Charset', 'utf-8')]
    url_response = opener.open(url)
    raw_html = url_response.read().decode('utf-8')
    return get_relevant(raw_html)


def get_keywords(text):
    from topia.termextract import extract
    extractor = extract.TermExtractor()
    return sorted(extractor(text))[:20]


def get_keywords_from_url(url):
    return get_keywords(get_readable_text(url))
