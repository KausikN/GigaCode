'''
Summary
Library of Big Data Analytics Functions made by ME
'''

# Imports
import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import pandas as pd
import statsmodels.api as sm 
import pylab as py

# Data Generation
#FS
def ReadCSVFile(filepath):
    #DS
    # Read CSV File as pandas dataframe
    #DE
    #IS
    import pandas as pd
    #IE

    return pd.read_csv(filepath)
#FE

#FS
def GenerateRandomData(n_data, range):
    #DS
    # Generate n random integers from specified range
    #DE
    #IS
    import random
    #IE

    X = []
    Y = []
    for i in range(n_data):
        x = random.randint(range[0], range[1])
        y = (2 * x) + 3
        X.append(x)
        Y.append(y)
    return X, Y
#FE

#FS
def GenerateStandardNormalDist(n, mean=0.0, SD=1.0):
    #DS
    # Generate n values from Standard Normal Distribution
    #DE
    #IS
    import numpy as np
    #IE

    return np.random.normal(mean, SD, (n))
#FE

#FS
def GenerateLogNormalDist(n, mean=0.0, SD=1.0):
    #DS
    # Generate n values from Log Normal Distribution
    #DE
    #IS
    import numpy as np
    #IE

    return np.random.lognormal(mean, SD, (n))
#FE

# Data Analysis
#FS
def Mean(values):
    #DS
    # Calculate mean of values
    #DE
    #IS
    #IE

    sum = 0
    for v in values:
        sum += v
    return sum / len(values)
#FE

#FS
def Median(values):
    #DS
    # Calculate median of values
    #DE
    #IS
    #IE

    values.sort()

    if len(values) % 2 == 1:
        return values[int((len(values) - 1)/2)]
    else:
        return (values[int(len(values)/2)] + values[int(len(values)/2 - 1)]) / 2
#FE

#FS
def Mode(X):
    #DS
    # Calculate mode of values
    #DE
    #IS
    #IE

    modex = -1
    modex_freq = -1

    freq = FreqDist(X)

    for key in freq.keys():
        if freq[key] > modex_freq:
            modex = key
            modex_freq = freq[key]

    return modex
#FE

#FS
def BubbleSort(arr):
    #DS
    # Bubblesort for sorting an array
    #DE
    #IS
    #IE

    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
#FE

#FS
def StandardDeviation(X):
    #DS
    # Calculate Standard Deviation of values
    #DE
    #IS
    #IE

    SD = 0.0

    mean = Mean(X)
    sumsqaurediff = 0.0
    for x in X:
        sumsqaurediff += (x - mean) ** 2
    SD = (sumsqaurediff / len(X)) ** (1/2)

    return SD
#FE

#FS
def Skewness(X):
    #DS
    # Calculate Skewness of values
    #DE
    #IS
    #IE

    return (Mean(X) - Mode(X)) / StandardDeviation(X)
#FE

#FS
def Sum(X):
    #DS
    # Calculate Sum of values
    #DE
    #IS
    #IE

    sum = 0
    for x in X:
        sum += x
    return sum
#FE

#FS
def Max(X):
    #DS
    # Calculate Max of values
    #DE
    #IS
    #IE

    max = 0
    for x in X:
        if max < x:
            max = x
    return max
#FE

#FS
def FreqDist(X):
    #DS
    # Calculate Frequency Distribution of values
    #DE
    #IS
    #IE

    freq = {}
    for x in X:
        freq[x] = 0
    for x in X:
        freq[x] += 1
    return freq
#FE

#FS
def FreqDist_ClassLimited(X, allowedClasses=[]):
    #DS
    # Calculate Frequency Distribution of values for only specific classes or labels
    #DE
    #IS
    #IE

    # Accepts only 1, 2, 3, other
    freq = {}
    for c in allowedClasses:
        freq[c] = 0
    freq['other'] = 0
    for x in X:
        if x in allowedClasses:
            freq[str(x)] += 1
        else:
            freq['other'] += 1
    return freq
#FE

#FS
def FreqDist_Bins(X, binsize):
    #DS
    # Calculate Frequency Distribution of values with binning
    #DE
    #IS
    #IE

    values = []
    Freq = {}
    minVal = int(min(X))
    maxVal = int(round(max(X)))
    print("Range:", minVal, "-", maxVal)
    for i in range(minVal, maxVal+1, binsize):
        values.append(i)
        Freq[str(i)] = 0
    for x in X:
        key = int(int((round(x) - minVal)/binsize)*binsize + minVal)
        Freq[str(key)] += 1
    return Freq
