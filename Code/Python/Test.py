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
    import random
    #IE
    matrix = []

    for i in range(matrixSize[0]):
        row = []
        for j in range(matrixSize[1]):
            row.append(random.randint(ValRange[0], ValRange[1]))
        matrix.append(row)
    
    return matrix
#FE