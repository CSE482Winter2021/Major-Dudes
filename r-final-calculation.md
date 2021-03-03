# Calculation of By-Stop ORCA Rates



Given:

* Route $R$ with stops $S_1\cdots S_n$
* Total ORCA rate $r_R=\frac{o_{\text{total}}}{\text{apc}_{\text{total}}}$ for the route
* Observed ORCA rate $o_i$ and tract population $p_i$ for each $S_i$

We want an estimator $\bold{\hat r}=[\hat r_1\cdots \hat r_n]$ which estimates the ORCA rate $\frac{o_i}{\text{apc}_i}$ for each $S_i\in R$.

**Assumption:** For each stop, $\frac{o_i}{p_i}$ is linearly dependent with $\frac{o_i}{\text{apc}_i}$ (i.e., the ORCA for that route and stop), which is unknown. In other words, $\forall S_i \in R:\space \frac{o_i}{\text{apc}_i}\approx c\left(\frac{o_i}{p_i}\right)$, where $c$ is some constant scalar. This is a pretty flimsy assumption, but it's the best we can do given the data we have.



#### Calculation

Let:
$$
\begin{align}
\bold o &= [o_1\cdots o_n]\\
\bold p &= [p_1\cdots p_n]\\
\bold{\hat r}' &= \frac{\bold o}{\bold p}
\end{align}
$$
Under our assumption, $\bold{\hat r}'$ is linearly dependent with $\bold{\hat r}$, so there must be some $c$ such that $c\bold{\hat r}'=\bold{\hat r}$. Since we are given $r_R=\frac{o_{\text{total}}}{\text{apc}_{\text{total}}}$, we can rewrite that expression as $r_R=c\left(\frac{\sum\bold o}{\sum\bold p}\right)$. Taking that definition of $c$, we can find $\bold{\hat r}$ as follows:
$$
\begin{align}
r_R &= \frac{c\sum_{i=1}^{n}o_i}{\sum_{i=1}^{n}p_i} \quad\rarr\quad
c = \frac{r_R\sum_{i=1}^{n}p_i}{\sum_{i=1}^{n}o_i}\\\\
\bold{\hat r} &= c\bold{\hat r}'
=\left(\frac{r_R\sum_{i=1}^{n}p_i}{\sum_{i=1}^{n}o_i}\right)\bold{\hat r}'
=\frac{\left(r_R\sum_{i=1}^{n}p_i\right)\bold o}{\left(\sum_{i=1}^{n}o_i\right)\bold p}
\end{align}
$$


#### Error Analysis

Since the whole point of finding $\bold{\hat r}$ is to capture the variance of $r$ across the route, then we expect lots of variance among its values compared to $r$. Nonetheless, it is still useful to look at the error as a measure of how much variance we have.

In our analysis we used MAE and RMSE. These are calculated as follows:
$$
\begin{align}
\text{MAE}&=
\text{average}\left\{(\hat r_i-r_R) : S_i\in R, R\in D\right\}\\
\text{RMSE}&=
\left(\text{average}\left\{
(\hat r_i-r_R)^2 : S_i\in R, R\in D
\right\}\right)^{\frac12}\\
\end{align}
$$
where $D$ is the dataset containing each route $R$, each with a unique $r_R$ and $\hat{\bold r}$.

Using the winter APC counts data with a 15 minute time interval, we calculated an MAE of **1.082** and an RMSE of **4.113**. Approximately 46% of the predicted by-stop ORCA rate estimates fell within the tolerance interval [0.1, 1]. For the points that fell outside of this interval, we threw them out and replaced them with their corresponding $r$ value, averaged across each route travelling through the stop and weighted by the routes' APC counts. Note that these error values were calculated before running the tolerance interval.

Although only 46% of our estimates fell within a reasonable interval, we believe that this estimation model is still quite robust given the data to which we have access, and the relatively high MAE and RMSE values indicate that we've captured a good amount of ORCA rate variance within routes.