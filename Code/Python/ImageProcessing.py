'''
Summary
Library of Image Processing Functions made by ME
'''

# Imports
import random
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import json
import imutils
import math

# Matrix / Image Creation
def CreateMatrix_UserInput(matrixSize):
    ''' Creates a matrix with user input '''
    matrix = []

    for i in range(matrixSize[0]):
        row = []
        for j in range(matrixSize[1]):
            row.append(int(input("Enter value at (" + str(i) + ", " + str(j) + "): ")))
        matrix.append(row)
    
    return matrix

def CreateMatrix_RandomInput(matrixSize, ValRange):
    ''' Creates a matrix with random input '''
    matrix = []

    for i in range(matrixSize[0]):
        row = []
        for j in range(matrixSize[1]):
            row.append(random.randint(ValRange[0], ValRange[1]))
        matrix.append(row)
    
    return matrix

# Image Matrix Operations
def MatSum(matrix):
    sum = 0

    for row in matrix:
        for val in row:
            sum += val
    
    return sum

def MatMax(matrix):
    max = 0

    for row in matrix:
        for val in row:
            if max < val:
                max = val
    
    return max

def MatFreqDist(matrix):
    freq = {}

    for row in matrix:
        for val in row:
            freq[val] = 0

    for row in matrix:
        for val in row:
            freq[val] += 1

    return freq

def MatMean(matrix):
    sum = 0
    for row in matrix:
        for val in row:
            sum += val
    return sum / (len(matrix) * len(matrix[0]))

def MatMedian(matrix):
    arr = []
    for row in matrix:
        for val in row:
            arr.append(val)
    # Bubble Sort Code
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

    if len(arr) % 2 == 1:
        return arr[int((len(arr) - 1)/2)]
    else:
        return (arr[int(len(arr)/2)] + arr[int(len(arr)/2 - 1)]) / 2

def MatMode(matrix):
    modeVal = -1
    modeVal_freq = -1

    freq = MatFreqDist(matrix)

    for key in freq.keys():
        if freq[key] > modeVal_freq:
            modeVal = key
            modeVal_freq = freq[key]

    return modeVal

def MatStandardDeviation(matrix):
    SD = 0.0

    mean = MatMean(matrix)
    sumsqaurediff = 0.0
    for row in matrix:
        for val in row:
            sumsqaurediff += (val - mean) ** 2
    SD = (sumsqaurediff / (len(matrix) * len(matrix[0]))) ** (1/2)

    return SD

def GetFreqDist(Image, pixelRange=(0, 255)):
    Freq = []
    for i in range(pixelRange[0], pixelRange[1]+1):
        Freq.append(0)
    for row in tqdm(Image):
        for pixel in row:
            Freq[pixel - pixelRange[0]] += 1
    return Freq

def GetCumulativeDist(Dist):
    CumulativeDist = []
    cumulativeVal = 0.0
    for d in Dist:
        cumulativeVal += d
        CumulativeDist.append(cumulativeVal)
    return np.array(CumulativeDist)

def HistPlot(Data, nbins=25):
    X = np.arange(len(Data))
    n, bins, patches = plt.hist(Data, nbins, facecolor='blue', alpha=0.5)
    #plt.show()

def ceil(a):
    if (a-float(int(a))) > 0:
        return a + 1
    return a

# Image Conversion
def rgb2gray(I):
    I = I.astype(int)
    r, g, b = I[:,:,0], I[:,:,1], I[:,:,2]
    #gray = (0.2989 * r + 0.5870 * g + 0.1140 * b)
    gray = (1 * r + 1 * g + 1 * b) / 3
    return gray.astype(np.uint8)

# Image Noise Addition
def SaltPepperNoise(I, prob):
    max = 255
    I_g = I.copy()
    probpercent = int(prob*100)
    # Greyscale
    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1], 1))
    for i in range(I_g.shape[0]):
        for j in range(I_g.shape[1]):
            r = random.randrange(1, 100)
            #r = random.randint(1, 100)
            if r <= probpercent:
                if r <= int(probpercent / 2):
                    I_g[i, j, :] = np.ones(I_g.shape[2]) * max # Salt
                else:
                    I_g[i, j] = np.ones(I_g.shape[2]) * 0 # Pepper
    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1]))
    I_g = I_g.astype(np.uint8)
    return I_g

def GaussianNoise(I, mean, variance):
    I_g = I.astype(int).copy()

    SD = variance ** 0.5

    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1], 1))

    rows, pixs, channels = I_g.shape
    noise = np.random.normal(mean, SD, (rows, pixs, channels))
    noise = noise.reshape(rows, pixs, channels)
    I_g = np.add(I_g, noise.astype(int))

    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1]))

    I_g = I_g.astype(np.uint8)
    return I_g

def SpeckleNoise(I):
    I_g = I.astype(int).copy()

    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1], 1))

    rows, pixs, channels = I_g.shape
    noise = np.random.randn(rows, pixs, channels)
    noise = noise.reshape(rows, pixs, channels)
    I_g = np.add(I_g, np.multiply(I_g, noise).astype(int))

    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1]))

    I_g = I_g.astype(np.uint8)
    return I_g

# Image Operations
def ImgAverage(Is):
    AvgI = Is[0].copy().astype(int)
    for imgindex in range(len(Is)):
        if imgindex != 0:
            Is[imgindex] = Is[imgindex].astype(int)
            AvgI = np.add(AvgI, Is[imgindex])
    AvgI = np.divide(AvgI, len(Is)).astype(int)
    AvgI = AvgI.astype(np.uint8)
    return AvgI

