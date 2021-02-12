import argparse

import sklearn.metrics as skl
import seqeval.metrics as sqe
from seqeval.scheme import IOB2

def readfile(filename):
    data = []
    sentence = []
    labels = []
    f = open(filename)
    for line in f:
        if len(line) == 0 or line.startswith('-DOCSTART') or line[0]=="\n":
            if len(sentence) > 0:
                data.append((sentence, labels))
                sentence = []
                labels = []
            continue
        splits = line.split('\t')
        sentence.append(splits[0])
        labels.append(splits[-1][:-1])

    if len(sentence) > 0:
        data.append((sentence, labels))
        sentence = []
        labels = []

    return data

def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """pretty print for confusion matrixes"""
    columnwidth = max([len(x) for x in labels]+[10]) # 5 is value length
    empty_cell = " " * columnwidth
    # Print header
    print( empty_cell + " t/p " , end='')
    for label in labels: 
        print("%{0}s".format(columnwidth) % label, end='')
    print()
    # Print rows
    for i, label1 in enumerate(labels):
        print("     %{0}s".format(columnwidth) % label1, end='')
        for j in range(len(labels)): 
            cell = "%{0}.1f".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end='')
        print()

parser = argparse.ArgumentParser()

parser.add_argument("--ref", default=None, type=str, required=True)
parser.add_argument("--pred", default=None, type=str, required=True)

args = parser.parse_args()

reference = readfile(args.ref)
prediction = readfile(args.pred)

y_true = []
y_pred = []

for (ref_sent, ref_labels), (_, pred_labels) in zip(reference, prediction):
    if len(ref_labels) != len(pred_labels):
        print(ref_sent)
        print(ref_labels)
        print(pred_labels)
        print()
    elif not '?' in ref_labels:
        y_true.extend(ref_labels)
        y_pred.extend(pred_labels)
    else:
        pass # print(ref_labels)
    #assert len(ref_labels) == len(pred_labels)

labels = ["B-ENG","I-ENG", "B-OTHER", "I-OTHER", "O"]

#print_cm(skl.confusion_matrix(y_true, y_pred), labels)

print()

#print(skl.classification_report(y_true, y_pred, digits=4, labels=labels))

print()

assert len(y_true) == len(y_pred), "problem"
    
#print(sqe.classification_report(y_true, y_pred, digits=4, scheme=IOB2))
print(sqe.classification_report([y_true], [y_pred], digits=4, scheme=IOB2))
