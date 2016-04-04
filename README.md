# Target-scan-obdelava
Obdelava target scan podatkov (Summary_counts.txt) za potrebe cytoscape

###summary_counts_mod.py
Prebere summary_counts.txt datoteko ter ustvari datoteko summary_counts_mod.txt kjer je delimitier ";" med posameznimi elementi

###parser_compare_create.py
Prebere miRNA_HOS_etc...cvs datoteko, ustvari dict. key:value (miRNA:nCounts), pregleda summary_counts_mod.txt, izpiše vse vrstice 
  kjer je miRNA v summary_counts_mod.txt in miRNA_HOS_...cvs enaka (s pogojem da species = "9606")

Ustvari datoteko z vrsticami cytoscape.txt kjer so columni v Target gene; miRNA; nCounts; Cumulative weighted context++ score

###Create_CVS.py
Prebere miRNA_HOS_etc...cvs in ustvari miRNA_HOS_...output.cvs s prečiščenim besedilom. Ustvari nam osnovni CVS za obdelavo v R
