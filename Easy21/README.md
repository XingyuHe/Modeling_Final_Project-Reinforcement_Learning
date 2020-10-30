# Easy21
## Discussion

### What are the pros and cons of bootstrapping in Easy21?
Bootstrapping helps reduce the variance but it increases the bias. It allows updates with varying step interval rather than waiting till the end of an episode. On the other hand, using Monte Carlo control allows convergence to the true value function. 

### Would you expect bootstrapping to help more in blackjack or Easy21?
I would not expect bootstrapping to help more in blackjac or Easy21 than Monte Carlo control. Blackjack and Easy21 have very limited number of states. Hence, variance is affordable when using Monte Carlo. Consider that dealer's first cards vary from 1 to 10 and the summation of player's cards can range from 1 to 21. There are 10 × 21 = 210 states. It is entirely possible that every possible state is covered using Monte Carlo control. Therefore, it is not necessary to use bootstrapping. 

### What are the pros and cons of function approximation in Easy21?
Function approximator allows the usage of feature. This allows using hand engineering or convolution neural network to extract useful features. Further, using features reduces the number of trained variables. However, comparing to Monte Carlo control using table look up, it does not guarantee reaching the true value functions. It could get stuck in local optima if using gradient descent. 

### How would you modify the function approximator suggested in this section to get better results in Easy21?
I think a decent idea to try out is using convolution neural network instead of hand engineering features. The feature mapper seems kind of arbitrary. Different intervals don't seem to matter that much when they are overlapping. 



