#!/usr/bin/env python

from pyblique import error_rate, get_data, ObliqueClassifier
from sklearn.model_selection import KFold
import argparse
import os
import sys
import time


class Tee:

    def __init__(self, *args):
        self.outputs = args

    def __call__(self, s="", end="\n"):
        for o in self.outputs:
            o.write(s + end)


def run(fname, folds):
    st = time.time()
    data = get_data("Data/{}.data".format(fname))
    with open("Results/{}_{}folds.txt".format(fname, folds), "a") as f:
        tee = Tee(sys.stdout, f)
        tee("Validating classifier with {}-fold test...".format(folds))
        kfm = KFold(n_splits=folds)
        kf = kfm.split(data)
        avg_error = 0
        it = 1
        for train, test in kf:
            start = time.time()
            tee("Iteration #{}".format(it))
            oc = ObliqueClassifier()
            oc.fit(data[train])
            predictions = [oc.predict(r) for r in data[test]]
            actual_labels = data[test][:, -1]
            error = error_rate(predictions, actual_labels)
            tee("Error: {:.3f}".format(error))
            tee("Elapsed time: {:.3f} seconds".format(time.time() - start))
            tee()
            avg_error += error
            it += 1
        totaltime = time.time() - st
        tee("Average error: {:.3f}".format(avg_error/folds))
        tee("Total elapsed time: {:.3f} seconds.".format(totaltime))
        tee("Average elapsed time: {:.3f} seconds.".format(totaltime/folds))


if __name__ == "__main__":
    files = os.listdir("Data")
    files = [f.split(".")[0] for f in files]
    if not os.path.exists("Results"):
        os.makedirs("Results")
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folds", default=5, type=int,
                        help="Amount of folds")
    parser.add_argument("data", type=str, help="Name of dataset",
                        choices=files)

    args = parser.parse_args()
    run(args.data, args.folds)
