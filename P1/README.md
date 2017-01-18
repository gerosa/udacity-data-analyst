# Stroop Effect Statistical Analysis 

## Background Information
In a Stroop task, participants are presented with a list of words, with each word displayed in a color of ink. The participant’s task is to say out loud the color of the ink in which the word is printed. The task has two conditions: a congruent words condition, and an incongruent words condition. In the congruent words condition, the words being displayed are color words whose names match the colors in which they are printed: for example RED, BLUE. In the incongruent words condition, the words displayed are color words whose names do not match the colors in which they are printed: for example PURPLE, ORANGE. In each case, we measure the time it takes to name the ink colors in equally-sized lists. Each participant will go through and record a time from each condition.

## Study Design
A pre-test post-test statistical study will be performed on [this dataset](https://github.com/gerosa/udacity-data-analyst/P1/stroopdata.csv) which contains results from 24 participants in the task. Each row of the dataset contains the performance for one participant, with the first number their results on the congruent task and the second number their performance on the incongruent task.

The goal of the study is to observe if participants take more time to name the words in the incongruent condition than in the congruent condition. In other words, this study aims to demonstrate the Stroop effect. 

## Questions for Investigation

### 1. What is our independent variable? What is our dependent variable?
The independent variable is the word condition (congruent or incroguent) and the dependent variable is the time to name the words.

### 2. What is an appropriate set of hypotheses for this task? What kind of statistical test do you expect to perform? Justify your choices.
The null hypothesis is there is no difference between the two conditions. To be more precise, the null hypothesis is the mean time to name the words in the incroguent condition is less then or equals to the mean time to name the words in the congruent condition.
![](https://render.githubusercontent.com/render/math?math=H_0%3A%20%20%5Cmu_i%20%20%5Cleq%20%20%5Cmu_c)

The null hypothesis can be rephrased as the diference between the incongruent and congruent means is less than or equals to 0.
![](https://render.githubusercontent.com/render/math?math=H_0%3A%20%5Cmu_i%20-%20%5Cmu_c%20%20%5Cleq%200)
![](https://render.githubusercontent.com/render/math?math=H_0%3A%20%20%5Cmu_D%20%20%5Cleq%200)

The alternative hypothesis is the mean difference are greater than 0.
![](https://render.githubusercontent.com/render/math?math=H_0%3A%20%20%5Cmu_D%20%3E%200)

A one-sample t-test will be performed because we don't know the population parameters.  

## Results

### Descriptive statistics

Sample size: 24



### Inferential statistics
A one-sample t-test will be used to 

### Effect size measures


## Interpretation


