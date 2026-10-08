---
id: ph211-data-analysis-handout
title: "Lab 2 – Fundamentals of Data Analysis"   # the original title text; see ledger 22
course: PH211
sequence: 2
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH211/Lab 2 - Data Analysis - Handout.docx"
source_sha256: "3891e5de553bd94a641881ef64671a73949e8e68445b6150614558fc0e99fd40"
status: converted
---

# Lab 2 – Fundamentals of Data Analysis

## PH211 – General Physics with Calculus

**Experimental goal:** **Analyze position vs time data for an object rolling down a ramp and determine an experimental value for the acceleration of gravity, *g*.**

*Data* is a collection of information; in physics, usually numbers representing physical quantities. *Analysis* is a process of doing operations on data (such as calculations) or quantifying and visualizing relationships in the data to make meaning from it. In this lab, you’ll learn the fundamental data analysis skills, listed below, that will be utilized and built upon throughout this course.

## Learning Objectives

**Learning goal:** **Develop and practice fundamental data analysis techniques.**

This lab activity is designed to help you practice the following skills:

1.  Produce scatter plots of data.
2.  Fit simple functions to a data set.
3.  Use an *R^2^* value to evaluate the quality of a fit.
4.  Linearize data.
5.  Extract physical parameters from fits to a model.

## Equipment

::: action
- A computer with Excel installed.
- The *Excel Skills* document which has tutorials for all of the activities in this lab
:::

**We advise *against* using the web version of Excel in this course. It doesn’t have all the functionality you’ll need.**

## Installing Excel Software (optional)

