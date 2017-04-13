from sklearn.metrics import confusion_matrix
import gzip
import matplotlib.pyplot as plt
import numpy as np
import itertools


#comment out this block for testing:
readin = []
with open("test",'r') as file:
    for l in file:
        ls = eval(l)
        readin.append(ls)
    file.close()

#pair_list contains pairs of pred and true
pair_list = []
for i in range(0,8,2):
    pair_list.append([readin[i],readin[i+1]])
features=['c1', 'c2', 'c3', 'c4']
sport_types=['run','bike','bike (transport)','mountain bike']

'''
#test
readin = [[[1,2,2,4,3,3,4,4,5,4,7,6,7,8],[1,2,4,5,3,3,4,4,5,6,7,7,7,8]]];
pair_list=readin
features=['feature1']
sport_types=[1,2,3,4,5,6,7,8];
'''

#vertical -> true, horizontal -> predict
#cm->confusion matrix
#classes-> spt names
def plot_confusion_matrix(cm, classes, normalize=False,title='Confusion matrix',cmap=plt.cm.jet):

    #display image
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    #vertical color bar
    plt.colorbar()

    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    print('Confusion matrix')
    print(cm)

    #adjust the number shown in the grid
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],horizontalalignment="center",color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

for pair in pair_list:
    y_true = pair[0]
    y_pred = pair[1]
    matrix = confusion_matrix(y_true, y_pred, labels=sport_types)
    plt.figure()
    plot_confusion_matrix(matrix, classes=sport_types,title='Confusion matrix',cmap=plt.cm.jet)
    plt.show()


