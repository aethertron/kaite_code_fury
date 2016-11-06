#!/usr/bin/python2.7
from __future__ import print_function
#
from datetime import datetime 
import pandas
import sys



def test_write_to_xls(infile, outfile):
    data_frame = pandas.read_excel("combenefit_test.xlsx")

    print(dir(data_frame))

    writer = pandas.ExcelWriter('test.xls')
    data_frame.to_excel(writer, "Sheet1")
    writer.save()
    



def main(args):
    print('----------------------------------------------------')
    print("--- this is a test at {0} ---".format(datetime.now()))
    print('----------------------------------------------------')

    data_frame = pandas.read_excel("combenefit_test.xlsx")

    print(dir(data_frame))

    

if __name__ == '__main__':
    main(sys.argv[1:])


