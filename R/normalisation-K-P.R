require(dplyr)
require(reshape2)
require(ggplot2)
library(psych)

source("http://bioconductor.org/biocLite.R")
biocLite("preprocessCore")

library("preprocessCore")

# load data
data<-read.csv("data.csv")
data<-select(data,-Annotation,-Probe.Name)

# convert to molten table
data.melt<-melt(data,id.vars=c("Gene.name","Accession.No.","Class.Name"),value.name = "counts",variable.name="sample")
data.melt<-mutate(data.melt,sample=sub("X",data.melt$sample,replacement=""))
data.melt<-data.melt %>% filter(Class.Name=="Endogenous") # Remove non-Endogenous 

# remove outliers or errors
d1<-data.melt %>%
  group_by(Gene.name) %>%
  filter(sd(counts)!=0)

# normalisation to reference genes
d1<-d1 %>%
  group_by(sample) %>%
  #filter(Class.name=="SpikeIn" & Gene.name %in% c("ath-miR159a","cel-miR-248")) %>%
  filter(Class.Name=="Endogenous") %>%
  top_n(n=100, wt=counts) %>%
  # geometricna sredina
  summarise(factor=exp(mean(log(counts)))) %>%
  mutate(factor=mean(factor)/factor) %>%
  inner_join(d1) %>%
  mutate(normalised=counts*factor)

# RMA method for bg correction, used in microarrays
d11<-acast(d1,Gene.name~sample,value.var="normalised")
d12<-rma.background.correct(d11)
rownames(d12)<-rownames(d11)
colnames(d12)<-colnames(d11)
d13<-melt(d12)
names(d13)<-c("Gene.name","sample","bgcor")
d13$sample<-as.factor(d13$sample)

d2<-inner_join(d1,d13)

# Create Wide-Format data
casted <- dcast(d2, Gene.name + Accession.No. + Class.Name ~ sample, value.var = "bgcor")

# Column pos. 8 = 124.K, column pos. 9 = 124.P
KinP_24 <- select(casted, Gene.name, 8, 9)
KinP_24$"Difference 124K - 124P" <- round(abs(KinP_24$'124.K' - KinP_24$'124.P'), digits = 5)

# Column pos. 16 = 172.K, column pos. 17 = 172.P
KinP_72 <- select(casted, Gene.name, 16, 17)
KinP_72$"Difference 172K - 172P" <- round(abs(KinP_72$'172.K' - KinP_72$'172.P'), digits = 5)

#Column pos. 8 = 124.K, column pos. 10 = 124.PE
KinPE_24 <- select(casted, Gene.name, 8, 10)
KinPE_24$"Difference 124K - 124PE" <- round(abs(KinPE_24$'124.K' - KinPE_24$'124.PE'), digits = 5)

#Column pos. 16 = 172.K, column pos. 18 = 172.PE
KinPE_72 <- select(casted, Gene.name, 16, 18)
KinPE_72$"Difference 172K - 172PE" <- round(abs(KinPE_72$'172.K' - KinPE_72$'172.PE'), digits = 5)

final <- inner_join(KinP_24, KinP_72)
final <- inner_join(final, KinPE_24)
final <- inner_join(final, KinPE_72)

# Rearrange for better coherence
final <- final[c(1, 2, 3, 8, 5, 6, 10, 4, 7, 9, 11)]

# add fold change
# The value is negative when the "P" or "PE" value is smaller than the ""initial"" "K" value
final$"Fold ch. 124K -> 124P" <- (final$`124.P` - final$`124.K`) / final$`124.K`
final$"Fold ch. 172K -> 172P" <- (final$`172.P` - final$`172.K`) / final$`172.K`
final$"Fold ch. 124K -> 124PE" <- (final$`124.PE` - final$`124.K`) / final$`124.K`
final$"Fold ch. 172K -> 172PE" <- (final$`172.PE` - final$`172.K`) / final$`172.K`

# Write data
write.csv(final, file="final.csv")
