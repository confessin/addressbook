#!/usr/bin/env python
# encoding: utf-8

"""
Test cases for AddressBook.
"""

__author__ = 'confessin@gmail.com (Mohammad Rafi)'

import unittest
import addressbook


class TestAddressBook(unittest.TestCase):
    """Test cases for Addressbook."""

    def setUp(self):
        addressbook.initialize_addressdata()
        addressbook.app.config['TESTING'] = True
        self.app = addressbook.app.test_client()

    def tearDown(self):
        pass

    def test_all_addresses(self):
        resp = self.app.get('/address')
        assert 'error' not in resp.data

    def test_single_address(self):
        resp = self.app.get('/address/1')
        assert 'name' in resp.data
        assert 'address' in resp.data

    def test_add_single_address(self):
        resp = self.app.post('/address?name=foo&id=5&address=rafias')
        assert 'rafias' in resp.data

    def test_edit_single_address(self):
        resp = self.app.put('/address?name=foo&id=1&address=rafias')
        assert 'rafias' in resp.data

    def test_edit_single_address_error(self):
        resp = self.app.put('/address?name=foo&id=3&address=rafias')
        assert 'ERROR' in resp.data

    def test_add_single_address_error(self):
        resp = self.app.post('/address?name=foo&id=1&address=rafias')
        assert 'ERROR' in resp.data


if __name__ == '__main__':
    unittest.main()
