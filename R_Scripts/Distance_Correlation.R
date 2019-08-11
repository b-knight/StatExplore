x         <- c(0, 1, 2, 3, 4) 
y         <- c(2, 1, 0, 1, 2) 

x_mat     <- dist(x, method = "euclidean", diag = TRUE, upper = TRUE, p = 2)
y_mat     <- dist(y, method = "euclidean", diag = TRUE, upper = TRUE, p = 2)

take_doubly_centered_distances <- function(x_mat) {
library(reshape2)
x_df               <- melt(as.matrix(x_mat), 
                      varnames = c("row", "col"))

x_row_means        <- aggregate(x_df, list(x_df$row), mean)
x_row_means        <- subset(x_row_means, select = -c(Group.1, col))
names(x_row_means) <- c("row", "row_mean")
x_df               <- merge(x=x_df, y=x_row_means, by="row")

x_col_means        <- aggregate(x_df, list(x_df$col), mean)
x_col_means        <- subset(x_col_means, select = 
                           -c(Group.1, row, row_mean))
names(x_col_means) <- c("col", "col_mean")
x_df               <- merge(x=x_df, y=x_col_means, by="col")

x_df$grand_mean    <- mean(c(x_row_means$row_mean, 
                           x_col_means$col_mean)) 
x_df$X             <- x_df$value - x_df$row_mean - 
                      x_df$col_mean + x_df$grand_mean 
return(x_df)
}

x_dist <- take_doubly_centered_distances(x_mat)
y_dist <- take_doubly_centered_distances(y_mat)




