library("readxl")
library(stringr)
library(ggplot2)
library(corrplot)

'--- Read table of numerical ---'
source <- getwd()
path <- paste(source,"/data/SpotifyFeatures_normalized_data.csv", sep = "", collapse = NULL)
data <- read.csv(path)
q <- quantile(data$popularity)
data <- data[data$popularity >= q[4],]


path_to_save_imgs <- paste(source,"/results/exploratory_data/", sep = "", collapse = NULL)
'--- Read table of numerical ---'

'--- MEAN POPULARITY BY KEY ---'
mean <- aggregate(popularity ~ key, data, mean)
colnames(mean) <- c("key", "mean")
mean[,'mean']=round(mean[,'mean'],2)
count <- aggregate(popularity ~ key, data, FUN = length)
colnames(count) <- c("key", "qtd")
key <- merge(mean, count, by = "key")
g <- ggplot(data=key, aes(x=key, y=mean, fill=key)) +
  geom_bar(stat="identity") +
  geom_text(aes(label=mean), position=position_dodge(width=0.2), angle=-90)
ggsave(paste(path_to_save_imgs,"mean_popularity_by_key.png"))
dev.off()
'--- MEAN POPULARITY BY KEY ---'

'--- QUANTITY POPULARITY BY KEY ---'
g <- ggplot(data=key, aes(x=key, y=qtd, group=1)) +
  geom_line() +
  geom_text(aes(label=qtd), position=position_dodge(width=0.5), vjust=-0.25)
ggsave(paste(path_to_save_imgs,"quantity_by_key.png"))
dev.off()
'--- QUANTITY POPULARITY BY KEY ---'



'--- MEDIAN POPULARITY BY KEY ---'
median <- aggregate(popularity ~ key, data, median)
colnames(median) <- c("key", "median")
median[,'median']=round(median[,'median'],2)

g <- ggplot(data=median, aes(x=key, y=median, fill=key)) +
  geom_bar(stat="identity") +
  geom_text(aes(label=median), position=position_dodge(width=0.2), angle=-90)

ggsave(paste(path_to_save_imgs,"median_popularity_by_key.png"))
dev.off()
'--- MEAN POPULARITY BY KEY ---'

'--- DENSITY OF FEATURES ---'
pdf(paste(path_to_save_imgs,"Features Density_q_4.pdf"))
par(mfrow=c(1,3))
for(i in 4:length(data)) {
  plot(density(data[,i]), main=names(data)[i])
}
dev.off()
'--- DENSITY OF FEATURES ---'

'--- FEATURES CORRELATIONS ---'
jpeg(paste(path_to_save_imgs,"Correlations_4.jpg"), width = 1000, height = 1000)
correlations <- cor(data[,4:length(data)])
corrplot(correlations, method="circle")
dev.off()
'--- FEATURES CORRELATIONS ---'

'--- FEATURES CORRELATIONS ---'
jpeg(paste(path_to_save_imgs,"Pairs_1_q_4.jpg"), width = 1000, height = 1000)
pairs(data[,4:8])
dev.off()
jpeg(paste(path_to_save_imgs,"Pairs_2_q_4.jpg"), width = 1000, height = 1000)
pairs(data[,9:14])
dev.off()
'--- FEATURES CORRELATIONS ---'