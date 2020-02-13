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
def ReadCSVFile(filepath):
    return pd.read_csv(filepath)

def GenerateData(n_data, MaxVal):
    X = []
    Y = []
    for i in range(n_data):
        x = random.randint(6, MaxVal)
        y = (2 * x) + 3
        X.append(x)
        Y.append(y)
    return X, Y

def GenerateStandardNormalDist(n, mean=0.0, SD=1.0):
    return np.random.normal(mean, SD, (n))

def GenerateLogNormalDist(n, mean=0.0, SD=1.0):
    return np.random.lognormal(mean, SD, (n))

# Data Analysis
def Mean(marks):
    sum = 0
    for mark in marks:
        sum += mark
    return sum / len(marks)

def Median(marks):
    BubbleSort(marks)

    if len(marks) % 2 == 1:
        return marks[int((len(marks) - 1)/2)]
    else:
        return (marks[int(len(marks)/2)] + marks[int(len(marks)/2 - 1)]) / 2

def Mode(X):
    modex = -1
    modex_freq = -1

    freq = FreqDist(X)

    for key in freq.keys():
        if freq[key] > modex_freq:
            modex = key
            modex_freq = freq[key]

    return modex

def BubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]

def StandardDeviation(X):
    SD = 0.0

    mean = Mean(X)
    sumsqaurediff = 0.0
    for x in X:
        sumsqaurediff += (x - mean) ** 2
    SD = (sumsqaurediff / len(X)) ** (1/2)

    return SD

def Skewness(X):
    return (Mean(X) - Mode(X)) / StandardDeviation(X)

def Sum(X):
    sum = 0
    for x in X:
        sum += x
    return sum

def Max(X):
    max = 0
    for x in X:
        if max < x:
            max = x
    return max

def FreqDist(X):
    freq = {}
    for x in X:
        freq[x] = 0
    for x in X:
        freq[x] += 1
    return freq

def FreqDist_ClassLimited(X, allowedClasses=[]):
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

def FreqDist_Bins(X, binsize):
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

def Correlation(X, Y):
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

def PrintNonZeroFreq(FreqDist, binsize):
    print("Freq Dist " + str(binsize) + " Non Zero Values: ")
    nbins = 0
    for k in FreqDist.keys():
        if FreqDist[k] > 0:
            nbins += 1
            #print(k, ":", FreqDist[k], "\n")
    print("Found", nbins, "non empty bins")

def MissingCount(Data, label):
    missing = 0
    indices = []
    i = 0
    for d in Data[label]:
        if str(d).strip().replace('nan', '') in ['', ' '] or 'NaN' in str(d):
            missing += 1
            indices.append(i)
        i += 1
    return missing, indices

# Data Normalisations
def MinMaxNorm(X):
    minVal = min(X)
    maxVal = max(X)
    X_Norm = []
    for x in X:
        X_Norm.append(round((x - minVal) / (maxVal - minVal), 2))
    return X_Norm

def ZScoreNorm(X, mean, SD):
    X_Norm = []
    for x in X:
        X_Norm.append(round(((x - mean) / SD), 2))
    return X_Norm

def DecimalScaleNorm(X):
    maxVal = max(X)
    divpow = len(str(maxVal))
    X_Norm = []
    for x in X:
        X_Norm.append(round((x / (10 ** divpow)), 2))
    return X_Norm

# Data Visualisation / Plots
# Tables
def GenerateTallyStr(no):
    five = '||||\\ '
    tally = five * int(no / 5) + '|' * (no % 5)
    return tally

# Plots
def GeneratePieChart(data, labels):
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'grey']
    plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()

def GenerateBarGraph(data, labels):
    plt.bar(data, data, align='center', alpha=0.5)
    plt.xticks(data, labels)
    plt.xlabel('Grades')
    plt.ylabel('No of Students')
    plt.title('Class Performance')
    plt.show()

def GenerateHistogram(Marks):
    n_bins = 10
    X = np.arange(len(Marks))
    n, bins, patches = plt.hist(Marks, n_bins, facecolor='blue', alpha=0.5)
    plt.show()

