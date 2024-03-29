## Distance Correlation
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; In statistics, the Pearson product-moment correlation coefficient (or simply "the correlation coefficient") is a standard measure of the extent *and direction* to which two variables move together. Ranging from [-1,1] where 1 implies perfect correlation and -1 implies perfect inverse correlation, this statistic encapsulates the ratio between two variables' covariance (the numerator) and the product of their variances (the denominator).

<div align="center">
<img 
src="https://github.com/b-knight/StatExplore/blob/master/images/Pearsons_Correlation_Coefficient.gif?sanitize=true", 
align="middle",
alt="Pearson Product-Moment Correlation Coefficient">
</div>
<p align="center"><sub><b>Equation 1: Pearson Product-Moment Correlation Coefficient</sub></b></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; An key assumption of this statistic is that the underlying relationship between these two statistics is *linear*. However, this assumption of linearity is often not borne out in reality. Imagine we are assessing the relationship between the amount of money spent on ads targeting visitors of a given website, and the rate of conversion from visitor to paying customer. We could easyily imagine a scenario where up to a certain point, more resources spent on ads tends to increase conversion. However, there may come a point where the prevalence of ads is so great that it is actually offputting to the consumer, accomplishing the opposite of its intended purpose. This scenario is not theoretical, but has been validated by [survey data](https://www.cmswire.com/cms/customer-experience/too-much-online-advertising-may-turn-consumers-off-survey-finds-014707.php, "Too Much Online Advertising May Turn Consumers Off, Survey Finds"). The implication is that while ad spend may relate intimately to conversion, the correlation coefficient between these two variables is likley to be small - to the point of approaching zero. <br>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The scatterplots below illustrate how, when the relationship between two variables involves a change in direction, the Pearson Product-Moment Correlation Coefficient fails to report the true degree of dependence between variables. 
<div align="center">
<img 
src="https://github.com/b-knight/StatExplore/blob/master/images/Correlation_Examples.png?sanitize=true", 
align="middle",
alt="Sets of Pearson Correlation Coefficients">
</div>
<p align="center"><sub><b>Image 1: Sets of Pearson Correlation Coefficients </b></sub></p>
<p align="center"><sub> SOURCE: https://commons.wikimedia.org/wiki/File:Correlation_examples2.svg </sub></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; In 2007, Gábor J. Székely called attention to this important limitation of the correlation coefficient and introduced the concept of 'distance correlation' as part of his conception of '[E-statistics](https://en.wikipedia.org/wiki/Energy_distance, "E-statistics")' - statistics concerning the energy distance between probability distributions. Within the framework of E-statistics, Székely re-formulated many classical statistical concepts, such as 'distance variance' versus variance, 'distance standard deviation' versus standard deviation, and 'distance covariance' versus covariance. Using these, the definition of correlation coefficient can be re-written, but in such a way that a value of zero occurs if, and only if the two variables are genuinely independent.

<div align="center">
<img 
src="https://github.com/b-knight/StatExplore/blob/master/images/Distance_Correlation.gif?sanitize=true", 
align="middle",
alt="Distance Correlation">
</div>
<p align="center"><sub><b>Equation 2: Distance Correlation</sub></b></p>





<div align="center">
<img src="https://github.com/b-knight/StatExplore/blob/master/images/Distance_Correlation_Examples.png?sanitize=true",
align="middle", 
alt="Sets of Distance Correlation Coefficients">
</div>
<p align="center"><sub><b>Image 2: Sets of Distance Correlation Coefficients</b></sub></p>
<p align="center"><sub> SOURCE: https://commons.wikimedia.org/wiki/File:Distance_Correlation_Examples.svg</sub></p>




#### Calculating the Distance Covariance 

<div align="center">
<img src="https://github.com/b-knight/StatExplore/blob/master/images/Pairwise_Distances.gif?sanitize=true",
align="middle", 
alt="Pairwise Distances">
</div>


For example, let's create some data using R:

```R
x = c(0, 1, 2, 3, 4) 
y = c(2, 1, 0, 1, 2) 
```

Next, we derive a matrix for each variable containing the [pairwise distances](https://en.wikipedia.org/wiki/Distance_matrix "Wikipedia: Pairwise Distances") for that variable. For the purposes of calculating the distance covariance, we use the [Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance "Wikipedia: Euclidean Distance"). If we were exploring two-dimensional observations (for example, on the Cartesian plane) the appropriate formulation of the Euclidean distance would be as follows: 

<br>
<div align="center">
<img src="https://github.com/b-knight/StatExplore/blob/master/images/Two_Dimensional_Euclidean_Distance.gif?sanitize=true",
align="middle", 
alt="Euclidean Distance: Two Dimensions">
</div>
<br>

However, in the example below *X* and *Y* are each univariate, and so the Euclidean distance reduces to the absolute value of the differences between observations. 

<br>
<div align="center">
<img src="https://github.com/b-knight/StatExplore/blob/master/images/Unidimensional_Euclidean_Distance.gif?sanitize=true",
align="middle", 
alt="Euclidean Distance: Unidimensional">
</div>
<br>

This can be done in R by calling the 'dist' method and specifying "euclidean" as the distance.
```R
x_mat <- dist(x, method = "euclidean", diag = TRUE, upper = TRUE, p = 2)
y_mat <- dist(y, method = "euclidean", diag = TRUE, upper = TRUE, p = 2)
```
We will also need the column and row means from these distance matrices, as well as the grand mean of those means. If you were to derive these manually, you might use a function like the following:
```
take_doubly_centered_distances <- function(x_mat) {
    library(reshape2)
    x_df               <- melt(as.matrix(x_mat), varnames = c("row", "col"))
    x_row_means        <- aggregate(x_df, list(x_df$row), mean)
    x_row_means        <- subset(x_row_means, select = -c(Group.1, col))
    names(x_row_means) <- c("row", "row_mean")
    x_df               <- merge(x=x_df, y=x_row_means, by="row")
    x_col_means        <- aggregate(x_df, list(x_df$col), mean)
    x_col_means        <- subset(x_col_means, select = -c(Group.1, row, row_mean))
    names(x_col_means) <- c("col", "col_mean")
    x_df               <- merge(x=x_df, y=x_col_means, by="col")
    x_df$grand_mean    <- mean(c(x_row_means$row_mean, x_col_means$col_mean)) 
    x_df$X             <- x_df$value - x_df$row_mean - x_df$col_mean + x_df$grand_mean 
    x_df = x_df[with(x_df, order(col, row)), ]
    myList <- list()
    for (i in unique(x_df[["col"]])){
      myList[[length(myList)+1]] <- x_df[x_df$col == i,]$X
    }
    output <- matrix(unlist(myList), ncol = length(unique(x_df[["col"]])), byrow = TRUE)
    return(output)
    }
```
..resulting in the following:
<table>
<tr><th> X Pair-Wise Distances </th><th> Y Pair-Wise Distances </th></tr>

<tr><td>

| X               | A  | B  | C  | D  | E  | Row<br>Mean         |
| --              | -- | -- | -- | -- | -- | ------------------- |
| A               | 0  | 1  | 2  | 3  | 4  | 2                   |
| B               | 1  | 0  | 1  | 2  | 3  | 1.4                 |
| C               | 2  | 1  | 0  | 1  | 2  | 1.2                 |
| D               | 3  | 2  | 1  | 0  | 1  | 1.4                 |
| E               | 4  | 3  | 2  | 1  | 0  | 2                   |
| Column<br>Mean  | 2  | 1.4|1.2 |1.4 | 2  | Grand<br>Mean = 1.6 |

</td><td>

| Y               | A    | B   | C  | D  | E   | Row<br>Mean          |
| --              | --   | --  | -- | -- | --  | -------------------- |
| A               | 0    | 1   | 2  | 1  | 0   | 0.8                  |
| B               | 1    | 0   | 1  | 0  | 1   | 0.6                  |
| C               | 2    | 1   | 0  | 1  | 2   | 1.2                  |
| D               | 1    | 0   | 1  | 0  | 1   | 0.6                  |
| E               | 0    | 1   | 2  | 1  | 0   | 0.8                  |
| Column<br>Mean  | 0.8  | 0.6 |1.2 |0.6 | 0.8 | Grand<br>Mean = 0.8  |

</td></tr> </table>
<p align="center"><sub><b>Tables 1 & 2: Pair-Wise Distances</b></sub></p>
We need to doubly center these distance matrices - doubly in this context means we will first subtract from each element its row mean, and secondly subtract its column mean before adding to each element the grand mean. 

<br>
<div align="center">
<img 
src="https://github.com/b-knight/StatExplore/blob/master/images/Doubly_Centered_Distances.gif?sanitize=true", 
align="middle",
alt="Doubly Centered Distances">
</div>
<br>

The resulting matrices should have all rows and all columns sum to zero.

<table>
<tr><th> X Doubly Centered Distances </th><th> Y Doubly Centered Distances </th></tr>

<tr><td>

| X                        | A    | B    | C    | D    | E    | <sub>Row<br>Sum</sub>   |
| ------------------------ | ---- | ---- | ---- | ---- | ---  | ----------------------- |
| A                        | -2.4 | -0.8 | 0.4  | 1.2  | 1.6  | 0                       |
| B                        | -0.8 | -1.2 | 0    | 0.8  | 1.2  | 0                       |
| C                        | 0.4  | 0    | -0.8 | 0    | 0.4  | 0                       |
| D                        | 1.2  | 0.8  | 0    | -1.2 | -0.8 | 0                       |
| E                        | 1.6  | 1.2  | 0.4  | -0.8 | -2.4 | 0                       |
| <sub>Column<br>Sum</sub> | 0    | 0    | 0    | 0    | 0    |                         |

</td><td>

| Y                        | A    | B    | C    | D    | E    | <sub>Row<br>Sum</sub>  |
| ------------------------ | ---- | ---- | ---- | ---- | ---- | ---------------------- |
| A                        | -0.8 | 0.4  | 0.8  | 0.4  | -0.8 | 0                      |
| B                        | 0.4  | -0.4 | 0    | -0.4 | 0.4  | 0                      |
| C                        | 0.8  | 0    | -1.6 | 0    | 0.8  | 0                      |
| D                        | 0.4  | -0.4 | 0    | -0.4 | 0.4  | 0                      |
| E                        | -0.8 | 0.4  | 0.8  | 0.4  | -0.8 | 0                      |
| <sub>Column<br>Sum</sub> | 0    | 0    | 0    | 0    | 0    |                        |

</td></tr> </table>
<p align="center"><sub><b>Tables 3 & 4: Distance Matrices After Doubly Centering</b></sub></p>

Next, we need to take the arithmetic average of the products of the doubly centered matrices. The summed products is also referred to as the [Frobenius inner product](https://en.wikipedia.org/wiki/Frobenius_inner_product, "Wikipedia: Frobenius Inner Product"), which we subsequently multiply times 1 over n squared to yield the arithmetic average.

<br>
<div align="center">
<img 
src="https://github.com/b-knight/StatExplore/blob/master/images/Squared_Sample_Distance_Covariance.gif?sanitize=true", 
align="middle",
alt="Squared Sample Distance Covariance">
</div>
<br>
<p align="center"><sub><b>Equation 3: Squared Sample Distance Covariance</sub></b></p>

We can manually do this in R via the 'matrixcalc' library. 
```R
arithmetic_average_of_products <- function(x_mat, y_mat) {
  library(matrixcalc)
  if ((nrow(x_mat) == nrow(y_mat)) & (ncol(x_mat) == ncol(y_mat))) {
    val <- frobenius.prod(x_mat, y_mat)
    return(val*(1/nrow(x_mat)^2))
  }
}
```
Finally, we take the square root of this result to get the sample distance covariance. If compare the results with R's ['energy' package](https://www.rdocumentation.org/packages/energy/versions/1.7-6/topics/distance%20correlation, "Energy"), we see that the results are the same:
``` R
> arithmetic_average_of_products(x_mat, y_mat)^(1/2)
    0.438178
> 
> library(energy)
> dcov.test(x, y, index = 1.0, R = NULL)

	Specify the number of replicates R (R > 0) for an independence test

data:  index 1, replicates 0
nV^2 = 0.96, p-value = NA
sample estimates:
    dCov 
    0.438178 
```
#### Calculating the Distance Standard Deviations

### References
* Björn Böttcher, Martin Keller-Ressel, René L. Schilling. (2019), Distance multivariance: New Dependence Measures for Random Vectors, The Annals of Statistics, Vol. 47, No. 5, pp.2757-2789. https://projecteuclid.org/euclid.aos/1564797863

* Szekely, G.J., Rizzo, M.L., and Bakirov, N.K. (2007), Measuring and Testing Dependence by Correlation of Distances, Annals of Statistics, Vol. 35 No. 6, pp. 2769-2794. http://dx.doi.org/10.1214/009053607000000505

* Szekely, G.J. and Rizzo, M.L. (2009), Brownian Distance Covariance, Annals of Applied Statistics, Vol. 3, No. 4, 1236-1265. http://dx.doi.org/10.1214/09-AOAS312

* Szekely, G.J. and Rizzo, M.L. (2009), Rejoinder: Brownian Distance Covariance, Annals of Applied Statistics, Vol. 3, No. 4, 1303-1308. https://projecteuclid.org/euclid.aoas/1267453941


