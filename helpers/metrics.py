def classification_accuracy(predictions, labels):
    scores = [0] * 4
    #[TP, TN, FP, FN]
    for i, prediction in enumerate(predictions):
        if int(labels[i]) == 1:
            if int(prediction) == int(labels[i]):
                scores[0] += 1
            else:
                scores[3] += 1
        else:
            if int(prediction) == int(labels[i]):
                scores[1] += 1
            else:
                scores[2] += 1
    #print(scores)
    try:
        pre = float(scores[0]) / float((scores[0] + scores[2]))
        rec = float(scores[0]) / float((scores[0] + scores[3]))
        f_measure = float(2 * pre * rec) / float(pre + rec)
    except ZeroDivisionError:
        f_measure = 0
    return f_measure