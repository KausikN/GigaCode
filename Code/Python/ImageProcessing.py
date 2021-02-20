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
#FS
def CreateMatrix_UserInput(matrixSize):
    #DS
    # Creates a matrix with user input
    #DE
    #IS
    #IE

    matrix = []

    for i in range(matrixSize[0]):
        row = []
        for j in range(matrixSize[1]):
            row.append(int(input("Enter value at (" + str(i) + ", " + str(j) + "): ")))
        matrix.append(row)
    
    return matrix
#FE

#FS
def CreateMatrix_RandomInput(matrixSize, ValRange):
    #DS
    # Creates a matrix with random input
    #DE
    #IS
    #IE

    matrix = []

    for i in range(matrixSize[0]):
        row = []
        for j in range(matrixSize[1]):
            row.append(random.randint(ValRange[0], ValRange[1]))
        matrix.append(row)
    
    return matrix
#FE

# Image Matrix Operations
#FS
def MatSum(matrix):
    #DS
    # Calculate sum of all values in a matrix
    #DE
    #IS
    #IE

    sum = 0

    for row in matrix:
        for val in row:
            sum += val
    
    return sum
#FE

#FS
def MatMax(matrix):
    #DS
    # Calculate max of all values in a matrix
    #DE
    #IS
    #IE

    max = 0

    for row in matrix:
        for val in row:
            if max < val:
                max = val
    
    return max
#FE

#FS
def MatFreqDist(matrix):
    #DS
    # Calculate frequency distribution of all values in a matrix
    #DE
    #IS
    #IE

    freq = {}

    for row in matrix:
        for val in row:
            if val in freq.keys():
                freq[val] += 1
            else:
                freq[val] = 1

    return freq
#FE

#FS
def MatMean(matrix):
    #DS
    # Calculate mean of all values in a matrix
    #DE
    #IS
    #IE

    sum = 0
    for row in matrix:
        for val in row:
            sum += val
    return sum / (len(matrix) * len(matrix[0]))
#FE

#FS
def MatMedian(matrix):
    #DS
    # Calculate median of all values in a matrix
    #DE
    #IS
    #IE

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
#FE

#FS
def MatMode(matrix):
    #DS
    # Calculate mode of all values in a matrix
    #DE
    #IS
    #IE

    modeVal = -1
    modeVal_freq = -1

    freq = MatFreqDist(matrix)

    for key in freq.keys():
        if freq[key] > modeVal_freq:
            modeVal = key
            modeVal_freq = freq[key]

    return modeVal
#FE

#FS
def MatStandardDeviation(matrix):
    #DS
    # Calculate Standard Deviation of all values in a matrix
    #DE
    #IS
    #IE

    SD = 0.0

    mean = MatMean(matrix)
    sumsqaurediff = 0.0
    for row in matrix:
        for val in row:
            sumsqaurediff += (val - mean) ** 2
    SD = (sumsqaurediff / (len(matrix) * len(matrix[0]))) ** (1/2)

    return SD
#FE

#FS
def ImageFreqDist(Image, pixelRange=(0, 255)):
    #DS
    # Calculate frequency distribution of all values in a image
    #DE
    #IS
    from tqdm import tqdm
    #IE

    Freq = []
    for i in range(pixelRange[0], pixelRange[1]+1):
        Freq.append(0)
    for row in tqdm(Image):
        for pixel in row:
            Freq[pixel - pixelRange[0]] += 1
    return Freq
#FE

#FS
def GetCumulativeDist(Dist):
    #DS
    # Calculate Cumulative distribution of a distribution
    #DE
    #IS
    #IE

    CumulativeDist = []
    cumulativeVal = 0.0
    for d in Dist:
        cumulativeVal += d
        CumulativeDist.append(cumulativeVal)
    return np.array(CumulativeDist)
#FE

#FS
def HistPlot(Data, nbins=25):
    #DS
    # Plot Histogram of data
    #DE
    #IS
    import numpy as np
    import matplotlib.pyplot as plt
    #IE

    X = np.arange(len(Data))
    n, bins, patches = plt.hist(Data, nbins, facecolor='blue', alpha=0.5)
    plt.show()
#FE

#FS
def ceil(a):
    #DS
    # Calculate ceiling of a value
    #DE
    #IS
    #IE

    if (a-float(int(a))) > 0:
        return a + 1
    return a
#FE

# Image Conversion
#FS
def rgb2gray(I):
    #DS
    # Convert RGB image to GreyScale
    #DE
    #IS
    import numpy as np
    #IE

    I = I.astype(int)
    r, g, b = I[:,:,0], I[:,:,1], I[:,:,2]
    gray = (0.2989 * r + 0.5870 * g + 0.1140 * b)
    # gray = (1 * r + 1 * g + 1 * b) / 3
    return gray.astype(np.uint8)
#FE

# Image Noise Addition
#FS
def SaltPepperNoise(I, prob):
    #DS
    # Add Salt and Pepper noise to a image
    #DE
    #IS
    import random
    import numpy as np
    #IE

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
#FE

#FS
def GaussianNoise(I, mean, variance):
    #DS
    # Add Gaussian noise to a image
    #DE
    #IS
    import numpy as np
    #IE

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
#FE

#FS
def SpeckleNoise(I):
    #DS
    # Add Speckle noise to a image
    #DE
    #IS
    import numpy as np
    #IE

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
#FE

