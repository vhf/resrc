# -*- coding: utf-8 -*-:
import urllib2
import hashlib
import os


def construct_body(link):
    if link.content in ['', '˘']:
        return
    try:
        opener = urllib2.build_opener()
        opener.addheaders = [('Accept-Charset', 'utf-8'), ('User-agent', 'Mozilla/5.0')]
        f = opener.open(link.url)

        data = f.read()
        f.close()
        opener.close()

        subtype = f.info().subtype

        if subtype == 'pdf':
            filename = hashlib.md5(link.url).hexdigest()

            thefile = open('/tmp/%s.pdf' % filename, "wb")
            thefile.write(data)
            thefile.close()

            os.system(("ps2ascii /tmp/%s.pdf /tmp/%s.txt") %(filename , filename))

            link.content = open("/tmp/%s.txt" % filename).read()
            link.save()

        elif subtype == 'html':
            from readability.readability import Document
            readable_article = Document(data).summary()
            link.content = readable_article
            link.save()
        else:
            link.content = u'˘'
            link.save()
    except:
        link.content = u'˘'
        link.save()
        pass