All the lab computers have Excel installed on them, but you are welcome to work on your own computer if you prefer. If you need to install Excel, you can get it through OSU as part of the Microsoft 365 package. To do this, go to [[https://technology.oregonstate.edu/services/microsoft-365]{.underline}](https://technology.oregonstate.edu/services/microsoft-365) (website correct as of Fall 2026).

If you have trouble installing Excel, you may contact OSU help desk [[here]{.underline}](https://technology.oregonstate.edu/help). If you need help while going through this lab, reach out to peers in the class or your lab instructor.

If no one in your group can install Excel, or if you just prefer not to use a personal laptop, you should use the lab computer at your station.

## Part 1: Importing and Plotting Data

Your lab instructor may have demonstrated rolling an object down an incline. The data provided below gives the position of the object at different points in time. You will practice creating plots with this data.

### Importing

Linked below is a spreadsheet with ten data sets, each collected at a different ramp angle. [Your group will be assigned *one* of the data sets to analyze.]{.underline} Later in the lab, you’ll be given the value of your angle and share your results with your class.

Position vs time data: [[https://rb.gy/i71up4]{.underline}](https://rb.gy/i71up4)

::: action
- **Copy your group’s data into Excel from the link above.**
- **After importing your data, create a scatter plot of your** $\mathbf{r\ vs.\ t}$ **data. Instructions for doing this are provided in the *Excel Skills* document.**
:::

### Plotting

::: hint
- By convention, “*a vs. b*”, means *a* goes on the y-axis and *b* goes on the x-axis.
- Do **not** connect data points on a scatter plot with lines. Adding lines to a scatter plot implies a relationship between the data points that might not exist.
- Make sure you create **Scatter Plots** and not Line Plots.
:::

:::: box
### Whenever you create a plot, you should:

::: hint
- Evaluate if the plot makes sense. Are the axes correct? Do you have the right number of data points?
- Include a descriptive title and labels on each axis, always including physical units.
- Add a legend, unless you only have one set of data and the title describes it.
- Display the equation and *R^2^* value for any trendline you include (learn how in Part 2!)
:::
::::

## Part 2: Adding a Trendline

Fitting a function to a dataset is a key part of data analysis because it allows us to understand how the *dependent* variable relates to the *independent* variable. Most of the plots you’ll create will include a fit to your data. Fits are typically used to determine how well the data agrees with a particular (mathematical) model, or equation, that describes the system’s behavior.

The correlation coefficient, *R^2^*, is one measure of how well the model fits the data. Values close to 1 signify that the fit does a good job of predicting the data, whereas values closer to zero signify that the fit poorly predicts the data. While there are no hard cutoffs, below 0.7 is indicative of a poor fit, and above 0.9 or 0.95 is generally indicative of a good or very good fit.

While you can use visual inspection to make rough evaluations of each trendline, *R^2^* is often useful for distinguishing among equally good-looking fits.

::: action
- Use Excel’s trendline feature to try different fits to the data.
- If you need help, refer to the section on Plotting and Fitting Data in the *Excel Skills* document or talk with your Instructor.
:::

::: {.question #ph211-data-analysis:trendlines-tried}
**Which trendlines did you try to model the position vs. time data? Which type of mathematical relationship best describes the data? How did you decide? Justify your conclusion with evidence.**
:::

::: hint
- **Try at least two fits. Use the above information about interpreting the R^2^ value to help decide which one is best.**
:::

::: {.question #ph211-data-analysis:plot-each-model}
**Insert a separate plot with the trendline, equation, and R^2^ value for each model you tried.**
:::

::: hint
- **Make sure your plot includes all the required elements described in the box on the previous page.**
:::

## Part 3: Introduction to Linearization

In Part 2, you tried a few different trendlines to see which matched your data best. Often, though, experimenters have a hypothesis or *model*, usually expressed as an equation, about how the variables will be related to each other. The goal of an experiment is often to check whether the data supports or refutes the model – whether the model describes the data well.

:::: box
### Linearization

In the context of data analysis, “linear” refers to a directly proportional relationship between the dependent and independent variables in an equation.

::: action
- Mathematically, if two variables $x$ and $y$ have a linear relationship, we can express this as $y = mx + b$ where m and b are constants.
- More simply, we can write this as $y \propto x$ where $\propto$ means “is proportional to”.
- When graphed, data with a linear relationship falls on a straight line.
:::

Linearization comes in handy when your data or hypothesis is *not* linear.

When you fit data with a linear trendline, you are essentially checking whether the two variables are proportional to each other. To check a nonlinear hypothesis, can we instead check if one variable is proportional to *a function of* the other variable.

**In practice, linearization is done by calculating a new column of data that gives the values of a function of the input variable** (you will practice this below, so don’t worry if you don’t understand what this means yet). Typically, the input variable is the independent variable, and the function is chosen so that the resulting quantity is proportional to the dependent variable. Then, the linearized data can be plotted and analyzed.
::::

When a nonlinear hypothesis is being investigated, it is often helpful to use this technique. Linearizing data is a powerful analysis tool we will use again and again throughout the 21X sequence.

Let’s create a linearized plot of the position vs. time data you’ve been analyzing. Typically, we will build or justify a model using the physics being investigated in the lab. Since we’re just getting started, this time we’ll simply state the model to be tested.

[Our model:]{.underline} The distance an object has traveled down a ramp at some time t after being released is proportional to the time squared. In equation form:

$$r = \frac{1}{2}{at}^{2}$$

Note that this is a *nonlinear* (specifically quadratic) relationship between *r* and *t*. Another way to describe this model is that it states that *r* is proportional to $t^{2}$ ($r \propto t^{2}$). In order to check whether this model describes our data, follow these steps:

::: {.question #ph211-data-analysis:linearize-position-time}
**Linearize and analyze the position vs. time data**

a.  **Consider the plot of *r* vs*. t* that you made in Part 1. Check if the two variables have a linear relationship by fitting the data with a linear trendline and looking at the** $\mathbf{R}^{\mathbf{2}}$ **value. Based on the quality of the fit, is *r* directly proportional to *t*?**
b.  **Linearize your data: create a new column in your data table that calculates** $\mathbf{t}^{\mathbf{2}}$**.**

::: hint
- Time saver: Do not calculate $t^{2}$ individually for each data point, instead use Excel’s formula drag feature.
:::

c.  **Create a plot of *r* vs.** $\mathbf{t}^{\mathbf{2}}$ **Note that even though we’re not representing it as just a letter,** $\mathbf{t}^{\mathbf{2}}$ **is also a variable, just like plain old t.**
d.  **Check whether the variables *r* and** $\mathbf{t}^{\mathbf{2}}$ **are proportional to each other by fitting the plot with a linear trendline and looking at the** $\mathbf{R}^{\mathbf{2}}$ **value. Remember to display the equation for the trendline on your plot as well. Include this plot in your lab report.**
e.  **Which relationship describes the data better,** $\mathbf{r\  \propto \ t}$ **or *r***$\mathbf{\  \propto}\mathbf{t}^{\mathbf{2}}$**? Support your decision by comparing the** $\mathbf{R}^{\mathbf{2}}$ **values.**
:::

:::: box
### Why Linearize?

::: action
- Linear data is typically easier to understand and analyze.
- There are analysis methods we can apply to linear data that don’t work as well (or at all) with nonlinear data.
- It is relatively easy to fit a line to data - there are just two important values to determine: the slope and intercept of the data.
:::
::::

Another benefit of linearizing data is that we can easily use the equations of our trendlines to find out what the constants (or *parameters*) are in our model. In the model above, there is some constant *a* that relates *t* to *x*. (This turns out to be acceleration, as you may have learned in lecture).

::: {.question #ph211-data-analysis:find-constant-a}
**Use your linearized data to find the constant *a*:**

a.  **Compare the equation for a line:** $\mathbf{y = mx + b}$ **to the hypothesis:** $\mathbf{r =}\frac{\mathbf{1}}{\mathbf{2}}\mathbf{at}^{\mathbf{2}}$**. For your linearized data, what is graphed on the x-axis, and what is graphed on the y-axis?**
b.  **In a linear equation, m represents the slope of the line. Which part of the model corresponds to this piece of the linear equation?**
c.  **Now write down the equation of the trendline you created on your linearized plot. Which part of this equation corresponds to “m”?**
d.  **Now matching parts of the model equation and the trendline equation, calculate the value of *a.* Show your work (you can insert equation in most text-editing programs).**
:::

## Part 4: Collaboration and Linearization Practice

Collaboration is a key part of science. While scientists certainly compete with each other, they are all still working towards the same goal of understanding the world around them. Collaborations allow scientists to expand their experimental work beyond what they can do individually.

Each of you have been given data taken at a different ramp angle. Once all of the groups have reported the value of $a$ from the fit to their linearized data, your instructor will add additional information to the chart - the angle of the incline when each set of data was taken. Instead of all groups working with all data sets, you have collaborated to spread out the work.

Next, we will analyze the behavior of the $a\ vs.\ \theta$ data. The model we will test is one you may have seen in physics lecture (we provide it here without justification, similar to above, since this lab is focused on how to do the analysis itself).

[Our model:]{.underline} the acceleration of an object traveling down a ramp is proportional to the acceleration of gravity times the sine of the ramp angle. In equation form:

$$a\  = \ g\ sin(\theta)$$

We will test this model by seeing if our data follows the expected behavior. This is a *nonlinear* relationship, so it will be useful to linearize the data.

::: action
- **Copy the angle and slope data for the entire class into your own Excel spreadsheet. (Put the angle in the first column.)**
:::

::: {.question #ph211-data-analysis:acceleration-vs-angle}
**Analyze the acceleration vs. angle data**

a.  **What fit (relationship between the variables) could you use to support or refute the model expressed by the above equation?**

::: action
- **Create a scatter plot of acceleration vs. angle. Fit the plot with a linear trendline. Display the equation and** $\mathbf{R}^{\mathbf{2}}$ **value.**
:::

b.  **Include the plot in your report.**
c.  **Now compare the equation for a line and the model you are testing (**$\mathbf{a = g\ sin\theta}$**). In the model, which term corresponds to each piece of the linear equation (y, m, x, and b)?**
d.  **Linearize the data by creating a new, calculated column in your data table that calculates what you said corresponds to x.**

::: hint
- You will need to convert the angles to radians using a conversion factor in your Excel formula. Note that in Excel π is written as “PI()” with nothing inside the parentheses. This is [not]{.underline} linearizing, this is just changing units.
:::

::: action
- **Create a new scatter plot of the linearized data and add a linear trendline. Display the equation and** $\mathbf{R}^{\mathbf{2}}$ **value**
:::

e.  **Include the plot in your report. Based on the quality of the fit, does the data support the model** $\mathbf{a = g\ sin\theta}$**?**
:::

::: {.question #ph211-data-analysis:experimental-g}
**Use your plot and fit to the linearized data to find the experimental value of the constant g from the model. (This is similar to how you used your fit to the** $\mathbf{r\ vs.\ }\mathbf{t}^{\mathbf{2}}$ **plot to find *a* in Part 3).**

a.  **Show or describe how you found your experimental value of *g* and report the value you found.**
b.  **Is this close to what you would expect (if you’re not sure what the expected value is, ask your instructor)?**
:::

## Part 5: Plotting Multiple Data Sets

Choose any two data sets of position vs time from the data table at the end of this handout (or from the Excel file of data if that’s been provided to you). Plot both sets of data on one scatter plot. The *Excel Skills* document explains how to do this.

You should get two sets of points. Both will have the same x values (the time). They will have different y values (the position). Add separate trendlines, one for each set of data. Display the equation of the fit and the R^2^ value for each trendline.

Now add a *legend* to your plot. (Look in the “Add Chart Element” dropdown in the “Chart Design” menu.) The legend should include separate entries for each data set as well as each trendline. Notice that you can edit the legend (double-click on it) if you’d like to remove any of the entries.

::: {.question #ph211-data-analysis:multiple-data-sets-plot}
**Insert your plot or a cropped screenshot of the plot with multiple data sets you created into your report. Don’t forget to include a title and label your axes.**
:::

## Part 6: Summarizing and Reflecting

::: {.question #ph211-data-analysis:summarize-results}
**Briefly summarize your results and analysis by describing your procedure and the strategies you used. What did your group learn about the behavior of the system? Specifically touch on the following points:**

::: action
- **What does linearization allow you to do?**
- **How can you tell when linearization is a useful tool for analyzing your data?**
- **List how each of your group members contributed to the work you did in the lab.**
:::
:::

::: {.question #ph211-data-analysis:individual-reflection}
**Each lab member should write an [individual]{.underline} concise paragraph reflecting on the lab. Identify each contribution by name. Each should specifically address the following:**

::: action
- **One new thing you've learned about analyzing data.**
- **Any unanswered questions you still have.**
- **Your comfort working with Excel as we continue in the course.**
- **What things did your group do well today to ensure inclusion of everyone in the group?**
:::
:::

## Part 7: Submit Your Group’s Lab Report

Make sure everyone’s name is on your group’s lab report. If you submit through Gradescope remember to add everyone in your group to the assignment. This is done at the end of the submission process.

## Appendix: Position vs. Time

**Distance (m)**

  ----------------------------------------------------------------------------------------------
  **Time (s)**   1       2       3       4       5       6       7       8       9       10
  -------------- ------- ------- ------- ------- ------- ------- ------- ------- ------- -------
  0.00           0.000   0.000   0.000   0.000   0.000   0.000   0.000   0.000   0.000   0.000

  0.10           0.014   0.005   0.015   0.008   0.023   0.027   0.027   0.029   0.044   0.044

  0.20           0.024   0.039   0.048   0.055   0.090   0.108   0.128   0.138   0.180   0.181

  0.30           0.032   0.082   0.114   0.135   0.201   0.247   0.294   0.325   0.413   0.424

  0.40           0.052   0.132   0.213   0.237   0.341   0.422   0.514   0.579   0.728   0.756

  0.50           0.081   0.199   0.323   0.385   0.523   0.639   0.803   0.920   1.119   1.174

  0.60           0.134   0.274   0.466   0.566   0.752   0.904   1.152   1.339   1.614   1.699

  0.70           0.208   0.376   0.648   0.775   1.019   1.218   1.555   1.824   2.197   2.322

  0.80           0.272   0.509   0.858   1.023   1.323   1.584   2.011   2.394   2.855   3.044

  0.90           0.341   0.650   1.079   1.299   1.670   2.001   2.529   3.030            

  1.00           0.431   0.799   1.300   1.596   2.061   2.482   3.115                    

  1.10           0.527   0.970   1.548   1.934   2.502   3.007                            

  1.20           0.618   1.153   1.836   2.328   2.983                                    

  1.30           0.703   1.357   2.162   2.750                                            

  1.40           0.818   1.589   2.502                                                    

  1.50           0.950   1.853   2.871                                                    

  1.60           1.093   2.138                                                            

  1.70           1.242   2.431                                                            

  1.80           1.392   2.732                                                            

  1.90           1.551   3.041                                                            

  2.00           1.707                                                                    

  2.10           1.883                                                                    

  2.20           2.064                                                                    
  ----------------------------------------------------------------------------------------------