# Image Operations
#FS
def ImgAverage(Is):
    #DS
    # Get Average image of many images
    #DE
    #IS
    import numpy as np
    #IE

    AvgI = Is[0].copy().astype(int)
    for imgindex in range(len(Is)):
        if imgindex != 0:
            Is[imgindex] = Is[imgindex].astype(int)
            AvgI = np.add(AvgI, Is[imgindex])
    AvgI = np.divide(AvgI, len(Is)).astype(int)
    AvgI = AvgI.astype(np.uint8)
    return AvgI
#FE

#FS
def BillinearInterpolation_Scaling(Image, Scale=(2, 2)):
    #DS
    # Scale an image using Billinear Interpolation Algorithm
    #DE
    #IS
    import numpy as np
    from tqdm import tqdm
    #IE

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
#FE

#FS
def BillinearInterpolation_Rotation(Image, Angle=0.0):
    #DS
    # Rotate an image using Billinear Interpolation Algorithm
    #DE
    #IS
    import numpy as np
    from tqdm import tqdm
    #IE

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
#FE

#FS
def RotateImage(Image, angle, cropBoundary=False):
    #DS
    # Rotate an image
    #DE
    #IS
    import imutils
    import numpy as np
    #IE

    RotatedImage = None
    if cropBoundary:
        RotatedImage = imutils.rotate(Image, angle)
    else:
        RotatedImage = imutils.rotate_bound(Image, angle)
    return RotatedImage
#FE

# Image Transformation
#FS
def ImagePixelReplace(Image, pixelReplaceVals):
    #DS
    # Replace all pixel values in an image using a mapping
    #DE
    #IS
    import numpy as np
    from tqdm import tqdm
    #IE

    I = np.zeros(Image.shape)
    for i in tqdm(range(Image.shape[0])):
        for j in range(Image.shape[1]):
            I[i, j] = pixelReplaceVals[Image[i, j]]
    return I
#FE

#FS
def NormaliseToRange(I, Range=(0, 255)):
    #DS
    # Normalise all values in a matrix to a range
    #DE
    #IS
    import numpy as np
    #IE

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
#FE

#FS
def HistogramMatching(I_input, I_ref, pixelRange=(0, 255)):
    #DS
    # Perform Histogram matching algorithm on an input image and a reference image
    #DE
    #IS
    import random
    import numpy as np
    from tqdm import tqdm
    #IE

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
#FE

#FS
def HistogramEqualisation(Image, pixelRange=(0, 255)):
    #DS
    # Perform Histogram Equalisation algorithm on an image
    #DE
    #IS
    import numpy as np
    #IE

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
#FE

#FS
def CrossCorrelation(I, W, stride=(1, 1), mean_mode='full'):
    #DS
    # Perform Cross Correlation algorithm on an input image with a window
    #DE
    #IS
    import numpy as np
    from tqdm import tqdm
    #IE

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
#FE

#FS
def Correlation(I, W, stride=(1, 1)):
    #DS
    # Perform Correlation algorithm on an input image with a window
    #DE
    #IS
    import numpy as np
    from tqdm import tqdm
    #IE

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
#FE

#FS
def ApplyMedianFilter(I, WSize=(3, 3), stride=(1, 1)):
    #DS
    # Apply Median filtering to an image
    #DE
    #IS
    import numpy as np
    from tqdm import tqdm
    #IE

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
#FE

# Image Filters
#FS
def GenerateEdgeFilter(size=(3, 3)):
    #DS
    # Generate an Edge filter window
    #DE
    #IS
    import numpy as np
    #IE

    if size[0]%2 == 0 or size[1] == 0:
        return None
    W = np.ones(size) * -1
    W[int(size[0]/2), int(size[1]/2)] = -(size[0]*size[1] - 1)
    return W
#FE

#FS
def GenerateAverageFilter(size=(3, 3)):
    #DS
    # Generate an average filter window
    #DE
    #IS
    import numpy as np
    #IE

    return np.ones(size).astype(float) / (size[0]*size[1])
#FE

# Image Augmentation
#FS
def BoundingBox(Image, pos, window_size, radius=1, color=[0, 0, 0]):
    #DS
    # Apply Bounding box at a location in an image
    #DE
    #IS
    import numpy as np
    #IE

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
#FE

#FS
def GenerateSolidColourImage(Imgsize, color):
    #DS
    # Generate an image with a single solid color
    #DE
    #IS
    import numpy as np
    #IE

    return np.ones(Imgsize) * color
#FE

#FS
def GenerateColorShiftedImage(Image, ExpectedAvgColor):
    #DS
    # Generate an image by shifting the colors in another image
    #DE
    #IS
    import numpy as np
    #IE

    I = Image.copy().astype(int)
    avgC = np.round(np.sum(np.sum(I, axis=1), axis=0) / (I.shape[0]*I.shape[1])).astype(int)
    AvgDiff = np.clip(ExpectedAvgColor - avgC, 0, 255)
    I = np.clip(np.add(I, AvgDiff), 0, 255)
    return I.astype(np.uint8)
#FE

#FS
def ResizeImage(Image, fillImgSize):
    #DS
    # Resize an image using cv2 library
    #DE
    #IS
    import cv2
    #IE

    return cv2.resize(Image, fillImgSize)
#FE

#FS
def AveragePixelValue(Image):
    #DS
    # Get the average pixel value in an image
    #DE
    #IS
    import numpy as np
    #IE

    return (np.sum(np.sum(Image, axis=1), axis=0) / (Image.shape[0]*Image.shape[1])).astype(int)
#FE