#FE

#FS
def Correlation(X, Y):
    #DS
    # Calculate Correlation of 2 sets of values
    #DE
    #IS
    #IE

    n = len(X)
    sig_xy = 0
    sig_x = 0
    sig_y = 0
    sig_x2 = 0
    sig_y2 = 0
    for x, y in zip(X, Y):
        sig_xy += x*y
        sig_x += x
        sig_y += y
        sig_x2 += x**2
        sig_y2 += y**2

    corr = ((n*sig_xy) - (sig_x*sig_y)) / (((n*sig_x2 - (sig_x**2)) * (n*sig_y2 - (sig_y**2)))**(1/2))
    return corr
#FE

#FS
def PrintNonZeroFreq(FreqDist, binsize):
    #DS
    # Display non-zero frquency values in a frequency distribution
    #DE
    #IS
    #IE

    print("Freq Dist " + str(binsize) + " Non Zero Values: ")
    nbins = 0
    for k in FreqDist.keys():
        if FreqDist[k] > 0:
            nbins += 1
            #print(k, ":", FreqDist[k], "\n")
    print("Found", nbins, "non empty bins")
#FE

#FS
def MissingCount(Data, label):
    #DS
    # Get count of missing values in a data label associated data
    #DE
    #IS
    #IE

    missing = 0
    indices = []
    i = 0
    for d in Data[label]:
        if str(d).strip().replace('nan', '') in ['', ' '] or 'NaN' in str(d):
            missing += 1
            indices.append(i)
        i += 1
    return missing, indices
#FE

# Data Normalisations
#FS
def MinMaxNorm(X):
    #DS
    # Calculate Min-Max Norm of values
    #DE
    #IS
    #IE

    minVal = min(X)
    maxVal = max(X)
    X_Norm = []
    for x in X:
        X_Norm.append(round((x - minVal) / (maxVal - minVal), 2))
    return X_Norm
#FE

#FS
def ZScoreNorm(X, mean, SD):
    #DS
    # Calculate Z-Score Norm of values
    #DE
    #IS
    #IE

    X_Norm = []
    for x in X:
        X_Norm.append(round(((x - mean) / SD), 2))
    return X_Norm
#FE

#FS
def DecimalScaleNorm(X):
    #DS
    # Calculate Decimal Scale Norm of values
    #DE
    #IS
    #IE

    maxVal = max(X)
    divpow = len(str(maxVal))
    X_Norm = []
    for x in X:
        X_Norm.append(round((x / (10 ** divpow)), 2))
    return X_Norm
#FE

# Data Visualisation / Plots
# Tables
#FS
def GenerateTallyStr(no):
    #DS
    # Generate Tally marks string for a number
    #DE
    #IS
    #IE

    five = '||||\\ '
    tally = five * int(no / 5) + '|' * (no % 5)
    return tally
#FE

# Plots
#FS
def GeneratePieChart(data, labels):
    #DS
    # Generate Pie Chart for data
    #DE
    #IS
    import matplotlib.pyplot as plt
    #IE

    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'grey']
    plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()
#FE

#FS
def GenerateBarGraph(data, labels):
    #DS
    # Generate Bar Chart for data
    #DE
    #IS
    import matplotlib.pyplot as plt
    #IE

    plt.bar(data, data, align='center', alpha=0.5)
    plt.xticks(data, labels)
    plt.xlabel('Grades')
    plt.ylabel('No of Students')
    plt.title('Class Performance')
    plt.show()
#FE

#FS
def GenerateHistogram(Marks):
    #DS
    # Generate Histogram for data
    #DE
    #IS
    import numpy as np
    import matplotlib.pyplot as plt
    #IE

    n_bins = 10
    X = np.arange(len(Marks))
    n, bins, patches = plt.hist(Marks, n_bins, facecolor='blue', alpha=0.5)
    plt.show()
#FE

#FS
def Generate_Stems_Leaves(data, leaflen):
    #DS
    # Generate Stems and Leaves from data
    #DE
    #IS
    #IE

    leaves = []
    stems = []
    for d in data:
        leaves.append(int(str(d)[(-1*leaflen):]))
        stems.append(int(str(d)[:(-1*leaflen)]))
    return stems, leaves
