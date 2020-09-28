library(ggplot2)

'--- Read table of numerical ---'
source <- getwd()
path <- paste(source,"/results/linear regression/data/forward_stepwise_selection_models_and_indicators.csv", sep = "", collapse = NULL)
data <- read.csv(path)
path_to_save_imgs <- paste(source,"/results/linear regression/imgs/", sep = "", collapse = NULL)
'--- Read table of numerical ---'

data$n_features <- seq.int(nrow(data))

'--- Generate PDF ---'
pdf(paste(path_to_save_imgs,"Linear Regression Indicators.pdf"))
par(mfrow=c(1,3))
for(i in 3:(length(data)-1)) {
  plot(data$n_features, data[,i], main=names(data)[i], xlab="Number variables", ylab=(colnames(data)[i]))
}
dev.off()
'--- Generate PDF ---'
