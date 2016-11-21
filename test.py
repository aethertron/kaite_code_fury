#!/usr/bin/python2.7
from __future__ import print_function
#
from datetime import datetime
import pandas
import sys
import numpy as np


def test_write_to_xls():
    data_frame = pandas.read_excel("combenefit_test.xlsx")

    print(dir(data_frame))

    # writer = pandas.ExcelWriter()
    data_frame.to_excel('test.xls', "Sheet1")
    # writer.save()


def parse_head(data):
    '''
    # type: (DateFrame) -> (title, (r_comp, r_unit), (c_comp, c_unit), row, col)
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
    # type: (DateFrame) -> List[np.array]
    '''
    pass


def test():
    filename = 'combenefit_test.xlsx'
    data = pandas.read_excel(filename, header=None)
    dummy = data


def main(args):
    print('----------------------------------------------------')
    print("--- this is a test at {0} ---".format(datetime.now()))
    print('----------------------------------------------------')

    test_write_to_xls()


if __name__ == '__main__':
    main(sys.argv[1:])
