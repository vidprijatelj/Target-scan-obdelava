import os

os.chdir(r"C:\Users\Vid-PC\Desktop\Diploma")
#spremenimo direktorij kjer imamo shranjeno datoteko
filename1 = "Summary_Counts.txt"
filename2 = "Summary_Counts_mod.txt"

i = 1
#naredimo za potrebe pregledovanja, ali smo v prvi vrstici tekstovne datoteke

with open(filename1) as f1, open(filename2, 'w') as f2:
    #odpremo izvirno datoteko f1 in novo datoteko, v katero bomo zapisovali

    for line in f1:
        if i != 1:
            #če nismo v prvi vrstici, tekst obdelamo
            #spremenimo vrstico v listo elementov
            paragraph = line.split()
            paragraph = ";".join(paragraph)
            #listo elementov nato pretvorimo v string, kjer so elementi ločeni z ";"
            f2.write(paragraph + "\n")
            #zapišemo vrstico v novo daotetko
            i += 1
        else:
            f2.write(line) #na koncu ni potreben "\n", verjetno zato ker smo pustili v original obliki
            i += 1
