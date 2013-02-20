#!/usr/bin/env python
# encoding: utf-8

"""
RESTful api with Flask for getting addresses.
"""

__author__ = 'confessin@gmail.com (Mohammad Rafi)'


import csv
import sqlite3
from flask import Flask
from flask import jsonify
from multiprocessing import Lock

app = Flask(__name__)
FILENAME = 'addresses.csv'
CSV_DELIMITER = '|_|'
ADDRESS_DATA = None


@app.route("/address", methods=['GET'])
def addresses():
    """@todo: Docstring for address

    :returns: @todo

    """
    return ADDRESS_DATA.get_all_addresses()


@app.route("/address/<address_id>", methods=['GET', 'POST', 'PUT'])
def address(address_id):
    """@todo: Docstring for address

    :returns: @todo

    """
    return ADDRESS_DATA.get_address(address_id)


@app.route("/address/<person_name>")
def address_by_name(arg1):
    """@todo: Docstring for address

    :arg1: @todo
    :returns: @todo

    """
    pass


@app.route("/")
def hello():
    return "Hello World!"


class AddressData(object):
    """Docstring for AddressData """
    _instance = None

    def __init__(self, filename):
        """Initializer for Address Data"""
        self._data = {}
        self.file_name = filename
        self.data_lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Implement a Singleton class."""
        if not cls._instance:
            cls._instance = super(AddressData, cls).__new__(
                    cls, *args, **kwargs)
        return cls._instance

    def initialize_dict(self):
        """Create a dictionary object from the file for searching.
        :returns: A dictionary object
        """
        self._data = {}
        with open(self.file_name) as f:
            for line in f:
                row = line.strip().split(CSV_DELIMITER)
                self._data[row[0].strip()] = {'name': row[1], 'address': row[2]}

    def initialize_db(self):
        """FIXME: Not used in this."""
        con = sqlite3.Connection('database.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE "addresses" ("id" varchar(12), '
                    '"name" varchar(12), "address" varchar(12));')
        f = open(self.file_name)
        csv_reader = csv.reader(f, delimiter=CSV_DELIMITER)

        cur.executemany('INSERT INTO addresses VALUES (?, ?, ?)', csv_reader)
        cur.close()
        con.commit()
        con.close()
        f.close()

    def get_address(self, idx):
        """Get specific address.

        :returns: the address if present else return an error.

        """
        with self.data_lock:
            return jsonify(self._data.get(idx,
                {'ERROR': 'No Address with given id found.'}))

    def get_all_addresses(self):
        """Get all Addresses data.

        :returns: @todo
        """
        return jsonify(self._data)


def initialize_addressdata():
    """@todo: Docstring for main
    :returns: @todo

    """
    global ADDRESS_DATA
    ADDRESS_DATA = AddressData(FILENAME)
    ADDRESS_DATA.initialize_dict()


if __name__ == "__main__":
    initialize_addressdata()
    app.run(debug=True)