#FE

#FS
def GenerateStemPlot(stems, leaves):
    #DS
    # Generate Stem-Leaf plot for data
    #DE
    #IS
    import matplotlib.pyplot as plt
    #IE

    plt.title('Stem and Leaf Plot')
    plt.xlabel('Stems')
    plt.ylabel('Leaves')
    markerline, stemlines, baseline = plt.stem(stems, leaves)
    plt.show()
#FE

#FS
def DensityPlot(X, labels):
    #DS
    # Generate Density plot for data
    #DE
    #IS
    import seaborn as sns
    import matplotlib.pyplot as plt
    #IE

    for x, label in zip(X, labels):
        sns.distplot(x, hist = False, kde = True,
                    kde_kws = {'linewidth': 3},
                    label = label)
    
    # Plot formatting
    plt.legend(prop={'size': 16}, title = 'Water vs Beverage')
    plt.title('Density Plot')
    plt.xlabel('Days')
    plt.ylabel('Consumption')
    plt.show()
#FE

#FS
def RugPlot(X, labels):
    #DS
    # Generate Rug plot for data
    #DE
    #IS
    import seaborn as sns
    import matplotlib.pyplot as plt
    #IE

    for x, label in zip(X, labels):
        sns.rugplot(x, label=label)
    plt.title('Rug Plot')
    plt.xlabel('Days')
    plt.ylabel('Consumption')
    plt.show()
#FE

#FS
def Scatterplot(X, Y):
    #DS
    # Generate Scatter plot for data
    #DE
    #IS
    import matplotlib.pyplot as plt
    #IE

    plt.scatter(X, Y)
    plt.title('Scatter Plot')
    plt.xlabel('Mass')
    plt.ylabel('Litres')
    plt.show()
#FE

#FS
def BoxPlot(X, title='', xlabel='', ylabel=''):
    #DS
    # Generate Box plot for data
    #DE
    #IS
    import matplotlib.pyplot as plt
    #IE

    plt.boxplot(X)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
#FE

#FS
def SwarmPlot(X, title='', xlabel='', ylabel=''):
    #DS
    # Generate Swarm plot for data
    #DE
    #IS
    import seaborn as sns
    import matplotlib.pyplot as plt
    #IE

    sns.swarmplot(X)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
#FE

#FS
def JitteredBoxPlot(X, title='', xlabel='', ylabel=''):
    #DS
    # Generate Jittered Box plot for data
    #DE
    #IS
    import seaborn as sns
    import matplotlib.pyplot as plt
    #IE

    sns.boxplot(data=X)
    sns.swarmplot(data=X, color='grey')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
#FE

#FS
def ViolinPlot(X, title=''):
    #DS
    # Generate Violin plot for data
    #DE
    #IS
    import matplotlib.pyplot as plt
    #IE

    plt.violinplot(X)
    plt.title(title)
    plt.show()
#FE

#FS
def RadarPlot(name, statsList, attribute_labels, plot_markers, plot_str_markers):
    #DS
    # Generate Radar plot for data
    #DE
    #IS
    import numpy as np
    import matplotlib.pyplot as plt
    #IE

    labels = np.array(attribute_labels)
    fig= plt.figure()
    for stats in statsList:
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
        stats = np.concatenate((stats,[stats[0]]))
        angles = np.concatenate((angles,[angles[0]]))

        ax = fig.add_subplot(111, polar=True)
        ax.plot(angles, stats, 'o-', linewidth=2)
        ax.fill(angles, stats, alpha=0.25)
        ax.set_thetagrids(angles * 180/np.pi, labels)
        plt.yticks(markers)
        ax.set_title(name)
        ax.grid(True)
    plt.show()
#FE

#FS
def RadarPlot_PlotLY(statsList, labels):
    #DS
    # Generate Radar plot for data using PlotLY module
    #DE
    #IS
    import pandas as pd
    import plotly.express as px
    #IE

    for stats in statsList:
        df = pd.DataFrame(dict(r=stats, theta=labels))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.show()
#FE

#FS
def FunnelPlot(X, labels):
    #DS
    # Generate Funnel plot for data using PlotLY module
    #DE
    #IS
    import plotly.express as px
    #IE

    data = dict(number=X, stage=labels)
    fig = px.funnel(data, x='number', y='stage')
    fig.show()
#FE