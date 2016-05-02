# Target-scan-obdelava
Obdelava target scan podatkov (Summary_counts.txt) za potrebe cytoscape  
  
  
---
##R folder
Dodan .R in kot njegov rezultat .csv geometrične normalizacije z razlikami in fold changeom  
-> 124K - 124P  
-> 172K - 172P  
-> 124K - 124PE  
-> 172K - 172PE  
  
  
---
##Cytoscape datoteke folder
Vsi filei relevantni za cytoscape
Dodani exporti grafik najdenih z BinGO  
  
  
---
###summary_counts_mod.py
Prebere summary_counts.txt datoteko ter ustvari datoteko summary_counts_mod.txt kjer je delimitier ";" med posameznimi elementi

###parser_compare_create.py
Prebere miRNA_HOS_etc...cvs datoteko, ustvari dict. key:value (miRNA:nCounts), pregleda summary_counts_mod.txt, izpiše vse vrstice 
  kjer je miRNA v summary_counts_mod.txt in miRNA_HOS_...cvs enaka (s pogojem da species = "9606")

Ustvari datoteko z vrsticami cytoscape.txt kjer so columni v Target gene; miRNA; nCounts; Cumulative weighted context++ score

###Create_CVS.py
Prebere miRNA_HOS_etc...cvs in ustvari miRNA_HOS_...output.cvs s prečiščenim besedilom. Ustvari nam osnovni CVS za obdelavo v R

###miRNA-miRNA_connections.py
Pregleda .cvs (V tem primeru  cytoscape_bam.cvs), na koncu .cvs doda miRNA pare, ki vplivajo na iste gene.

"Target gene" || "miRNA"

"miRNA-ime" || "miRNA-ime"


Dodano za potrebe clusterjev.
Pri uvozu v cytoscape nujno odstraniti edge duplications.
