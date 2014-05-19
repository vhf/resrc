from readability.readability import Document
from lxml.html import fragment_fromstring

def get_relevant(raw):
    try:
        cleaned = Document(raw).summary(True)
        et = fragment_fromstring(cleaned)
        return ' '.join(x.text for
                        x in et.getiterator()
                        if x.text)
    except Exception as e:
        print(e)
        return ''

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
    return sorted(extractor(text))[:10]

def get_keywords_from_url(url):
    return get_keywords(get_readable_text(url))