def BillinearInterpolation_Scaling(Image, Scale=(2, 2)):
    NewSize = (int(round(Image.shape[0]*Scale[0])), int(round(Image.shape[1]*Scale[1])))
    ScaledImg = np.ones(NewSize) * -1

    for i in range(Image.shape[0]):
        for j in range(Image.shape[1]):
            if int(i % (1/Scale[0])) == 0 and int(j % Scale[1]) == 0:
                ScaledImg[int(i*Scale[0]), int(j*Scale[1])] = Image[i, j]

    # Fill Missing Spots
    for i in tqdm(range(NewSize[0])):
        for j in range(NewSize[1]):
            if ScaledImg[i, j] == -1:
                InvCo = (i/Scale[0], j/Scale[1])
                A1 = (InvCo[0] - int(InvCo[0]))*(InvCo[1] - int(InvCo[1]))
                A2 = (1 - (InvCo[0] - int(InvCo[0])))*(InvCo[1] - int(InvCo[1]))
                A3 = (InvCo[0] - int(InvCo[0]))*(1 - (InvCo[1] - int(InvCo[1])))
                A4 = (1 - (InvCo[0] - int(InvCo[0])))*(1 - (InvCo[1] - int(InvCo[1])))
                A = A4
                if int(InvCo[0]) + 1 < Image.shape[0] and int(InvCo[1]) + 1 < Image.shape[1]:
                    A += A1 + A2 + A3
                elif int(InvCo[0]) + 1 < Image.shape[0]:
                    A += A3
                elif int(InvCo[1]) + 1 < Image.shape[1]:
                    A += A2
                

                ScaledImg[i, j] = (A4*Image[int(InvCo[0]), int(InvCo[1])])/A
                if int(InvCo[0]) + 1 < Image.shape[0] and int(InvCo[1]) + 1 < Image.shape[1]:
                    ScaledImg[i, j] += (A1*Image[int(InvCo[0]) + 1, int(InvCo[1]) + 1])/A
                    ScaledImg[i, j] += (A3*Image[int(InvCo[0]) + 1, int(InvCo[1])])/A
                    ScaledImg[i, j] += (A2*Image[int(InvCo[0]), int(InvCo[1]) + 1])/A
                elif int(InvCo[0]) + 1 < Image.shape[0]:
                    ScaledImg[i, j] += (A3*Image[int(InvCo[0]) + 1, int(InvCo[1])])/A
                elif int(InvCo[1]) + 1 < Image.shape[1]:
                    ScaledImg[i, j] += (A2*Image[int(InvCo[0]), int(InvCo[1]) + 1])/A

    return ScaledImg

def BillinearInterpolation_Rotation(Image, Angle=0.0):
    anglerad = -Angle * math.pi / 180.0
    NewSize = (Image.shape[0], Image.shape[1])
    RotImg = np.ones(NewSize) * -1

    for i in range(Image.shape[0]):
        for j in range(Image.shape[1]):
            newi = math.cos(anglerad)*i + math.sin(anglerad)*j
            newj = -1*math.sin(anglerad)*i + math.cos(anglerad)*j
            if (newi-float(int(newi))) == 0.0 and (newj-float(int(newj))) == 0.0:
                RotImg[int(newi), int(newj)] = Image[i, j]

    # Fill Missing Spots
    for i in tqdm(range(NewSize[0])):
        for j in range(NewSize[1]):
            if RotImg[i, j] == -1:
                InvCo = [math.cos(anglerad)*i - math.sin(anglerad)*j, math.sin(anglerad)*i + math.cos(anglerad)*j]
                A1 = (InvCo[0] - int(InvCo[0]))*(InvCo[1] - int(InvCo[1]))
                A2 = (1 - (InvCo[0] - int(InvCo[0])))*(InvCo[1] - int(InvCo[1]))
                A3 = (InvCo[0] - int(InvCo[0]))*(1 - (InvCo[1] - int(InvCo[1])))
                A4 = (1 - (InvCo[0] - int(InvCo[0])))*(1 - (InvCo[1] - int(InvCo[1])))
                A = A4
                if int(InvCo[0]) + 1 < Image.shape[0] and int(InvCo[1]) + 1 < Image.shape[1]:
                    A += A1 + A2 + A3
                elif int(InvCo[0]) + 1 < Image.shape[0]:
                    A += A3
                elif int(InvCo[1]) + 1 < Image.shape[1]:
                    A += A2
                
                if int(InvCo[0]) < Image.shape[0] and int(InvCo[1]) < Image.shape[1]:
                    RotImg[i, j] = (A4*Image[int(InvCo[0]), int(InvCo[1])])/A
                    if int(InvCo[0]) + 1 < Image.shape[0] and int(InvCo[1]) + 1 < Image.shape[1]:
                        RotImg[i, j] += (A1*Image[int(InvCo[0]) + 1, int(InvCo[1]) + 1])/A
                        RotImg[i, j] += (A3*Image[int(InvCo[0]) + 1, int(InvCo[1])])/A
                        RotImg[i, j] += (A2*Image[int(InvCo[0]), int(InvCo[1]) + 1])/A
                    elif int(InvCo[0]) + 1 < Image.shape[0]:
                        RotImg[i, j] += (A3*Image[int(InvCo[0]) + 1, int(InvCo[1])])/A
                    elif int(InvCo[1]) + 1 < Image.shape[1]:
                        RotImg[i, j] += (A2*Image[int(InvCo[0]), int(InvCo[1]) + 1])/A

    return RotImg

def RotateImage(Image, angle, cropBoundary=False):
    RotatedImage = None
    if cropBoundary:
        RotatedImage = imutils.rotate(Image, angle)
    else:
        RotatedImage = imutils.rotate_bound(Image, angle)
    return RotatedImage

