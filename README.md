# StatExplore
A Python Package to Facilitate Statistical Research

## Distance Correlation


<div align="center">
<img 
src="https://github.com/b-knight/StatExplore/blob/master/images/Pearsons_Correlation_Coefficient.gif?sanitize=true", 
align="middle",
alt="Pearson Product-Moment Correlation Coefficien">
</div>
<p align="center"><sub><b>Equation 1: Pearson Product-Moment Correlation Coefficient</sub></b></p>





<div align="center">
<img 
src="https://github.com/b-knight/StatExplore/blob/master/images/Correlation_Examples.png?sanitize=true", 
align="middle",
alt="Sets of Pearson Correlation Coefficients">
</div>
<p align="center"><sub><b>Image 1: Sets of Pearson Correlation Coefficients </b></sub></p>
<p align="center"><sub> SOURCE: https://commons.wikimedia.org/wiki/File:Correlation_examples2.svg </sub></p>


<div align="center">
<img 
src="https://github.com/b-knight/StatExplore/blob/master/images/Distance_Correlation.gif?sanitize=true", 
align="middle",
alt="Pearson Product-Moment Correlation Coefficien">
</div>
<p align="center"><sub><b>Equation 2: Distance Correlation</sub></b></p>



<div align="center">
<img src="https://github.com/b-knight/StatExplore/blob/master/images/Distance_Correlation_Examples.png?sanitize=true",
align="middle", 
alt="Sets of Distance Correlation Coefficients">
</div>
<p align="center"><sub><b>Image 2: Sets of Distance Correlation Coefficients</b></sub></p>
<p align="center"><sub> SOURCE: https://commons.wikimedia.org/wiki/File:Distance_Correlation_Examples.svg</sub></p>

The numerator is the distance covariance. The first step in calculating 

|    | X  | Y  |
| -- | -- | -- |
| A  | 0  | 2  |
| B  | 1  | 1  |
| C  | 2  | 0  |
| D  | 3  | 1  |
| E  | 4  | 2  |
<p align="center"><sub><b>Table 1: Raw Data</b></sub></p>


<table>
<tr><th> X Pair-Wise Distances </th><th> Y Pair-Wise Distances </th></tr>

<tr><td>

| X  | A  | B  | C  | D  | E  |
| -- | -- | -- | -- | -- | -- |
| A  | 0  | -  | -  | -  | -  |
| B  | 1  | 0  | -  | -  | -  |
| C  | 2  | 1  | 0  | -  | -  |
| D  | 3  | 2  | 1  | 0  | -  |
| E  | 4  | 3  | 2  | 1  | 0  |

</td><td>

| Y  | A  | B  | C  | D  | E  |
| -- | -- | -- | -- | -- | -- |
| A  | 0  | -  | -  | -  | -  |
| B  | 1  | 0  | -  | -  | -  |
| C  | 2  | 1  | 0  | -  | -  |
| D  | 1  | 0  | 1  | 0  | -  |
| E  | 0  | 1  | 2  | 1  | 0  |

</td></tr> </table>
<p align="center"><sub><b>Tables 2 & 3: Pair-Wise Distances</b></sub></p>

### References
* Huo, Xiaoming, Gábor J. Székely, and Alfréd Rényi, “Fast Computing for Distance Covariance”,  
eprint arXiv:1410.1503, October 2014, https://arxiv.org/abs/1410.1503.