def Generate_Stems_Leaves(data, leaflen):
    leaves = []
    stems = []
    for d in data:
        leaves.append(int(str(d)[(-1*leaflen):]))
        stems.append(int(str(d)[:(-1*leaflen)]))
    return stems, leaves

def GenerateStemPlot(stems, leaves):
    plt.title('Stem and Leaf Plot')
    plt.xlabel('Stems')
    plt.ylabel('Leaves')
    markerline, stemlines, baseline = plt.stem(stems, leaves)
    plt.show()

def DensityPlot(X, labels):
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

def RugPlot(X, labels):
    for x, label in zip(X, labels):
        sns.rugplot(x, label=label)
    plt.title('Rug Plot')
    plt.xlabel('Days')
    plt.ylabel('Consumption')
    plt.show()

def Scatterplot(X, Y):
    plt.scatter(X, Y)
    plt.title('Scatter Plot')
    plt.xlabel('Mass')
    plt.ylabel('Litres')
    plt.show()

def BoxPlot(X, title='', xlabel='', ylabel=''):
    plt.boxplot(X)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def SwarmPlot(X, title='', xlabel='', ylabel=''):
    sns.swarmplot(X)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def JitteredBoxPlot(X, title='', xlabel='', ylabel=''):
    sns.boxplot(data=X)
    sns.swarmplot(data=X, color='grey')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def ViolinPlot(X, title=''):
    plt.violinplot(X)
    plt.title(title)
    plt.show()

def RadarPlot(name, statsList, attribute_labels, plot_markers, plot_str_markers):

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

def RadarPlot_PlotLY(statsList, labels):
    for stats in statsList:
        df = pd.DataFrame(dict(r=stats, theta=labels))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.show()

def FunnelPlot(X, labels):
    data = dict(number=X, stage=labels)
    fig = px.funnel(data, x='number', y='stage')
    fig.show()


# Custom Functions
def GenerateMarks_1(n_students, rollno_prefix):
    marks = []
    rollnos = []
    for i in range(n_students):
        zero_prefix = '0' * (len(str(n_students)) - len(str(i)))
        rollno = rollno_prefix + zero_prefix + str(i)
        mark = 0
        if i % 2 == 0:
            mark = 25 + ((i + 8) % 10)
        else:
            mark = 25 + ((i + 7) % 10)
        marks.append(mark)
        rollnos.append(rollno)
    return marks, rollnos

def GenerateMarks_2(n_data, rand=True):
    MidSemMarks = []
    EndSemMarks = []
    AssignmentMarks = []
    for i in range(n_data):
        if rand:
            MidSemMarks.append(random.randint(0, 30))
            EndSemMarks.append(random.randint(0, 50))
            AssignmentMarks.append(random.randint(0, 20))
        else:
            MidSemMarks.append(int(input("Enter Midsem Marks for " + str(i+1) + ": ")))
            EndSemMarks.append(int(input("Enter Endsem Marks for " + str(i+1) + ": ")))
            AssignmentMarks.append(int(input("Enter Assignment Marks for " + str(i+1) + ": ")))
    return MidSemMarks, EndSemMarks, AssignmentMarks

def CalculateTotalMarks(MidSemMarks, EndSemMarks, AssignmentMarks):
    TotalMarks = []
    for midsem, endsem, assign in zip(MidSemMarks, EndSemMarks, AssignmentMarks):
        TotalMarks.append(midsem + endsem + assign)
    return TotalMarks

def GetGrade(mark, avgmarks):
    grade = 'U'
    if mark >= 90:
        grade = 'S'
    elif mark >= 80:
        grade = 'A'
    elif mark >= 70:
        grade = 'B'
    elif mark >= 60:
        grade = 'C'
    elif mark >= 50:
        grade = 'D'
    elif mark >= int(avgmarks / 2):
        grade = 'E'
    else:
        grade = 'U'
    return grade

def CalculateGrades(TotalMarks):
    Grades = []
    avgmarks = Mean(TotalMarks)
    for totmark in TotalMarks:
        Grades.append(GetGrade(totmark, avgmarks))
    return Grades