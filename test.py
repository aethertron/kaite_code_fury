#!/usr/bin/python2.7
from __future__ import print_function
#
from datetime import datetime
import pandas as pd
import sys
import numpy as np
from collections import OrderedDict


def test_write_to_xls():
    data_frame = pd.read_excel("test/combenefit_test.xlsx")

    print(dir(data_frame))

    data_frame.to_excel('test/test.xls', "Sheet1")


class compound_axis(object):

    def __init__(self, name, units, abscissa):
        self.name = name
        self.units = units
        self.abscissa = abscissa

    def __str__(self):
        string = '{clsname}'
        string += '{{name: {name}, units: {units}, abscissa: {abscissa}}}'
        return string.format(clsname=self.__class__.__name__,
                             name=self.name,
                             units=self.units,
                             abscissa=self.abscissa)


def parse_head(data):
    '''
    # type: (data) -> (title, row_axis, col_axis)
    # type: (DateFrame) -> (str, compound_axis, compound_axis)
    '''
    ndata = np.array(data)
    title = ndata[0, 0]
    row_abs = ndata[2, 2:][pd.notnull(ndata[2, 2:])]
    col_abs = ndata[3, 2:][pd.notnull(ndata[3, 2:])]
    row_axis = compound_axis(ndata[2, 0],  ndata[2, 1], row_abs)
    col_axis = compound_axis(ndata[3, 0],  ndata[3, 1], col_abs)
    return (title, row_axis, col_axis)


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

# * Final Frame


def form_data_frame(table, datestr, row_axis, col_axis):
    '''
    # type: (np.array, str, compound_axis, compound_axis) -> DataFrame
    '''
    index = pd.Index(row_axis.abscissa,
                         name=row_axis.name)
    index.tags = {'units': row_axis.units}
    columns = pd.Index(col_axis.abscissa,
                           name=col_axis.name)
    columns.tags = {'units': col_axis.units}
    frame = pd.DataFrame(table, index=index, columns=columns)
    frame.name = datestr
    frame.tags = {'datestr': datestr}
    return frame


def write_data_frame(filename, frame, row_axis, col_axis):
    '''
    #type: (str, pd.DataFrame, compound_axis, compound_axis) -> None
    writes xls file
    '''
    frame.to_excel(filename)

def test():
    filename = 'test/combenefit_test.xlsx'
    data = pd.read_excel(filename, header=None)
    (title, row_axis, col_axis) = parse_head(data)
    tables = parse_data(data)
    normalize = True
    for datestr in tables:
        table = tables[datestr]
        if normalize:
            table = normalize_table(table)
        # extract 8x8
        frame = form_data_frame(table[:8, :8], datestr, row_axis, col_axis)
        # last cols are to be added: they are col concentration 0 and row concentration 0
        marg_row_vec = pd.DataFrame(table[:, 8:9], frame.index, [0])  # col concentration 0
        marg_col_vec = pd.DataFrame(table[:, 9:10].T, [0], frame.columns) # row concentration 0
        # add marginals
        frame = pd.concat([frame, marg_row_vec], 1)
        frame = pd.concat([frame, marg_col_vec], 0)
        frame = frame.sort_index(0).sort_index(0)
        # hacky: for whatever reason, need to add back names (keep units elsewhere)
        frame.index.name = row_axis.name
        frame.columns.name = col_axis.name
        frame.iloc[0, 0] = 0.0
        # Sorted, throw out last/highest indicies
        rows, cols = frame.shape
        frame = frame.iloc[:rows - 1, :cols - 1]
        # Frame has been normalized, filtered and is ready for writing!
        write_data_frame('foo.xls', frame, row_axis, col_axis)
        # Sort by indicies

        break

    # debug
    return locals()


def main(args):
    print('----------------------------------------------------')
    print("--- this is a test at {0} ---".format(datetime.now()))
    print('----------------------------------------------------')

    test()


if __name__ == '__main__':
    main(sys.argv[1:])
