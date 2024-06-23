from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_curve,
    matthews_corrcoef,
)
import matplotlib.pyplot as plt
import pickle
from pprint import pprint


def get_answer_pred(resultsList):
    y_true = []
    y_pred = []
    for result in resultsList:
        y_true.append(result[1])
        y_pred.append(result[0])
    return y_true, y_pred


def get_metrics(results):
    metrics = {}

    for key, value in results.items():
        metrics[key] = {}

        y_true, y_pred = get_answer_pred(value)

        metrics[key]["accuracy"] = accuracy_score(y_true, y_pred)
        metrics[key]["precision"] = precision_score(y_true, y_pred)
        metrics[key]["recall"] = recall_score(y_true, y_pred)
        metrics[key]["f1"] = f1_score(y_true, y_pred)
        metrics[key]["confusion"] = confusion_matrix(y_true, y_pred)
        metrics[key]["mcc"] = matthews_corrcoef(y_true, y_pred)
        fpr, tpr, _ = roc_curve(y_true, y_pred)
        metrics[key]["fpr"] = fpr
        metrics[key]["tpr"] = tpr

    return metrics


def plot_roc_curve(fpr, tpr):
    plt.plot(fpr, tpr, marker=".", label="ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.show()


def plot_confusion_matrix(confusion):
    plt.imshow(confusion, cmap="binary", interpolation="None")
    plt.show()


def plot_metrics(metrics):
    for key in metrics:
        print(key)
        print("Accuracy:", metrics[key]["accuracy"])
        print("Precision:", metrics[key]["precision"])
        print("Recall:", metrics[key]["recall"])
        print("F1:", metrics[key]["f1"])
        print("MCC:", metrics[key]["mcc"])
        print("Confusion matrix:")
        print(metrics[key]["confusion"])
        print("\n")

        fpr = metrics[key]["fpr"]
        tpr = metrics[key]["tpr"]
        plot_roc_curve(fpr, tpr)
        plot_confusion_matrix(metrics[key]["confusion"])


def get_best_pair_accuracy(metrics):
    best_pair = None
    best_accuracy = 0
    for key in metrics:
        if metrics[key]["accuracy"] > best_accuracy:
            best_accuracy = metrics[key]["accuracy"]
            best_pair = key
    return best_pair, best_accuracy


def get_min_shots_accuracy(metrics, threshold=0.8):
    max_accuracy = 0
    min_shots = None
    keys = metrics.keys()
    keys = sorted(keys, key=lambda x: (x[0], x[1]))
    for key in keys:
        if metrics[key]["accuracy"] >= threshold:
            min_shots = key
            max_accuracy = metrics[key]["accuracy"]
            break
    return min_shots, max_accuracy


# See for each context the first accuracy that is bigger than a threshold
def get_min_context_accuracy(metrics, threshold=0.8):
    max_accuracy = 0
    min_context = None
    keys = metrics.keys()
    keys = sorted(keys, key=lambda x: (x[1], x[0]))
    for key in keys:
        if metrics[key]["accuracy"] >= threshold:
            min_context = key
            max_accuracy = metrics[key]["accuracy"]
            break
    return min_context, max_accuracy


if __name__ == "__main__":
    results = pickle.load(open("predictions.pkl", "rb"))
    # Convert every value in results to int
    for key in results:
        results[key] = [(int(result[0]), int(result[1])) for result in results[key]]

    metrics = get_metrics(results)
    plot_metrics(metrics)

    best_pair, best_accuracy = get_best_pair_accuracy(metrics)
    print(f"Best pair: {best_pair}, Accuracy: {best_accuracy}")
    min_shots, max_accuracy = get_min_shots_accuracy(metrics)
    print(f"Min shots: {min_shots}, Accuracy: {max_accuracy}")
    min_context, max_accuracy = get_min_context_accuracy(metrics)
    print(f"Min context: {min_context}, Accuracy: {max_accuracy}")
