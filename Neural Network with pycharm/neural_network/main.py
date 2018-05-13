import definitions
import numpy as np
import copy as cp
from logistic_func import getF


def getDataSet( pathToFileFromProjectRoot ):
    pathToFile = definitions.ROOT_DIR + "/" + pathToFileFromProjectRoot
    openedFile = open(pathToFile, "rb")

    loadedText = np.loadtxt(openedFile, skiprows=0, dtype=str)
    floatDataSet = loadedText.astype(np.float)
    return floatDataSet

def getXY( dataSet, featureCnt, outputVecSize ):
    # print(dataSet)
    exampleCnt = dataSet.shape[0]

    X =  dataSet[:, 0:featureCnt ]
    Y = dataSet[:,-1]

    yVec = np.zeros( (exampleCnt, outputVecSize) )
    for i in range(exampleCnt):
        colToMake1 = int(Y[i])-1
        yVec[ i, colToMake1 ] = 1

    Y = yVec

    ret = {}
    ret['X'] = X
    ret['Y'] = Y

    return ret;


def getNN(xTrain, yTrain, neuronCntList, learningRate, totalRound):

    layerCnt = len( neuronCntList )
    print(layerCnt)


    assert neuronCntList[0]==xTrain.shape[1]
    featureCnt = neuronCntList[0]

    assert neuronCntList[-1]==yTrain.shape[1]
    outputVectorSize = neuronCntList[-1]

    assert xTrain.shape[0]==yTrain.shape[0]
    exampleCnt = xTrain.shape[0]

    wAr = getW(neuronCntList, np.random.random)
    print(wAr)

    for roundIdx in range(totalRound):
        errorInThisRound = 0.0

        delW = getW(neuronCntList=neuronCntList, arrayGettingMethod=np.zeros)
        print( delW )

        for exampleIdx in range(exampleCnt):
            curX = xTrain[exampleIdx,:]
            curY = yTrain[exampleIdx,:]

            vAr = getZigzagged2dArray(neuronCntList, np.zeros)
            yAr = getZigzagged2dArray(neuronCntList, np.zeros)

            yAr[0] = curX
            print(" yAr[0] ")
            print(yAr[0])


            forwardProp(wAr=wAr, yAr=yAr, vAr=vAr)
            estimatedY = yAr[ -1 ]

            errorForThisExample = distSq(estimatedY, curY)
            errorInThisRound += errorForThisExample


        print("roundIdx")
        print(roundIdx)

        print("errorInThisRound")
        print(errorInThisRound)






def getW(neuronCntList, arrayGettingMethod):

    w = []
    w.append(None)  # first layer is input layer
                    # So no weight vector is defined for that
    for i in range(1, len(neuronCntList) ):
        prevLayerNeuronCnt = neuronCntList[i - 1]
        curLayerNeuronCnt = neuronCntList[i]

        wr = arrayGettingMethod((curLayerNeuronCnt, prevLayerNeuronCnt+1))
        w.append(wr)

    return w


def getZigzagged2dArray( columnCntList, arrayGettingMethod ):
    za = []
    for i in columnCntList:
        addee = arrayGettingMethod(i)
        za.append(addee)
    return za



def forwardProp(wAr, yAr, vAr):
    layerCnt =  len(wAr)
    for layerIdx in range(1, layerCnt):
        print("layerIdx")
        print(layerIdx)

        curLayerW = wAr[layerIdx]
        print("curLayerW")
        print(curLayerW)

        prevYWithBias = np.append(1, yAr[layerIdx - 1])
        print("prevYWithBias")
        print(prevYWithBias)

        vAr[layerIdx] = np.dot(curLayerW, prevYWithBias)
        print("vAr[layerIdx]")
        print(vAr[layerIdx])

        yAr[layerIdx] = getF(x=vAr[layerIdx])

        print("yAr[layerIdx]")
        print(yAr[layerIdx])


def distSq(x, y):
    assert x.shape == y.shape
    return np.sum((x-y)**2)


pathToDataFileFromProjectRoot = "data1/data.txt";
dataSet = getDataSet(pathToFileFromProjectRoot=pathToDataFileFromProjectRoot)
ret = getXY(dataSet=dataSet, featureCnt=2, outputVecSize=2)

X = ret['X']
Y = ret['Y']

assert X.shape[0] == Y.shape[0] # Both X and Y should contain same number of examples
exampleCnt = X.shape[0]


# bias = np.ones( (exampleCnt, 1) )
# X = np.append(bias, X, axis=1)

print(X)
print(Y)

featureCnt = X.shape[1]
outputVecSize = Y.shape[1]


neuronCntList=[featureCnt, 5, 4, outputVecSize]
learningRate = 0.1
roundCnt = 1
getNN(xTrain=X, yTrain=Y, neuronCntList=neuronCntList, learningRate=learningRate,
      totalRound=roundCnt)