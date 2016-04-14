import os #rabimo za dir
import pandas as pd

os.chdir(r"C:\Users\Vid-PC\Desktop") #kjer se nahaja naš file

df = pd.read_csv("cytoscape_bam.csv", sep=";")
#df.dropna(how="all")


dictionary = {} #usvarimo dictionary; naši keyi bodo imena miRNA, value bodo liste genov

miRNA_list = list(df.miRNA.unique()) #ustvarimo listo unikatnih miRNA

for miRNA in miRNA_list:
    dictionary[miRNA] = list(df[df["miRNA"] == miRNA]["Target gene"])
    #value(miRNA) = lista vseh genov, na katere vpliva miRNA


"""
    Zanka - iterate čez vse keye našega dictionaryja
    Za vsak key iteriramo čez vse vrednosti tega keya
    Za vsako vrednost iteriramo čez vse keye našega dictionaryja, s tem da
        v tej drugi iteraciji pregledujemo, če se iskan value pojavi še v kakem
        drugem keyu
    Problem - dobimo dvojne vnose. Če je value x v keyih a in b, bomo dobili dvojice
        a-b in b-a
    Rešitev: cytoscape -> ignore duplicate edges
    Dirty programiranje
"""
for key in dictionary:
    for value in dictionary[key]:
        for key2 in dictionary:
            if (value in dictionary[key]) & (value in dictionary[key2]) & (key != key2):
                #print(d,"-",d1)
                df_add = pd.Series([key, key2, None, None], index=["Target gene", "miRNA", "nCounts",
                                                                   "Cumulative weighted context++ score"])
                result = df.append(df_add, ignore_index=True)
                df = result

print(df)
df.to_csv("test.csv", sep=";", index=False)