import matplotlib.pyplot as plt
import itertools
import numpy as np


def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion Matix', cmap=plt.cm.Blues, bg='#DFEBE9'):

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    #plt.set_facecolor('#DFEBE9')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:,np.newaxis]
        print("Normalized Confusion Matrix")
    else:
        print("Confusion Matrix")

    print(cm)

    thresh = cm.max()/2
    for i,j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j,i,cm[i,j],
                horizontalalignment="center",
                color="white" if cm[i,j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig('../Resultado.png')
    #plt.show()