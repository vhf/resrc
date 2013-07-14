# -*- coding: utf-8 -*-:
import re
import random

from markdown.postprocessors import Postprocessor
from markdown.extensions import Extension

HTMLELEMENTS = ['p', 'a', 'div', 'blockquote', 'hr']
HTMLATTRIBUTES = ['style', 'id', 'href', 'class']
STYLE_REG = reg = re.compile(r'\[([a-z]+)\]\{(.+?)\r?\n\}', re.DOTALL)

getStyle = lambda tag, blockcontent, blockid: {
    'secret': {
    '1hr': {},
        '7div':
        {'class':
            ['hidden-block'],
         'id':
         ['show-' + str(blockid)],
         'text':
         {'3p_':
          {'text':
           blockcontent
           },
          '1a':
          {'href':
           '#show-' + str(blockid),
    'id':
           'display-' + str(blockid),
    'class':
    ['hidden-link-show'],
    'text':
    u'Contenu masqué (cliquez pour afficher)',
          },
             '2a':
             {'href':
              '#hide-' + str(blockid),
              'id':
              'hide-' + str(blockid),
              'class':
              ['hidden-link-hide'],
              'text':
              'Masquer le contenu',
              },
         },
        },
        '4hr': {}


    },
}[tag]


class Element():
    __tag = None
    __attrs = {}
    __text = ""

    def __init__(self, tag):
        self.__tag = tag
        self.__attrs = {}
        self.__text = ""

    def setattr(self, name, value):
        self.__attrs[name] = unicode(value)

    def settext(self, text):
        self.__text = unicode(text)

    def completeWith(self, elem):
        for attr in elem.__attrs:
            self.setattr(attr, elem.__attrs[attr])
        self.__text = elem.__text

    def __repr__(self):
        def formatAttr(name, value):
            return unicode(name) + '="' + unicode(value) + '"'
        if len(self.__text) > 0:
            return '<' + unicode(self.__tag) + ' ' + \
                ' '.join([formatAttr(attr, self.__attrs[attr]) for attr in self.__attrs.keys()]
                         ) + '>' + unicode(self.__text) + '</' + unicode(self.__tag) + '>'
        else:
            return '<' + unicode(self.__tag) + ' ' + \
                ' '.join([formatAttr(attr, self.__attrs[attr]) for attr in self.__attrs.keys()]
                         ) + ' />'


def cleanElement(element_name):
    return re.sub(r'(?:[0-9]*)([a-z]+)_*', r'\1', element_name)


def localProcess(elements, parent=None):
    for elem in elements.keys():
        value = elements[elem]
        if cleanElement(elem) in HTMLELEMENTS:
            el = Element(cleanElement(elem))
            for e in localProcess(value, el):
                el = e
            yield el
        elif elem in HTMLATTRIBUTES:
            if isinstance(value, str) or isinstance(value, unicode):
                parent.setattr(elem, value)
            elif isinstance(value, list):
                parent.setattr(elem, ' '.join(value))
            elif isinstance(value, dict):
                parent.setattr(elem, ';'.join(
                    [':'.join([n, value[n]]) for n in value]))
            else:
                parent.setattr(elem, value)
            yield parent
        elif elem == 'text':
            if isinstance(value, dict):
                parent.settext(''.join([unicode(a)
                               for a in localProcess(value)]))
            elif isinstance(value, str) or isinstance(value, unicode):
                parent.settext(unicode(value))
            elif isinstance(value, list):
                parent.settext(' '.join(value))
            else:
                parent.settext("")
            yield parent
        else:
            yield parent


def processStyle(styles):
    return ''.join([unicode(a) for a in localProcess(styles)])


def process(match):
    try:
        return processStyle(getStyle(match.group(1), match.group(2), random.randint(1000, 9999)))
    except KeyError:
        return "Style non-valide"


class CSSPostprocessor(Postprocessor):

    def run(self, text):
        return re.sub(STYLE_REG, process, text, re.DOTALL)


class StyleExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        md.postprocessors.add('cssstyle', CSSPostprocessor(md), '_begin')