# Image Transformation
def ImagePixelReplace(Image, pixelReplaceVals):
    I = np.zeros(Image.shape)
    for i in tqdm(range(Image.shape[0])):
        for j in range(Image.shape[1]):
            I[i, j] = pixelReplaceVals[Image[i, j]]
    return I

def NormaliseToRange(I, Range=(0, 255)):
    I_g = I.copy()
    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1], 1))
    
    maxVal = np.max(np.max(I_g, axis=1), axis=0)
    minVal = np.min(np.min(I_g, axis=1), axis=0)

    minmaxRange = maxVal - minVal

    for i in range(I_g.shape[0]):
        for j in range(I_g.shape[1]):
            for c in range(I_g.shape[2]):
                I_g[i, j, c] = (((I_g[i, j, c] - minVal[c]) / minmaxRange) * (Range[1] - Range[0])) + Range[0]

    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1]))

    return I_g

def HistogramMatching(I_input, I_ref, pixelRange=(0, 255)):
    HistVals_input, HistProbDist_input, Hist2PixVals_input = HistogramEqualisation(I_input)
    HistVals_ref, HistProbDist_ref, Hist2PixVals_ref = HistogramEqualisation(I_ref)

    ProcessedDist = []
    noMapCheck = True
    for hv in tqdm(HistVals_input):
        if len(Hist2PixVals_ref[hv - pixelRange[0]]) > 0:
            randindex = random.randint(0, len(Hist2PixVals_ref[hv - pixelRange[0]])-1)
            ProcessedDist.append(Hist2PixVals_ref[hv - pixelRange[0]][randindex])
            noMapCheck = False
        else:
            ProcessedDist.append(-1)
            # if len(ProcessedDist) > 0:
            #     ProcessedDist.append(ProcessedDist[-1])
            # else:
            #     ProcessedDist.append(ProcessedDist[-1])
    
    if not noMapCheck:
        while (-1 in ProcessedDist):
            if ProcessedDist[0] == -1:
                ProcessedDist[0] = ProcessedDist[1]
            if ProcessedDist[-1] == -1:
                ProcessedDist[-1] = ProcessedDist[-2]
            
            for pdi in range(1, len(ProcessedDist)-1):
                if ProcessedDist[pdi] == -1:
                    if ProcessedDist[pdi-1] != -1 and ProcessedDist[pdi+1] != -1:
                        ProcessedDist[pdi] = int(round((ProcessedDist[pdi-1] + ProcessedDist[pdi+1]) / 2))
                    elif ProcessedDist[pdi-1] == -1 and ProcessedDist[pdi+1] != -1:
                        ProcessedDist[pdi] = ProcessedDist[pdi+1]
                    elif ProcessedDist[pdi-1] != -1 and ProcessedDist[pdi+1] == -1:
                        ProcessedDist[pdi] = ProcessedDist[pdi-1]

        ProbDist_input = np.array(GetFreqDist(I_input, pixelRange)) / (I_input.shape[0]*I_input.shape[1])
        ProbDist_processed = []
        for i in range(len(ProcessedDist)):
            ProbDist_processed.append(0.0)
        for pi in range(ProbDist_input.shape[0]):
            ProbDist_processed[ProcessedDist[pi] - pixelRange[0]] += ProbDist_input
        ProbDist_processed = np.array(ProbDist_processed)

        return ProcessedDist, ProbDist_processed
        
    print("No Mapping Exists for Reference to Input Image")
    return None

def HistogramEqualisation(Image, pixelRange=(0, 255)):
    FreqDist = np.array(GetFreqDist(Image, pixelRange))
    TotPixels = Image.shape[0]*Image.shape[1]

    ProbDist = (FreqDist / TotPixels)

    CumulativeProbDist = GetCumulativeDist(ProbDist)

    HistVals = np.round(CumulativeProbDist * (pixelRange[1] - pixelRange[0])).astype(int)

    HistProbDist = []
    Hist2PixVals = []
    for i in range(pixelRange[0], pixelRange[1]+1):
        HistProbDist.append(0.0)
        Hist2PixVals.append([])
    for hvi in range(HistVals.shape[0]):
        HistProbDist[HistVals[hvi] - pixelRange[0]] += ProbDist[hvi]
        Hist2PixVals[HistVals[hvi] - pixelRange[0]].append(hvi + pixelRange[0])
    HistProbDist = np.array(HistProbDist)

    return HistVals, HistProbDist, Hist2PixVals

