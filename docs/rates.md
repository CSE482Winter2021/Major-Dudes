#### Problem

Given:

* Route $X$ with stops $S_1\cdots S_n$
* Total ORCA to APC rate $r_X=\frac{o_{\text{total}}}{a_{\text{total}}}$ for the route
* Observed ORCA boarding count $o_i$ and census tract population $p_i$ for each $S_i\in X$

We want to estimate the ORCA rate $\frac{o_i}{a_i}$ at each stop $S_i$, such that $\frac{\sum_{i=1}^{n}o_i}{\sum_{i=1}^{n}a_i}=r_X$. We can define our approximation as $\bold{\hat r}=\begin{pmatrix}\hat r_1\cdots \hat r_n\end{pmatrix}$, where $\hat r_i\approx \frac{o_i}{a_i}$.

#### Assumptions

Unfortunately, we don't have data on observed APC counts by stop, but we do have the populations of the census tracts within which each stop falls. Let's assume that the population of a stop's tract is a good proxy for the number of APC boardings at that stop. More specifically, the APC count scales linearly with the tract population. This is a pretty flimsy assumption, but it's the best we can do given the data that we have.

**Formal assumption:** $\begin{pmatrix}p_1\cdots p_n\end{pmatrix}$ is linearly dependent with $\begin{pmatrix}a_1\cdots a_n\end{pmatrix}$. In other words, there is some constant scalar $c$ such that $\forall S_i \in X:\space\mathbb a_i = cp_i$.

<div style="page-break-after: always; break-after: page;"></div>

#### Calculation

Let:
$$
\bold o = \begin{pmatrix}o_1\cdots o_n\end{pmatrix}\qquad
\bold p = \begin{pmatrix}p_1\cdots p_n\end{pmatrix}\qquad
$$

Under our assumption, $\bold p$ is linearly dependent with $\begin{pmatrix}a_1\cdots a_n\end{pmatrix}$, so there must be some $c$ such that $\bold{\hat r}=\frac{\bold o}{c\bold p}$. Since we are given $r_X=\frac{o_{\text{total}}}{a_{\text{total}}}$, we can use our assumption to rewrite $r_X$ as follows:

$$
r_X
= \frac{\sum_{i=1}^{n}o_i}{\sum_{i=1}^{n}a_i}
= \frac{\sum_{i=1}^{n}o_i}{c\sum_{i=1}^{n}p_i}
$$

Taking that definition of $r_X$, we can find $\bold{\hat r}$ as follows:


$$
\begin{aligned}
r_X &= \frac{\sum_{i=1}^{n}o_i}{c  \sum_{i=1}^{n}p_i} \quad\rarr\quad
c    = \frac{\sum_{i=1}^{n}o_i}{r_X\sum_{i=1}^{n}p_i}\\\\
\bold{\hat r} &= \frac{\bold o}{c\bold p}
=\frac
{\left(r_X\sum_{i=1}^{n}p_i\right)\bold o}
{\left(   \sum_{i=1}^{n}o_i\right)\bold p}
\end{aligned}
$$


#### Error Analysis

Since the whole point of finding $\bold{\hat r}$ is to capture the variance of $r_X$ across the route, then we expect lots of variance among its values compared to $r_X$. Nonetheless, it is still useful to look at the error as a measure of how much variance we have.

In our analysis we used MAE and RMSE. These were calculated as follows:
$$
\begin{aligned}
\text{MAE}&=
\text{average}\left\{(\hat r_i-r_X) : S_i\in X, X\in D\right\}\\
\text{RMSE}&=
\left(\text{average}\left\{
(\hat r_i-r_X)^2 : S_i\in X, X\in D
\right\}\right)^{\frac12}\\
\end{aligned}
$$
where $D$ is the dataset containing each route $X$, each with a unique $r_X$ and $\hat{\bold r}$.

Using the winter APC counts data with a 15 minute time interval, we calculated an MAE of **1.082** and an RMSE of **4.113**. Approximately **46%** of the predicted by-stop ORCA rate estimates fell within the tolerance interval [0.1, 1]. For the points that fell outside of this interval, we threw them out and replaced them with their corresponding $r_D$ values averaged across each route travelling through the stop and weighted by the routes' APC counts. Note that these error values were calculated before running the tolerance interval.

Although only 46% of our estimates fell within a reasonable interval, we believe that this estimation model is still quite robust given the data to which we have access, and the relatively high MAE and RMSE values indicate that we've captured a good amount of ORCA rate variance within routes.