import numpy as np
import pandas as pd

data = 0


def open_file():
    global data
    # definiramo globalen scope spremenljivke data

    excel_file = pd.ExcelFile(r"C:\Users\Vid-PC\Documents\GitHub\Target-Scan-obdelava\miRNA_HOS_doktorat_vseh 16.xlsx")
    data = excel_file.parse(excel_file.sheet_names[1])
    # Odpremo excel file in naredimo datasheet <-> parsiramo normalizirane vrednosti


def is_outlier(array, threshold=3.5):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.
    """
    median = np.median(array)
    # pregledamo mediano elementov
    diff = np.abs(array - median)
    # definiramo nov array v katerega zapišemo absolutne vrednosti razlik med elementom in mediano
    med_abs_deviation = np.median(diff)
    # definiramo mediano absolutnih vrednosti razlik med elementi in mediano

    modified_z_score = 0.6745 * diff / med_abs_deviation
    # formula Z vrednosti za vse M.A.D.
    # 1 / 1.4826; sigma ~ 1.4826 * MAD -> MAD = sigma / 1.4826 -> MAD = sigma * 1 / 1.4826 = sigma * 0.6745
    # definiran je nov array

    i = 0
    a = []
    for x in array:
        if modified_z_score[i] > threshold:
            a.append( (i, modified_z_score[i], x))
        i += 1
    return a
    # pregledujemo array modificiranih Z vrednost kjer je vrednost večja od 3.5
        # pri Z vrednosti > 3.5 smo padli izven 99.5+% vrednosti populacije ergo je outlier
    # vrne nam pozicijo ncounts, modified_z_score za ta ncounts in sam ncounts

open_file()

"""TESTIRANJE PANDAS METOD

print (data.iat[0,0])
#začetek ime prve miR
#Odpremo skalar v row=0 in column=0

print (data.iat[799,0])
#konec ime zadnje miR
#Odpremo skalar v row=799 in column=0

print (list(data.columns.values)[36])
#list data columns values -> vrne nam imena kolon v obliki arraya, specifično ime 36. kolone
#izpusti [] za imena vseh kolon

columns = data.shape[1]
print (columns)
#data.shape[0] = število vrstic
#data.shape[1] = število kolon"""

matrix = np.zeros(17)
# potrebno definirati array axis=1 (horizontalno)
# da je dimenzije 17
# variabla s katero bomo primarno delali

for y in range(0, 800):
    # gremo čez vse miR kot vrstice

    p = []
    p.append(data.iat[y, 0])
    # pozicija 0 začasnega arraya, ime miR

    array = []
    # paralelen array za potrebe pregleda outlierjev

    for x in range(6, 38, 2):
        # skačemo po 2 koloni naenkrat pri norm. vrednostih, vzamemo samo norm. vrednosti

        if data.iat[y, x] > 0:
            p.append(data.iat[y, x])
            array.append(data.iat[y, x])
            # če je vrednost večja od 0, dodamo vrednost v array
        else:
            p.append(0)
            # če je vrednost manjša od 0, zapišemo 0; ne more ostati prazna vrednost
            # saj izgubimo informacijo o specifični cel. liniji

    if array == []:
        array = [0]
    # pregledovanje MAD -> če je array prazen nam vrže error povezan z NaN!

    matrix = np.row_stack((matrix, p))
    # dodamo začasni array v 2d matrix array, za potrebe zapisovanja

    print(is_outlier(array))

    """TO-DO: pregled mediane vseh začasnih arrayev, poišči vse outlierje
    ali so ti outlierji pomembni?
    kako se bo porihtalo, da vrednosti 0 niso pomembne za našo mediano t.j.
    ne vplivajo nanjo"""

# print(matrix)
