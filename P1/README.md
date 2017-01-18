# Stroop Effect Statistical Analysis 

## Background Information
In a Stroop task, participants are presented with a list of words, with each word displayed in a color of ink. The participant’s task is to say out loud the color of the ink in which the word is printed. The task has two conditions: a congruent words condition, and an incongruent words condition. In the congruent words condition, the words being displayed are color words whose names match the colors in which they are printed: for example RED, BLUE. In the incongruent words condition, the words displayed are color words whose names do not match the colors in which they are printed: for example PURPLE, ORANGE. In each case, we measure the time it takes to name the ink colors in equally-sized lists. Each participant will go through and record a time from each condition.

## Study Design
A pre-test post-test statistical study will be performed on [this dataset](https://github.com/gerosa/udacity-data-analyst/blob/master/P1/stroopdata.csv) which contains results from 24 participants in the task. Each row of the dataset contains the performance for one participant, with the first number their results on the congruent task and the second number their performance on the incongruent task.

The goal of the study is to observe if participants take more time to name the words in the incongruent condition than in the congruent condition. In other words, this study aims to demonstrate the Stroop effect. 

## Questions for Investigation

### 1. What is our independent variable? What is our dependent variable?
The independent variable is the word condition (congruent or incongruent) and the dependent variable is the time to name the words.

### 2. What is an appropriate set of hypotheses for this task? What kind of statistical test do you expect to perform? Justify your choices.
The null hypothesis is there is no significant difference between the mean time to name words in the congruent and incroguent conditions.

![](https://render.githubusercontent.com/render/math?math=H_0%3A%20%20%5Cmu_i%20%20%3D%20%5Cmu_c)

The null hypothesis can be rephrased as the diference between the incongruent and congruent condition means is equals to 0.

![](https://render.githubusercontent.com/render/math?math=H_0%3A%20%5Cmu_i%20-%20%5Cmu_c%20%3D%200)

![](https://render.githubusercontent.com/render/math?math=H_0%3A%20%20%5Cmu_D%20%3D%200)

The alternative hypothesis is the mean difference is greater than 0.

![](https://render.githubusercontent.com/render/math?math=H_a%3A%20%20%5Cmu_D%20%3E%200)

A t-test will be performed because:

1. We don't know the population standard deviation.
2. the sample size is less than 30.

As the same sample is been tested in two different conditions, a dependent t-test for paired samples is the best choice.

### 3. Report some descriptive statistics regarding this dataset. Include at least one measure of central tendency and at least one measure of variability.

| Condition        | Sample Mean  | Sample Standard Deviation    |
| ---------------- | ------------ | -----------------------------|
| congruent        | 14.05        | 3.56                         |
| incongruent      | 22.02        | 4.80                         |
| difference       | 7.96         | 4.86                         |

### 4. Provide one or two visualizations that show the distribution of the sample data. Write one or two sentences noting what you observe about the plot or plots.

#### Congruent Distribution
The congruent histogram (bin size equals 3) follows a normal distribution

![Congruent Distribution](https://raw.githubusercontent.com/gerosa/udacity-data-analyst/master/P1/congruent_distribution.png)

#### Incongruent Distribution
The incongruent histogram (bin size equals 2.5) follows a normal distribution with few outliners at the positive side.

![Incongruent Distribution](https://raw.githubusercontent.com/gerosa/udacity-data-analyst/master/P1/incongruent_distribution.png)

### 5. Now, perform the statistical test and report your results. What is your confidence level and your critical statistic value? Do you reject the null hypothesis or fail to reject it? Come to a conclusion in terms of the experiment task. Did the results match up with your expectations?
```
alpha = 0.01
t-critical = 2.5
t(23) = 8.02, p < 0.01, One-tailed positive direction
99% CI = (5.18, 10.75)
```
Based on the above results we reject the null and we can say that there is a statiscally significant effect in the positve direction, i.e, the incongruent task takes more time than the congruent task.

### 6. Optional: What do you think is responsible for the effects observed? Can you think of an alternative or similar task that would result in a similar effect? Some research about the problem will be helpful for thinking about these two questions!
When we learn how to read, we train our brains to reconize the words very fast. On the other hand, we don't need to train our brains to look at a specific color and immediately recognize its name, i.e, we need to think first. So, when there is an incongruence, the word is reconized faster than the color and takes more time to correct the wrong name.

A similar task could be performed with geometric forms, writting the name of the form in the center and measuring the performance with and without incongruence.

## Resources
Google Sheets: https://docs.google.com/spreadsheets/d/1VpcTJFTl8UvGMI5IqxiDtEyak8_9yt-ShlzRnBEIUzc/edit?usp=sharing

