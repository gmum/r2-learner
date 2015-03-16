import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import pickle
import numpy as np
from fit_models import grid_search
from r2 import R2SVMLearner
from datetime import datetime
from data_api import fetch_small_datasets, fetch_uci_datasets, fetch_medium_datasets
from misc.experiment_utils import get_logger
from misc.config import c


def main():

    type = 'small_' # small, medium, large
    exp_name = 'R2SVM_grid_' + type + str(datetime.now().time())[:-7]

    params = {'C': [np.exp(i) for i in xrange(-2, 6)],
              'beta': [0.05 * i for i in xrange(1, 5)],
              'depth': [i for i in xrange(2,10,3)],
              'fit_c': [None],
              'activation': ['sigmoid'],
              'scale': [True, False], #[True, False],
              'recurrent': [True, False],
              'use_prev': [True, False],
              'seed': [666]}

    datasets = fetch_medium_datasets()

    model = R2SVMLearner()
    logger = get_logger(exp_name, to_file=False)
    results = {d.name: {} for d in datasets}
    monitors = {d.name: {} for d in datasets}

    for data in datasets:
        exp = grid_search(model, data, params, logger=logger, verbose=1)
        results[data.name] = exp['results']
        monitors[data.name] = exp['monitors']
        results[data.name].update(monitors[data.name])
        print data.name + " done!"

    ret = pd.DataFrame.from_dict(results)

    f = open(os.path.join(c["RESULTS_DIR"],exp_name + '.pkl'), 'wb')
    pickle.dump(ret, f)
    f.close()

if __name__ == '__main__':
    main()