def CrossCorrelation(I, W, stride=(1, 1), mean_mode='full'):
    I2 = I.copy()
    W = W.copy()
    if I.ndim == 2:
        I2 = np.reshape(I2, (I2.shape[0], I2.shape[1], 1))
        W = np.reshape(W, (W.shape[0], W.shape[1], 1))

    padSize = (I2.shape[0] + 2*(W.shape[0]-1), I2.shape[1] + 2*(W.shape[1]-1), I2.shape[2])
    I_padded = np.zeros(padSize)
    I_padded[W.shape[0]-1:-W.shape[0]+1, W.shape[1]-1:-W.shape[1]+1, :] = I2[:, :, :]

    outSize = (int((I2.shape[0] + W.shape[0])/stride[0]), int((I2.shape[1] + W.shape[1])/stride[1]), I2.shape[2])
    I_g = np.zeros(outSize)

    I_bar = None
    SDProd = np.ones(I2.shape[2])
    W_bar = np.sum(np.sum(W, axis=1), axis=0) / (W.shape[0]*W.shape[1])
    if mean_mode == 'full':
        I_bar = np.sum(np.sum(I2, axis=1), axis=0) / (I2.shape[0]*I2.shape[1])
        for c in range(I2.shape[2]):
            SDProd[c] = np.sum(np.sum((I2[:, :, c] - I_bar)**2, axis=1), axis=0) ** (1/2)
            SDProd[c] *= np.sum(np.sum((W[:, :, c] - W_bar)**2, axis=1), axis=0) ** (1/2)
            #SDProd[c] = np.std(I2[:, :, c].flatten()) * np.std(W[:, :, c].flatten())

    for i in tqdm(range(0, I_padded.shape[0]-W.shape[0]+1, stride[0])):
        for j in range(0, I_padded.shape[1]-W.shape[1]+1, stride[1]):
            if mean_mode == 'window':
                I_bar = np.sum(np.sum(I_padded[i:i+W.shape[0], j:j+W.shape[1], :], axis=1), axis=0) / (W.shape[0]*W.shape[1])
            for c in range(I_padded.shape[2]):
                if mean_mode == 'window':
                    SDProd[c] = np.sum(np.sum((I_padded[i:i+W.shape[0], j:j+W.shape[1], c] - I_bar)**2, axis=1), axis=0) ** (1/2)
                    SDProd[c] *= np.sum(np.sum((W[:, :, c] - W_bar)**2, axis=1), axis=0) ** (1/2)
                    #SDProd[c] = np.std(I_padded[i:i+W.shape[0], j:j+W.shape[1], c].flatten()) * np.std(W[:, :, c].flatten())
                I_val = I_padded[i:i+W.shape[0], j:j+W.shape[1], c] - I_bar[c]
                W_val = W[:, :, c] - W_bar[c]
                I_g[i, j, c] = np.sum(np.sum(np.multiply(I_val, W_val), axis=1), axis=0) / SDProd[c]
            
    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1]))
        I_padded = np.reshape(I_padded, (I_padded.shape[0], I_padded.shape[1]))
        W = np.reshape(W, (W.shape[0], W.shape[1]))
    return I_g, I_padded

def Correlation(I, W, stride=(1, 1)):
    I2 = I.copy()
    W = W.copy()
    if I.ndim == 2:
        I2 = np.reshape(I2, (I2.shape[0], I2.shape[1], 1))
        W = np.reshape(W, (W.shape[0], W.shape[1], 1))

    padSize = (I2.shape[0] + 2*(W.shape[0]-1), I2.shape[1] + 2*(W.shape[1]-1), I2.shape[2])
    I_padded = np.zeros(padSize)
    I_padded[W.shape[0]-1:-W.shape[0]+1, W.shape[1]-1:-W.shape[1]+1, :] = I2[:, :, :]

    outSize = (int((I2.shape[0] + W.shape[0])/stride[0]), int((I2.shape[1] + W.shape[1])/stride[1]), I2.shape[2])
    I_g = np.zeros(outSize)

    for i in tqdm(range(0, I_padded.shape[0]-W.shape[0]+1, stride[0])):
        for j in range(0, I_padded.shape[1]-W.shape[1]+1, stride[1]):
            for c in range(I_padded.shape[2]):
                I_g[i, j, c] = np.sum(np.sum(np.multiply(I_padded[i:i+W.shape[0], j:j+W.shape[1], c], W[:, :, c]), axis=1), axis=0)
            
    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1]))
        I_padded = np.reshape(I_padded, (I_padded.shape[0], I_padded.shape[1]))
        W = np.reshape(W, (W.shape[0], W.shape[1]))
    return I_g, I_padded

def ApplyMedianFilter(I, WSize=(3, 3), stride=(1, 1)):
    I2 = I.copy()
    if I.ndim == 2:
        I2 = np.reshape(I2, (I2.shape[0], I2.shape[1], 1))

    padSize = (I2.shape[0] + 2*(WSize[0]-1), I2.shape[1] + 2*(WSize[1]-1), I2.shape[2])
    I_padded = np.zeros(padSize)
    I_padded[WSize[0]-1:-WSize[0]+1, WSize[1]-1:-WSize[1]+1, :] = I2[:, :, :]

    outSize = (int((I2.shape[0] + WSize[0])/stride[0]), int((I2.shape[1] + WSize[1])/stride[1]), I2.shape[2])
    I_g = np.zeros(outSize)

    for i in tqdm(range(0, I_padded.shape[0]-WSize[0]+1, stride[0])):
        for j in range(0, I_padded.shape[1]-WSize[1]+1, stride[1]):
            for c in range(I_padded.shape[2]):
                I_g[i, j, c] = np.median(I_padded[i:i+WSize[0], j:j+WSize[1], c])
            
    if I.ndim == 2:
        I_g = np.reshape(I_g, (I_g.shape[0], I_g.shape[1]))
    I_g = np.round(I_g).astype(np.uint8)
    return I_g

# Image Filters
def GenerateEdgeFilter(size=(3, 3)):
    if size[0]%2 == 0 or size[1] == 0:
        return None
    W = np.ones(size) * -1
    W[int(size[0]/2), int(size[1]/2)] = -(size[0]*size[1] - 1)
    return W

def GenerateAverageFilter(size=(3, 3)):
    return np.ones(size).astype(float) / (size[0]*size[1])

