from unicodedata import decimal


def line(p1, p2, x):
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    y = m* (p2[0] - x) - p2[1]
    return - y

def curve_chopper(curve, N = 50):
    xline = []
    yline = []
    n = 1
    x1 = curve[0][0]
    x2 = curve[0][1]
    y1 = curve[1][0]
    y2 = curve[1][1]
    
    #slope = line((x1,y1), (x2,y2))

    for x in range(N + 1):
        xstep = x / N
        if(xstep > x2):
            n +=1
            x1 = x2
            y1 = y2
            x2 = curve[0][n]
            y2 = curve[1][n]
            #slope = line((x1,y1), (x2,y2))

        xline.append(xstep)
        yline.append(line((x1,y1), (x2,y2), xstep))

    return (xline,yline)

def normalize_curve(ycurve, xcurve = []):
    maxy = max(ycurve)

    if(maxy == 0 and abs(min(ycurve)) == 0):
        maxy = 1
    elif (maxy < abs(min(ycurve))):
        maxy = abs(min(ycurve))

    if (len(ycurve) != len(xcurve)):
        maxx = len(ycurve) -1
        xcurve = [*range(maxx)]
        print("fart")
    else:
        maxx = max(xcurve)
    if (maxx == 0):
        maxx = 1
    x = []
    y = []
    n = 0
    for point in ycurve:
        y.append(point/maxy)
        x.append(xcurve[n]/maxx)
        n+=1
    return x,y

def standardize_curve(xcurve, ycurve, N = 50):
    return curve_chopper((normalize_curve(ycurve, xcurve)), N)

def curve_comparer(curve1, curve2, N = 50):
    sc1 = standardize_curve(curve1[0],curve1[1], N)
    sc2 = standardize_curve(curve2[0],curve2[1], N)
    result = 0
    for y in range(N + 1):
        result += abs(sc1[1][y] - sc2[1][y])

    return result/N

#test
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import copy

testcurve1 = ([0,1,2,3,4,5,6],[0,1,2,3,4,5,0])
testcurve2 = ([0,1],[0,-2])
print(curve_comparer(testcurve1,testcurve2))



testcurve2 = ([0,1,2,3,4,5,6,7,8,9,10,11,12],[0,1,2,3,4,5,6,7,8,9,10,5,0])
testcurve3 = ([0,1,2,3,4,5,6],[0,2,4,6,8,10,0])
print(curve_comparer(testcurve1,testcurve3))


#all sorts of excess
curvay = standardize_curve([0, 1, 2, 3, 4.25, 4.75, 5.25, 5.75, 6.75, 8], [0, 0.25, 1, 2.25, 3, 2, 1.5, 2, 3.5, 0])
testcurve = standardize_curve([0,1,2,3,4],[0,1,2,3,0])
testcurve1 = standardize_curve(testcurve[0], testcurve[1])
testcurve2 = standardize_curve(testcurve1[0], testcurve1[1])
print(curve_comparer(testcurve,testcurve2))
#print(curvay)
df = pd.DataFrame({'x': curvay[0], 'y': curvay[1]})
tdf = pd.DataFrame({'x': testcurve[0], 'y': testcurve[1]})

plt.xlim([0, 1.1]) 
plt.ylim([0, 1.1])


#curbs = curvesplitterliser(curvay)
#print(curbs)
#create scatterplot
polyline = np.linspace(0, 1, 50)
#plt.scatter(df.x, df.y)
plt.plot(tdf.x,tdf.y)
plt.plot(df.x, df.y, "red")

chopped = curve_chopper(testcurve)

dfp = pd.DataFrame({'x': chopped[0], 'y': chopped[1]})

chopped = curve_chopper(curvay)

