import os  # rabili bomo za spremembo dira
import csv  # rabili bomo za read normaliziranih vrednosti 172_0

os.chdir(r"C:\Users\Vid-PC\Desktop\Diploma")  # spremenimo dir v working dir

filename1 = "Summary_Counts_mod.txt"  # odpremo modificirano targetscan datoteko
filename2 = "miRNA_HOS_doktorat_vseh 16_normalized_SORT_1720.csv"  # odpremo normalizirane vrednosti 172_0
filename3 = "cytoscape.txt"  # datoteka v katero bomo zapisali rezultate

dictionary = {} # ustvarimo dict za potrebe hitrega pregledovanja čez naše rezultate t.j. miRNA_HOS_doct etc

with open(filename2, 'r') as miRNA_HOS:

    miRNA_HOS_read = csv.reader(miRNA_HOS, delimiter=";") # določimo lastnosti .csv datoteke
    next(miRNA_HOS_read) # preskočimo prvo vrstico/header normaliziranih vrednosti

    for row in miRNA_HOS_read: # parsing naših rezultatov
        dictionary[row[0]] = row[6] # definiramo dictionary key:value = miRNA:ncounts


with open(filename1, 'r') as target_scan, open(filename3, 'w') as results:

    target_scan.readline()  # preskočimo prvo vrstico/header targetscan datoteke
    results.write("Target gene;miRNA;nCounts;Cumulative weighted context++ score" + "\n")  # napišemo prvo vrstico

    for line in target_scan:  # parsing target scan seznama

        paragraph_target_scan = line.split(";")  # naredimo tuple elementov vrstice target scan datoteke
        human_species = paragraph_target_scan[3] # definiramo pozicijo species v tuple vrstice target scan datoteke
        miRNA = paragraph_target_scan[13] # definiramo pozicijo miRNA  v tuple vrstice target scan datoteke

        if human_species == "9606" and miRNA in dictionary:  # naša pogoja
            # če obstaja miRNA (v tuple vrstice) kot key v dictionaryju, nadaljujemo -- hash!

            gene_name = paragraph_target_scan[1]  # pozicija gena v tuple vrstice target scan datoteke
            cum_context_score = paragraph_target_scan[15]  # cumulative weighted context++ score v tuple vrstice

            results.write(gene_name + ";" + miRNA + ";" + dictionary[miRNA] + ";" + cum_context_score + "\n")
            # zapišemo gen, miRNA, value keya(miRNA) v dictionaryju t.j. ncounts, cum.context score