# Image Augmentation
def BoundingBox(Image, pos, window_size, radius=1, color=[0, 0, 0]):
    I = Image.copy()
    window_size = [window_size[0], window_size[1]]
    for wi in range(len(window_size)):
        if pos[wi] + window_size[wi] > Image.shape[wi]:
            window_size[wi] = Image.shape[wi] - pos[wi]
    
    if I.ndim == 2:
        for i in [pos[0], pos[0] + window_size[0]]:
            for p in range(pos[1], pos[1] + window_size[1]):
                I[i, p] = color[0]
                #print("Markx:", i, p, color[0])
        for j in [pos[1], pos[1] + window_size[1]]:
            for p in range(pos[0], pos[0] + window_size[0]):
                I[p, j] = color[0]
                #print("Marky:", p, j, color[0])
    elif I.ndim == 3:
        for i in [pos[0], pos[0] + window_size[0]]:
            for p in range(pos[1], pos[1] + window_size[1]):
                I[i, p, :] = color[:I.shape[2]]
        for j in [pos[1], pos[1] + window_size[1]]:
            for p in range(pos[0], pos[0] + window_size[0]):
                I[p, j, :] = color[:I.shape[2]]

    for ri in range(1, radius+1):
        I = BoundingBox(I, [pos[0]+ri, pos[1]+ri], [window_size[0]-(2*ri), window_size[1]-(2*ri)], radius=0, color=color)
    return I

# Image Database Functions
class ImageDetails:
    def __init__(self, path, GMatchVal, CMatchVal):
        self.path = path
        self.GMatchVal = GMatchVal
        self.CMatchVal = CMatchVal

def RefreshDatabase(DatabaseLocations=['FillImgs'], G_JSON='FillImgs_G.json', C_JSON='FillImgs_C.json', match_mode='avg', roundRange=10):
    global Images
    Images = []
    #DatabaseLocationProgress = 1
    #TotalLocs = len(DatabaseLocations)
    print("Refreshing File List...")
    for DatabaseLocation in tqdm(DatabaseLocations):
        for dirpath, dirnames, filenames in os.walk(DatabaseLocation):
            for filename in filenames:
                imgd = ImageDetails(os.path.join(dirpath, filename), 0.0, [0.0, 0.0, 0.0])
                Images.append(imgd)
        #print("Hashed", DatabaseLocation, ":", DatabaseLocationProgress, "/", TotalLocs)
        #DatabaseLocationProgress += 1
    UpdateImagesMatchVals(match_mode)
    print("Image Values Updated")
    G_Dict = GenerateGreyScaleDict(roundRange)
    print("GrayScale JSON Dictionary Generated")
    C_Dict = GenerateColorDict(roundRange)
    print("Color JSON Dictionary Generated")
    #print(G_Dict)
    #print(C_Dict)
    UpdateJSONFiles(G_Dict, C_Dict, G_JSON, C_JSON)
    print("JSON Files Updated")

def UpdateImagesMatchVals(match_mode='avg'):
    global Images
    print("Updating Image Match Vals...")
    for i in tqdm(range(len(Images))):
        if match_mode == 'avg':
            I = cv2.imread(Images[i].path)
            I_g = cv2.imread(Images[i].path, 0)
            Images[i].GMatchVal = np.sum(np.sum(I_g, axis=1), axis=0) / (I_g.shape[0]*I_g.shape[1])
            Images[i].CMatchVal = np.sum(np.sum(I, axis=1), axis=0) / (I.shape[0]*I.shape[1])
        elif match_mode == 'name': # Name is of form Type_SubDirName_000_000_000.png for color
            filename = os.path.splitext(os.path.basename(Images[i].path))[0]
            Images[i].CMatchVal = list(map(int, filename[-11:].split('_'))) 
            Images[i].GMatchVal = int(0.2989 * Images[i].CMatchVal[0] + 0.5870 * Images[i].CMatchVal[1] + 0.1140 * Images[i].CMatchVal[2])
    
def GenerateGreyScaleDict(roundRange=200):
    global Images
    G_Dict = {}
    G_Dict['roundrange'] = roundRange
    for i in range(0, 261, roundRange):
        G_Dict[str(i)] = []
    for img in Images:
        ValClass = str(int(round(img.GMatchVal / roundRange)*roundRange))
        G_Dict[ValClass].append(img.path)
    return G_Dict

def GenerateColorDict(roundRange=200):
    global Images
    C_Dict = {}
    C_Dict['roundrange'] = roundRange
    for r in range(0, 261, roundRange):
        for g in range(0, 261, roundRange):
            for b in range(0, 261, roundRange):
                C_Dict[str(r) + '_' + str(g) + '_' + str(b)] = []
    for img in Images:
        ValClass = str(int(round(img.CMatchVal[0] / roundRange)*roundRange)) + '_' + str(int(round(img.CMatchVal[1] / roundRange)*roundRange)) + '_' + str(int(round(img.CMatchVal[2] / roundRange)*roundRange))
        C_Dict[ValClass].append(img.path)
    return C_Dict

def UpdateJSONFiles(G_Dict, C_Dict, G_JSON='FillImgs_G.json', C_JSON='FillImgs_C.json'):
    if G_Dict is not None:
        with open(G_JSON, 'w') as fg:
            json.dump(G_Dict, fg)
    if C_Dict is not None:
        with open(C_JSON, 'w') as fc:
            json.dump(C_Dict, fc)