plt.scatter(dfp.x,dfp.y)
plt.scatter(chopped[0],chopped[1])
plt.scatter(testcurve2[0],testcurve2[1])
#model1 = (df.x, df.y, 1)
model2 = np.poly1d(np.polyfit(df.x, df.y, 2))
model3 = np.poly1d(np.polyfit(df.x, df.y, 3))
model4 = np.poly1d(np.polyfit(df.x, df.y, 4))
model5 = np.poly1d(np.polyfit(df.x, df.y, 5))
model6 = np.poly1d(np.polyfit(df.x, df.y, 6))
model7 = np.poly1d(np.polyfit(df.x, df.y, 7))
model8 = np.poly1d(np.polyfit(df.x, df.y, 8))



for c in curbs:
    print(c)
    pf = pd.DataFrame({'x': c[0], 'y': c[1]})

    model = np.poly1d(np.polyfit(pf.x,pf.y, 4))
    plt.plot(polyline, model(polyline))

plt.show()
#add fitted polynomial lines to scatterplot 
plt.plot(polyline, model1(polyline), color='green')
plt.plot(polyline, model2(polyline), color='red')
plt.plot(polyline, model3(polyline), color='purple')
plt.plot(polyline, model5(polyline), color='orange')
plt.plot(polyline, model4(polyline), color='blue')
"""
"""
plt.plot(polyline, model6(polyline), color='red')
plt.plot(polyline, model7(polyline), color='black')
plt.plot(polyline, model8(polyline), color='green')
plt.show()


curvsy = numpy.polyfit(curvay[0],curvay[1], 5)
#curv = scipy.optimize.curve_fit(f, curvay[0], curvay[1], (0,0,0,0,0), sigma=sigma)
#curv = scipy.optimize.curve_fit(f, curvay[0], curvay[1], (0,0,0,0,0))
ylist1 = numpy.polyval(curvsy,xlist)
#plt.plot(xlist,f(xlist,*curv))
plt.plot(xlist,ylist1)


def curvesplitterliser(curve):
    n = 0
    k = 0
    other = False
    acsending = True
    result = []
    tempUp = ([],[])
    tempDown = ([],[])
    for point in curve[1]:
        if (point < n and acsending):
            acsending = False
            if (other):
                lah = copy.deepcopy(tempDown)
                result.append(lah)
            tempDown = ([],[])
            other = True
        
        if (point > n and acsending == False or (other and point <= 0 and k == len(curve[1]) -1)):
            if (other and point <= 0 and k == len(curve[1]) -1):
                tempUp[0].append(curve[0][k])
                tempUp[1].append(point)

            acsending = True
            lah = copy.deepcopy(tempUp)
            result.append(lah)
            tempUp = ([],[])

        tempUp[0].append(curve[0][k])
        tempUp[1].append(point)
        tempDown[0].append(curve[0][k])
        tempDown[1].append(point)
        k += 1
        n = point

    return result

def curvesplitterliser(curve):
    n = 0
    k = 0
    other = False
    acsending = True
    result = []
    tempUp = ([],[])
    tempDown = ([],[])
    for point in curve[1]:
        if (point < n and acsending):
            acsending = False
            if (other):
                lah = copy.deepcopy(tempDown)
                result.append(lah)
            tempDown = ([tempDown[0][len(tempDown[0]) -1]],[tempDown[1][len(tempDown[1]) -1]])
            other = True
        
        if (point > n and acsending == False or (other and point <= 0 and k == len(curve[1]) -1)):
            if (other and point <= 0 and k == len(curve[1]) -1):
                tempUp[0].append(curve[0][k])
                tempUp[1].append(point)

            acsending = True
            lah = copy.deepcopy(tempUp)
            result.append(lah)
            tempUp = ([tempUp[0][len(tempUp[0]) -1]],[tempUp[1][len(tempUp[1]) -1]])

        tempUp[0].append(curve[0][k])
        tempUp[1].append(point)
        tempDown[0].append(curve[0][k])
        tempDown[1].append(point)
        k += 1
        n = point

    return result

"""