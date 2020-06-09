library("readxl")
library(stringr)
library(ggplot2)

results_path <- paste(source,"/results/", sep = "", collapse = NULL)

'--- Read table of numerical ---'
source <- getwd()
path <- paste(source,"/results/data/spotify_numerical_features_only.csv", sep = "", collapse = NULL)
data <- read.csv(path)
'--- Read table of numerical ---'

"SIMPLE PLOT Popularity AND Acoustiness"
png(filename=paste(results_path,"POPULARITY_x_ACOUSTICNESS.png",sep = "", collapse = NULL)
)
plot_var <- plot(data$acousticness, data$popularity, 
                 main= "Popularity x Acousticness",
                 xlab= "Acousticness",
                 ylab= "Popularity",
                 col= "blue", pch = 19, cex = 0.4, lty = "solid", lwd = 2)
dev.off()
"SIMPLE PLOT Popularity AND Acoustiness"
