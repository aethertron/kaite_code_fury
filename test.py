#!/usr/bin/python2.7
from __future__ import print_function
#
from datetime import datetime
import pandas
import sys
import numpy as np
from collections import OrderedDict


def test_write_to_xls():
    data_frame = pandas.read_excel("test/combenefit_test.xlsx")

    print(dir(data_frame))

    data_frame.to_excel('test/test.xls', "Sheet1")


def parse_head(data):
    '''
    # type: (DateFrame) ->
    #   (title, (r_comp, r_unit), (c_comp, c_unit), row, col)
    '''
    ndata = np.array(data)
    title = ndata[0, 0]
    #
    r_comp = ndata[2, 0]
    r_unit = ndata[2, 1]
    row = ndata[2, 2:]
    #
    c_comp = ndata[3, 0]
    c_unit = ndata[3, 1]
    col = ndata[3, 2:]
    #
    return (title, (r_comp, r_unit), (c_comp, c_unit), row, col)


def parse_data(data, remove_head=True):
    '''
    # type: (DateFrame) -> OrderedDict[datestring, np.array]
    '''
    ndata = np.array(data)
    start = 5 if remove_head else 0
    cnt, rem = divmod(ndata.shape[0] - start, 10)
    if rem != 9:
        raise ValueError("Should have (table_count - 1) x 10 + 9 rows after "
                         "header, have this instead: {0}"
                         .format(ndata.shape[0] - start))
    table_count = cnt + 1
    tables = OrderedDict()
    for ii in range(table_count):
        table_start = start + ii * 10
        datestring = ndata[table_start, 0]
        table = ndata[table_start + 1:table_start + 1 + 8]
        tables[datestring] = table
    return tables


# * Table Normalization


def normalize_table(table):
    '''
    # type: (np.array) -> (np.array)
    Maps 8x11/12 matrix to 8x10 matrix

    Concept: we throw out the 12th column if present
      we then find the mean along the 11th column
      we then divide everything by this mean
    '''
    norm = table[:, 10].mean()
    data = table[:, :10] / norm
    return data


def test():
    filename = 'test/combenefit_test.xlsx'
    data = pandas.read_excel(filename, header=None)
    parsed = parse_head(data)
    (title, (r_comp, r_unit), (c_comp, c_unit), r_axis, c_axis) = parsed
    tables = parse_data(data)
    normalize = True
    for table in tables:
        table = normalize_table(table)


    # debug
    return locals()


def main(args):
    print('----------------------------------------------------')
    print("--- this is a test at {0} ---".format(datetime.now()))
    print('----------------------------------------------------')

    test()


if __name__ == '__main__':
    main(sys.argv[1:])