def AddImagesToDatabase(paths, match_mode='avg', G_JSON='FillImgs_G.json', C_JSON='FillImgs_C.json'):
    global Images

    G_Dict = {}
    with open(G_JSON) as fgr:
        G_Dict = json.load(fgr)
    roundRangeG = G_Dict['roundrange']
    C_Dict = {}
    with open(C_JSON) as fcr:
        C_Dict = json.load(fcr)
    roundRangeC = C_Dict['roundrange']
    #progress = 0
    #totfiiles = len(paths)
    print("Adding Images to Database...")
    for path in tqdm(paths):
    # for path in paths:
        if os.path.exists(path):
            img = ImageDetails(path, 0.0, [0.0, 0.0, 0.0])

            if match_mode == 'avg':
                I = cv2.imread(img.path)
                I_g = cv2.imread(img.path, 0)
                img.GMatchVal = np.sum(np.sum(I_g, axis=1), axis=0) / (I_g.shape[0]*I_g.shape[1])
                img.CMatchVal = np.sum(np.sum(I, axis=1), axis=0) / (I.shape[0]*I.shape[1])
            elif match_mode == 'name': # Name is of form Type_SubDirName_000_000_000.png for color
                filename = os.path.splitext(os.path.basename(img.path))[0]
                img.CMatchVal = list(map(int, filename[-11:].split('_'))) 
                img.GMatchVal = int(0.2989 * img.CMatchVal[0] + 0.5870 * img.CMatchVal[1] + 0.1140 * img.CMatchVal[2])
            imgIndex = -1
            for i in range(len(Images)):
                if Images[i].path == img.path:
                    imgIndex = i
                    Images[i].GMatchVal = img.GMatchVal
                    Images[i].CMatchVal = img.CMatchVal
            if imgIndex == -1:
                Images.append(img)
            
            ValClassG = str(int(round(img.GMatchVal / roundRangeG)*roundRangeG))
            G_Dict[ValClassG].append(img.path)

            ValClassC = str(int(round(img.CMatchVal[0] / roundRangeC)*roundRangeC)) + '_' + str(int(round(img.CMatchVal[1] / roundRangeC)*roundRangeC)) + '_' + str(int(round(img.CMatchVal[2] / roundRangeC)*roundRangeC))
            #print(ValClassC, path)
            C_Dict[ValClassC].append(img.path)
            #progress += 1
            #print("Database Added:", progress, "/", totfiiles)

    UpdateJSONFiles(G_Dict, C_Dict, G_JSON, C_JSON)

def AddSolidColorImagesToDatabase(color_step, n_imgs_per_step, Imgsize=(100, 100, 3), match_mode='avg', DatabaseLocation='FillImgs', G_JSON='FillImgs_G.json', C_JSON='FillImgs_C.json'):
    paths = []
    print("Creating Solid Color Images...")
    for r in tqdm(range(color_step, 256, color_step)):
        for g in range(color_step, 256, color_step):
            for b in range(color_step, 256, color_step):
                for j in range(n_imgs_per_step):
                    redVal = random.randint(r-color_step, r)
                    greenVal = random.randint(g-color_step, g)
                    blueVal = random.randint(b-color_step, b)
                    img = GenerateSolidColourImage(Imgsize, (redVal, greenVal, blueVal))
                    zeropad = [str('0'*(3 - len(str(redVal)))), str('0'*(3 - len(str(greenVal)))), str('0'*(3 - len(str(blueVal))))]
                    filename = 'SolidColor_' + zeropad[0] + str(redVal) + '_' + zeropad[1] + str(greenVal) + '_' + zeropad[2] + str(blueVal) + '.png'
                    if not os.path.exists(os.path.join(DatabaseLocation, filename)):
                        cv2.imwrite(os.path.join(DatabaseLocation, filename), img)
                        paths.append(os.path.join(DatabaseLocation, filename))
                #print("Done Creating:","(" + str(r), ",", str(g) + ",", str(b) + ")")
    AddImagesToDatabase(paths, match_mode, G_JSON=G_JSON, C_JSON=C_JSON)

def AddSolidGreyScaleImagesToDatabase(color_step, n_imgs_per_step, Imgsize=(100, 100), match_mode='avg', DatabaseLocation='FillImgs', G_JSON='FillImgs_G.json', C_JSON='FillImgs_C.json'):
    paths = []
    print("Creating GrayScale Images...")
    for g in tqdm(range(color_step, 256, color_step)):
        for j in range(n_imgs_per_step):
            gVal = random.randint(g-color_step, g)
            img = GenerateSolidColourImage(Imgsize, gVal)
            zeropad = str('0'*(3 - len(str(gVal))))
            filename = 'SolidGreyScale_' + zeropad + str(gVal) + '_' + zeropad + str(gVal) + '_' + zeropad + str(gVal) + '.png'
            if not os.path.exists(os.path.join(DatabaseLocation, filename)):
                cv2.imwrite(os.path.join(DatabaseLocation, filename), img)
                paths.append(os.path.join(DatabaseLocation, filename))
        #print("Done Creating:", g)
    AddImagesToDatabase(paths, match_mode, G_JSON=G_JSON, C_JSON=C_JSON)

def GenerateSolidColourImage(Imgsize, color):
    return np.ones(Imgsize) * color

def AddColorShiftedImagesToDatabase(refImage, color_step, n_imgs_per_step, refImageName='test', Imgsize=(100, 100, 3), match_mode='name', DatabaseLocation='FillImgs_ColorShift', G_JSON='FillImgs_G_ColorShift.json', C_JSON='FillImgs_C_ColorShift.json'):
    paths = []
    print("Creating Color Shifted Images...")
    for r in tqdm(range(color_step, 256, color_step)):
        for g in range(color_step, 256, color_step):
            for b in range(color_step, 256, color_step):
                for j in range(n_imgs_per_step):
                    AvgColor = [random.randint(r-color_step, r), random.randint(g-color_step, g), random.randint(b-color_step, b)]
                    img = GenerateColorShiftedImage(refImage, AvgColor)
                    zeropad = [str('0'*(3 - len(str(AvgColor[0])))), str('0'*(3 - len(str(AvgColor[1])))), str('0'*(3 - len(str(AvgColor[2]))))]
                    filename = 'ColorShift_' + refImageName + '_' + zeropad[0] + str(AvgColor[0]) + '_' + zeropad[1] + str(AvgColor[1]) + '_' + zeropad[2] + str(AvgColor[2]) + '.png'
                    if not os.path.exists(os.path.join(DatabaseLocation, filename)):
                        cv2.imwrite(os.path.join(DatabaseLocation, filename), img)
                        paths.append(os.path.join(DatabaseLocation, filename))
                #print("Done Creating:","(" + str(r), ",", str(g) + ",", str(b) + ")")
    AddImagesToDatabase(paths, match_mode, G_JSON=G_JSON, C_JSON=C_JSON)

