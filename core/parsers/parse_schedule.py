from numpy import array
from pandas import read_csv
import os


def parse_num_sch_from(fname):
    """ parses numerical form of schedule that is generated from `Schedule.to_num_csv()` """
    nsch = read_csv(os.path.join(os.getcwd(), fname)).to_numpy()
    for i in nsch:
        i[4] = array([int(j) for j in i[4].split(",")])

    return nsch