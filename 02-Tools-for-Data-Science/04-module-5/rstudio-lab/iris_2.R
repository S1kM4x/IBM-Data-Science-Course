library(datasets)
data(iris)

View(iris)

library(GGally)
ggpairs(iris, mapping=ggplot2::aes(colour = Species))