def AddGreyScaleShiftedImagesToDatabase(refImage, color_step, n_imgs_per_step, refImageName='test', Imgsize=(100, 100), match_mode='avg', DatabaseLocation='FillImgs_ColorShift', G_JSON='FillImgs_G_GreyScaleShift.json', C_JSON='FillImgs_C_GreyScaleShift.json'):
    paths = []
    print("Creating GrayScale Images...")
    for g in tqdm(range(color_step, 256, color_step)):
        for j in range(n_imgs_per_step):
            AvgScale = random.randint(g-color_step, g)
            img = GenerateColorShiftedImage(refImage, AvgScale)
            zeropad = str('0'*(3 - len(str(AvgScale))))
            filename = 'GreyScaleShift_' + refImageName + '_' + zeropad + str(AvgScale) + '_' + zeropad + str(AvgScale) + '_' + zeropad + str(AvgScale) + '.png'
            if not os.path.exists(os.path.join(DatabaseLocation, filename)):
                cv2.imwrite(os.path.join(DatabaseLocation, filename), img)
                paths.append(os.path.join(DatabaseLocation, filename))
        #print("Done Creating:", g)
    AddImagesToDatabase(paths, match_mode, G_JSON=G_JSON, C_JSON=C_JSON)

def GenerateColorShiftedImage(Image, ExpectedAvgColor):
    I = Image.copy().astype(int)
    avgC = np.round(np.sum(np.sum(I, axis=1), axis=0) / (I.shape[0]*I.shape[1])).astype(int)
    AvgDiff = np.clip(ExpectedAvgColor - avgC, 0, 255)
    I = np.clip(np.add(I, AvgDiff), 0, 255)
    return I.astype(np.uint8)

def ImageBreak(originalImage, window_size, match_mode, fillImageSize=(100, 100), nextImageMode='increment', roundRange=10, DisplayIntermiateSteps=True):
    global BoundingBoxRadius
    newImage = None
    colorImg = (originalImage.ndim == 3)
    if not colorImg:
        newImageSize = (fillImageSize[0]*(int(round(originalImage.shape[0] / window_size[0])) + 1), 
                        fillImageSize[1]*(int(round(originalImage.shape[1] / window_size[1])) + 1))
        newImage = np.zeros(newImageSize)

        ni = 0
        nj = 0

        for i in tqdm(range(0, originalImage.shape[0], window_size[0])):
            nj = 0
            for j in range(0, originalImage.shape[1], window_size[1]):
                if match_mode == 'avg':
                    AvgPixVal = None
                    ImageWindowPortion = None
                    if (i+window_size[0] < originalImage.shape[0] and j+window_size[1] < originalImage.shape[1]):
                        ImageWindowPortion = originalImage[i:i+window_size[0], j:j+window_size[1]]
                    else:
                        ImageWindowPortion = originalImage[i:, j:]
                    AvgPixVal = AveragePixelValue(ImageWindowPortion)
                    #print("Matching: ", ni*fillImageSize[0], (ni+1)*fillImageSize[0], nj*fillImageSize[1], (nj+1)*fillImageSize[1])
                    newImage[ni*fillImageSize[0]:(ni+1)*fillImageSize[0], nj*fillImageSize[1]:(nj+1)*fillImageSize[1]] = ResizeImage(GetMatchingImage(AvgPixVal, match_mode, colorImg, nextImageMode=nextImageMode, roundRange=roundRange), fillImageSize)
                    zerocheck = np.sum(np.sum(newImage[ni*fillImageSize[0]:(ni+1)*fillImageSize[0], nj*fillImageSize[1]:(nj+1)*fillImageSize[1]], axis=1), axis=0)
                    if DisplayIntermiateSteps and zerocheck != 0.0:
                        originalImage_WindowHighlighted = BoundingBox(originalImage, [i, j], window_size, radius=BoundingBoxRadius, color=[50, 50, 50])
                        axw = plt.subplot(2, 2, 1)
                        plt.imshow(originalImage_WindowHighlighted, 'gray')
                        axw.title.set_text('OriginalImg')
                        axw = plt.subplot(2, 2, 2)
                        plt.imshow(ImageWindowPortion, 'gray')
                        axw.title.set_text('WindowPortion')
                        axp = plt.subplot(2, 2, 3)
                        plt.imshow(newImage[ni*fillImageSize[0]:(ni+1)*fillImageSize[0], nj*fillImageSize[1]:(nj+1)*fillImageSize[1]], 'gray')
                        axp.title.set_text('DBImgPortion')
                        ax = plt.subplot(2, 2, 4)
                        plt.imshow(newImage, 'gray')
                        ax.title.set_text('FullSplitImg')
                        plt.show()
                        #DisplayIntermiateSteps = (input("Disp: ") == '')
                nj += 1
            ni += 1
    else:
        #fillImageSize = (fillImageSize[0], fillImageSize[1], originalImage.shape[2])
        newImageSize = (fillImageSize[0]*(int(round(originalImage.shape[0] / window_size[0])) + 1), 
                        fillImageSize[1]*(int(round(originalImage.shape[1] / window_size[1])) + 1), 
                        originalImage.shape[2])
        newImage = np.zeros(newImageSize)

        ni = 0
        nj = 0

        for i in tqdm(range(0, originalImage.shape[0], window_size[0])):
            nj = 0
            for j in range(0, originalImage.shape[1], window_size[1]):
                if match_mode == 'avg':
                    AvgPixVal = None
                    ImageWindowPortion = None
                    if (i+window_size[0] < originalImage.shape[0] and j+window_size[1] < originalImage.shape[1]):
                        ImageWindowPortion = originalImage[i:i+window_size[0], j:j+window_size[1], :]
                    else:
                        ImageWindowPortion = originalImage[i:, j:, :]
                    AvgPixVal = AveragePixelValue(ImageWindowPortion)
                    #print("Matching: ", ni*fillImageSize[0], (ni+1)*fillImageSize[0], nj*fillImageSize[1], (nj+1)*fillImageSize[1])
                    newImage[ni*fillImageSize[0]:(ni+1)*fillImageSize[0], nj*fillImageSize[1]:(nj+1)*fillImageSize[1], :] = ResizeImage(GetMatchingImage(AvgPixVal, match_mode, colorImg, nextImageMode=nextImageMode, roundRange=roundRange), fillImageSize)
                    zerocheck = np.sum(np.sum(newImage[ni*fillImageSize[0]:(ni+1)*fillImageSize[0], nj*fillImageSize[1]:(nj+1)*fillImageSize[1], :], axis=1), axis=0)
                    if DisplayIntermiateSteps and zerocheck != 0.0:
                        originalImage_WindowHighlighted = BoundingBox(originalImage, [i, j], window_size, radius=BoundingBoxRadius, color=[0, 0, 0])
                        axw = plt.subplot(2, 2, 1)
                        plt.imshow(originalImage_WindowHighlighted)
                        axw.title.set_text('OriginalImg')
                        axw = plt.subplot(2, 2, 2)
                        plt.imshow(ImageWindowPortion)
                        axw.title.set_text('WindowPortion')
                        axp = plt.subplot(2, 2, 3)
                        plt.imshow(newImage[ni*fillImageSize[0]:(ni+1)*fillImageSize[0], nj*fillImageSize[1]:(nj+1)*fillImageSize[1]])
                        axp.title.set_text('DBImgPortion')
                        ax = plt.subplot(2, 2, 4)
                        plt.imshow(newImage)
                        ax.title.set_text('FullSplitImg')
                        plt.show()
                        #DisplayIntermiateSteps = (input("Disp: ") == '')
                nj += 1
            ni += 1
    return newImage


