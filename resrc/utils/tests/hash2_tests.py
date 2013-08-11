# -*- coding: utf-8 -*-:
from django.test import TestCase

from resrc.utils.hash2 import hash2, base36encode


class TemplateTagsTests(TestCase):

    def test_base36encode_ok(self):
        '''Test if base36encoding works'''
        self.assertEqual(base36encode(666), 'ii')

    def test_base36encode_neg(self):
        '''Test if base36encoding works'''
        self.assertEqual(base36encode(-666), '-ii')

    def test_base36encode_neg_len(self):
        '''Test if base36encoding works'''
        self.assertEqual(base36encode(2), '2')

    def test_base36encode_not_number(self):
        with self.assertRaises(TypeError):
            base36encode('a')

    def test_hash2(self):
        '''Test hash2'''
        self.assertEqual(hash2('http://example.com'), 's1o0gijd8y')
