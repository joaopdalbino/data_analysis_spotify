library("readxl")
library(stringr)
library(ggplot2)

source <- getwd()
results_path <- paste(source,"/results/", sep = "", collapse = NULL)
path <- paste(source,"/data/timelines.csv", sep = "", collapse = NULL)

data <- read.csv(path)

data$X...date <- as.Date(data$X...date , format = "%Y-%m-%d")
data <- data[data$X...date > "2020-05-01",]

"SIMPLE PLOT STREAMS AND DATE"
png(filename=paste(results_path,"SIMPLE_PLOT_STREAMS_AND_DATE.png",sep = "", collapse = NULL)
)
plot_var <- plot(data$X...date, data$streams, 
                main= "Streams",
                xlab= "Date",
                ylab= "Streams",
                col= "blue", pch = 19, cex = 0.4, lty = "solid", lwd = 2)
plot_var <- text(data$X...date, data$streams, labels=data$streams, cex= 0.5, pos=1)
dev.off()
"SIMPLE PLOT STREAMS AND DATE"

"SIMPLE PLOT LISTENERS AND DATE"
png(filename=paste(results_path,"SIMPLE_PLOT_LISTENERS_AND_DATE.png",sep = "", collapse = NULL)
)
plot_var <- plot(data$X...date, data$listeners, 
                 main= "Listeners",
                 xlab= "Date",
                 ylab= "Listeners",
                 col= "blue", pch = 19, cex = 0.4, lty = "solid", lwd = 2)
plot_var <- text(data$X...date, data$listeners, labels=data$listeners, cex= 0.5, pos=1)
dev.off()
"SIMPLE PLOT LISTENERS AND DATE"

"SIMPLE PLOT FOLLOWRERS AND DATE"
png(filename=paste(results_path,"SIMPLE_PLOT_FOLLOWERS_AND_DATE.png",sep = "", collapse = NULL)
)
plot_var <- plot(data$X...date, data$followers, 
                 main= "Followers",
                 xlab= "Date",
                 ylab= "Followers",
                 col= "blue", pch = 19, cex = 0.4, lty = "solid", lwd = 2)
plot_var <- text(data$X...date, data$followers, labels=data$followers, cex= 0.5, pos=1)
dev.off()
"SIMPLE PLOT FOLLOWRERS AND DATE"

"PLOT FOLLOWRERS AND LISTENERS"
png(filename=paste(results_path,"PLOT_FOLLOWERS_AND_LISTENERS.png",sep = "", collapse = NULL)
)
plot_var <- plot(data$followers, data$listeners, 
                 main= "Listeners x Followers",
                 xlab= "Followers",
                 ylab= "Listeners",
                 col= "blue", pch = 19, cex = 0.4, lty = "solid", lwd = 2)
plot_var <- text(data$followers, data$listeners, labels=data$listeners, cex= 0.5, pos=1)
dev.off()
"PLOT FOLLOWRERS AND DATE"

"PLOT STREAMS AND LISTENERS"
png(filename=paste(results_path,"PLOT_STREAMS_AND_LISTENERS.png",sep = "", collapse = NULL)
)
plot_var <- plot(data$listeners, data$streams, 
                 main= "Listeners x Streams",
                 xlab= "Listeners",
                 ylab= "Streams",
                 col= "blue", pch = 19, cex = 0.4, lty = "solid", lwd = 2)
plot_var <- text(data$listeners, data$streams, labels=data$streams, cex= 0.5, pos=1)
dev.off()
"PLOT FOLLOWRERS AND DATE"