def LoadFillImagesData(G_JSON='FillImgs_G.json', C_JSON='FillImgs_C.json'):
    global fillImg_G_dict
    global fillImgIndex_G_dict
    global fillImg_C_dict
    global fillImgIndex_C_dict
    with open(G_JSON) as f:
        fillImg_G_dict = json.load(f)
    for key in fillImg_G_dict.keys():
        fillImgIndex_G_dict[key] = 0
    with open(C_JSON) as f:
        fillImg_C_dict = json.load(f)
    for key in fillImg_C_dict.keys():
        fillImgIndex_C_dict[key] = 0

                    
                    
def GetMatchingImage(MatchVal, match_mode, colorImg, nextImageMode='increment', roundRange=10):
    global fillImg_G_dict
    global fillImgIndex_G_dict
    global fillImg_C_dict
    global fillImgIndex_C_dict

    if not colorImg:
        if match_mode in ['avg', 'min', 'max', 'median', 'mode']:
            ValClass = str(int(round(MatchVal / roundRange)*roundRange))
            #print("MatchClass:", ValClass, " - Found DBImgs:", len(fillImg_G_dict[ValClass]))
            if len(fillImg_G_dict[ValClass]) > 0:
                #print("Using ImgIndex:", fillImgIndex_G_dict[ValClass])
                fillImgPath = fillImg_G_dict[ValClass][fillImgIndex_G_dict[ValClass]]
                if nextImageMode == 'increment':
                    fillImgIndex_G_dict[ValClass] = int((fillImgIndex_G_dict[ValClass] + 1) % len(fillImg_G_dict[ValClass]))
                elif nextImageMode == 'random':
                    fillImgIndex_G_dict[ValClass] = random.randint(0, len(fillImg_G_dict[ValClass])-1)
                return cv2.imread(fillImgPath, 0)
            else:
                return np.zeros((1, 1))
    else:
        if match_mode in ['avg', 'min', 'max', 'median', 'mode']:
            ValClass = str(int(round(MatchVal[0] / roundRange)*roundRange)) + '_' + str(int(round(MatchVal[1] / roundRange)*roundRange)) + '_' + str(int(round(MatchVal[2] / roundRange)*roundRange))
            #print("MatchClass:", ValClass, " - Found DBImgs:", len(fillImg_C_dict[ValClass]))
            if len(fillImg_C_dict[ValClass]) > 0:
                #print("Using ImgIndex:", fillImgIndex_C_dict[ValClass])
                fillImgPath = fillImg_C_dict[ValClass][fillImgIndex_C_dict[ValClass]]
                if nextImageMode == 'increment':
                    fillImgIndex_C_dict[ValClass] = int((fillImgIndex_C_dict[ValClass] + 1) % len(fillImg_C_dict[ValClass]))
                elif nextImageMode == 'random':
                    fillImgIndex_C_dict[ValClass] = random.randint(0, len(fillImg_C_dict[ValClass])-1)
                return cv2.imread(fillImgPath)
            else:
                return np.zeros((1, 1, len(MatchVal)))

def ResizeImage(Image, fillImgSize):
    return cv2.resize(Image, fillImgSize)


def AveragePixelValue(Image):
    return (np.sum(np.sum(Image, axis=1), axis=0) / (Image.shape[0]*Image.shape[1])).astype(int)