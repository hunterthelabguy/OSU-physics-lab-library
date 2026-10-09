---
id: ph212-data-analysis-handout
title: "Lab 1 – Data Analysis"   # the original title text; see ledger 22
course: PH212
sequence: 1
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH212/Lab 1 - Data Analysis - Handout.docx"
source_sha256: "2d28c22db05827a39bcf703ac8643750423a800ec99d8af7bc59f93f14b5f032"
status: converted
---

# Lab 1 – Data Analysis

## PH 212 – General Physics with Calculus

**Experimental goal: Determine the period *T* of a pendulum with a set length. Then investigate how the period of a pendulum depends on its length and compare to a given hypothesis.**

:::: box
### As you work through the lab:

1.  Numbered items reference things that need to be included in your lab report.

::: action
- Bulleted items are activities or tasks you’ll need to do to answer questions.
:::

::: hint
- Items with an arrow are hints or suggestions.
:::

Boxed information is about either the expectations for your lab reports or key concepts for the course.
::::

In this lab activity, you will create a simple experiment to investigate periodic motion and practice data analysis techniques to compare your data to a given hypothesis.

## Learning Objectives

**Learning goal: Learn and practice fundamental data analysis skills.**

This lab activity is designed to help you practice the following skills:

1.  Choose appropriate data collection procedures.
2.  Create scatter plots of data.
3.  Linearize and fit simple functions to a data set.
4.  Determine whether data supports a hypothesis.
5.  Use quantitative evidence to support conclusions.

## Equipment

::: action
- Computer with data analysis software (Excel and Graphical Analysis)
- *Excell Skills* document
- Simple pendulum consisting of a mass on a light string
- Table stand, various clamps and rods.
- Stopwatch
- Meter stick
- Protractor
:::

## Installing Excel Software

All the lab computers have Excel installed on them, but you are welcome to work on your own computer if you prefer. Here is how to get Excel if you need it.

::: action
- Sign into Microsoft 365 at [[https://is.oregonstate.edu/microsoft]{.underline}](https://is.oregonstate.edu/microsoft) using your ONID information.
- Click on "Install and more" in the top right and select "Install Microsoft 365 apps".
- Follow the instructions to download and install Excel.
:::

If you have trouble installing Excel, you may contact OSU help desk [[here]{.underline}](https://oregonstate.teamdynamix.com/TDClient/1935/Portal/Requests/TicketRequests/NewForm?ID=Dr9c0T7BaSI_). If you need help while going through this lab, reach out to peers in the class or your lab instructor.

If no one in your group can install Excel, you can use the lab computer at your station.

## Part 1: Creating an inclusive learning environment

We want to create an inclusive learning environment in the lab, where everyone is able to contribute their ideas and feel respected by their peers.

::: {.question #ph212-data-analysis:group-member-qualities}
**In your lab group, list at least 3 qualities of a good group member. Choose one to share with the class. Keep the others as backup contributions in case your first idea gets suggested by another group.**
:::

## Part 2: Plan the Experiment

Your first task is to determine period the of a simple pendulum (how long it takes to complete one full swing cycle) for a given length *L*, at starting amplitudes of both 5˚ and 10˚.

::: action
- **As a group, develop a plan for an *experiment to determine the period of a pendulum***. As you plan your experiment, consider:
  - What you will measure and how (what equipment, what methods – be specific!).
  - How can you estimate the uncertainty in the measured period? **Read the box below on uncertainty** and use it to guide your thinking.
  - Next, you’ll have a class discussion of your ideas for measuring both length and period and come to a consensus so that you can combine and compare data from all groups.
  - When you have a class procedure, get the pendulum length that your group should measure from your instructor. Then proceed with the experiment.
:::

::: {.question #ph212-data-analysis:experimental-setup}
**Describe your experimental set-up. Include a clearly labeled diagram that you can use to define the variables involved (such as *L* and *θ*). Make sure you represent all the important aspects of the experiment.**
:::

::: {.question #ph212-data-analysis:procedure}
**Describe your procedure.**

a.  **List the steps in enough detail that someone familiar with the equipment could reproduce your experiment. Include a clear description of how you will measure the period.**
b.  **List the members of your group and the responsibilities of each as you do the experiment.**
:::

:::: {.question #ph212-data-analysis:uncertainty-sources}
**Read the box below on sources of uncertainty.**

::: box
### What is Uncertainty?

*Uncertainty* is the acknowledgement that we cannot measure things exactly, and so any conclusion based on measurements will always include a range of possible answers. When making a measurement, there is no single “true value” of the measurand (measured quantity) that we can determine. Instead, we can define an interval that defines the range of values that we think are *probable* for the measurand. The narrower the interval, the more precisely we can approximate the measurand.

When including uncertainty in a value, we report it as **A ± Δ~A~**. We believe the value is **A**, but we’re unable to rule out the possibility that it’s higher or lower by an amount **Δ~A~**. (Sometimes it’s written +Δ~1~ / -Δ~2~ if the higher and lower ranges are different.) For example, a time might be reported as 2.45 s ± 0.03 s.

Common sources of uncertainty include:

1.  your judgement in reading analogue instruments
2.  the effects of environmental conditions on the measurement
3.  the sensitivity of your instruments (e.g. a digital scale, a meter stick)
4.  the rating or stated calibration of the instrument
5.  approximations and assumptions that you make while doing the experiment
6.  variations in repeated readings made under apparently identical conditions (statistical uncertainty)

A measurement uncertainty is not meant to be an indication of “mistakes” that you might make in an experiment. If you are aware that you have made a mistake, then you should repeat your experiment. **“Human error” is not a valid source of uncertainty**. If you know that you did something “wrong”, then the right course of action is to redo it correctly.
:::

a.  **List which sources you expect will contribute significantly to the uncertainty in each measurement of the period (for simplicity, we will not consider uncertainty in the angle or length measurements).**
b.  **For each source, state specifically where the uncertainty comes from and estimate a value.** (The statistical uncertainty cannot be found until after you’ve taken your measurements. You’ll find it in question 6.)
::::

## Part 3: Collect Data

You are now ready to perform your experiment and collect data.

::: {.question #ph212-data-analysis:data-table}
**Collect your data and report it in a table with labeled columns, including units.**
:::

::: {.question #ph212-data-analysis:period-and-uncertainty}
**Determine the period at 5˚ and at 10˚.**

a.  **Find the statistical uncertainty (the uncertainty associated with the spread of all of the measurements you made) using one of the two methods below.**

    i.  **One method for calculating this uncertainty is to take half of the difference between the largest and smallest measurement you made.**
    ii. **Another method is to calculate the standard deviation of your measurements.**

b.  **Find the total uncertainty by combining the uncertainties from all sources (those you estimated in question 4 as well as the statistical uncertainty) using the following equation:**

    $$\mathbf{\mathrm{\Delta}}\mathbf{T}_{\mathbf{total}}\mathbf{= \ }\sqrt{\left( \mathbf{\mathrm{\Delta}}\mathbf{T}_{\mathbf{1}} \right)^{\mathbf{2}}\mathbf{+}\left( \mathbf{\mathrm{\Delta}}\mathbf{T}_{\mathbf{2}} \right)^{\mathbf{2}}\mathbf{+}\left( \mathbf{\mathrm{\Delta}}\mathbf{T}_{\mathbf{3}} \right)^{\mathbf{2}}}$$

    **Where** $\mathbf{\mathrm{\Delta}}\mathbf{T}_{\mathbf{1}}$**,** $\mathbf{\mathrm{\Delta}}\mathbf{T}_{\mathbf{2}}$**, and** $\mathbf{\mathrm{\Delta}}\mathbf{T}_{\mathbf{3}}$ **are the uncertainty values you estimated for each source.**

    ::: hint
    - This is called *adding in quadrature* and it’s the method you’ll use to combine sources of uncertainty throughout the course.
    :::

c.  **Report the period you found for each angle and report in the A ± Δ~A~ format.**
:::

::: action
- Once your group has a final determination of the period, share it with your classmates following the instructions given by your instructor. Do this before going on to the remaining questions so that your classmates have immediate access to your data (and you have immediate access to theirs).
:::

::: {.question #ph212-data-analysis:class-data-table}
**Create a data table of the class’s data with the length, period for each amplitude, and associated uncertainty. Include the data table here.**
:::

## Part 4.1: Analyze the Data – Plotting

Next, you’ll plot the data that you and your classmates have collected. Plotting data is a crucial part of analysis and it’s a skill that you’ll use in every lab. The box below gives guidelines to use whenever you are plotting data throughout this course.

Now plot the period as a function of pendulum length. Display the 5˚ measurements and the 10˚ measurements as two series on the same plot. Don’t add this plot to your report yet.

In order to represent the uncertainty in the measurements graphically, we can include error bars on the plot.

::: hint
- This is only possible in Excel or Graphical Analysis; Google Sheets does not have this capability. If you have been working in Sheets, you will need to copy the class’s data into Excel.
:::

::: box
### Whenever you create a plot, you should:

::: hint
- Not connect the data points with lines.
- Make sure you create *Scatter Plots* and not *Line Plots*.
- Evaluate if the plot makes sense. Are the axes correct? Do you have the right number of data points?
- Include a descriptive title and labels on each axis, always including physical units.
- Add a legend, unless you only have one set of data and the title describes it.
- Display the equation and R^2^ value for any trendline you include
:::
:::

**[Error bars]{.underline}**

Error bars are a way to visually represent the range of values that the measurand (measured quantity) is likely to have. Recall from the “What is Uncertainty?” box above that there is not a “true” value of a measurand, all we can do is collect more information to improve our knowledge of the quantity. Error bars allow us to convey the information we have about the measurand more fully.

### To add error bars to a plot in Excel:

1.  Click the data set you want to add error bars to, and then under “Chart Design”, select “Add Chart Element” → “Error Bars” → “More Error Bar Options”
2.  Both horizontal and vertical error bars will be added. We usually just want vertical error bars, so select the horizontal error bars and delete them
3.  Under “Format Error Bars” → “Error Amount” select “Custom”
4.  Click “Specify Value” and highlight the uncertainty values for both the positive and negative error bar values
5.  Repeat for each dataset that needs error bars

::: {.question #ph212-data-analysis:plot-with-error-bars}
**Attach the plot of the** $\mathbf{5°}$ **and the** $\mathbf{10°}$ **data with the error bars to your report.**
:::

::: {.question #ph212-data-analysis:two-data-sets}
**What do you notice about the two sets of data? Do they seem distinct? How can you tell? Your answer should reference the error bars.**
:::

::: hint
- **Note that if the error bars for two measurements overlap, you cannot rule out the possibility that the measurements are the same.**
:::

## Part 4.2: Analyze the Data – Fitting

Fitting a function to a dataset is a key part of experimental work because it allows us to understand how the *dependent* variable relates to the *independent* variable. Most of the plots you’ll create will include a fit to your data. Fits are typically used to determine how well the data agrees with a particular (mathematical) model of the system’s behavior.

The correlation coefficient, *R^2^*, is one measure of how well the model fits the data. Values close to 1 signify that the fit does a good job of predicting the data, whereas values closer to zero signify that the fit poorly predicts the data. While there are no hard cutoffs, below 0.7 is indicative of a poor fit, and above 0.9 or 0.95 is generally indicative of a good or very good fit.

While you can use visual inspection to make rough evaluations of each trendline, *R^2^* is often useful for distinguishing among equally good-looking fits. Note that the *R^2^* value is just one of many ways to evaluate the quality of a fit. Other techniques include

::: {.question #ph212-data-analysis:trendline-plot}
**Create a new plot with just the** 5˚ **data. Use Excel's Trendline feature to try a few different trendlines (at least 2). Choose the one that fits best and remove the others before including the plot in your report. Be sure to include all of the elements of a complete plot listed in the box on the previous page.**
:::

::: hint
- If you need help, refer to the section on *Plotting and Fitting Data in the Excel Skills document.*
:::

::: {.question #ph212-data-analysis:trendline-chosen}
**What type of trendline did you choose to model the data? Did it match the data well or not? Explain.**
:::

## Part 4.3: Analyze the Data – Comparing to a Model

In many experiments, the goal is to check a hypothesis, or model, that describes certain physical situations. In physics, models are often expressed as an equation that relates different physical quantities to each other. One model for the period of a simple pendulum states that

$$T = 2\pi\sqrt{\frac{L}{g}}$$

where $g$ is the acceleration due to gravity. In other words, we are predicting that $T\  \propto$ (is proportional to) $\sqrt{L}$. If we plotted *T* vs. *L*, we would expect a nonlinear curve.

It is typically easier to tell if something is or is not a line (that is, see if two quantities are proportional to each other) than to evaluate if they have some other, more complicated relationship. If we have a prediction about the relationship between two quantities that is nonlinear, we can “force” a proportional relationship using a process called *linearization*.

::: box
### Linearization

In the context of data analysis, “linear” refers to a directly proportional relationship between the dependent and independent variables in an equation.

::: hint
- Mathematically, if two variables $x$ and $y$ have a linear relationship, we can express this as $y = mx + b$ where m and b are constants.
- More simply, we can write this as $y \propto x$ where $\propto$ means “is proportional to”.
- When graphed, data with a linear relationship falls on a straight line.
:::

**Linearization comes in handy when your data or hypothesis is *not* linear.**

When you fit data with a linear trendline, you are essentially checking whether the two variables are proportional to each other. To check a nonlinear hypothesis, can we instead check if one variable is proportional to *a function of* the other variable.

In practice, **linearization is done by calculating a new column of data,** that gives the values of a *function* of the input variable. Typically, the input variable is the independent variable, and the function is chosen so that the resulting quantity is proportional to the dependent variable.

### Why Linearize?

::: hint
- Linear data is typically easier to understand and analyze.
- There are analysis methods we can apply to linear data that don’t work as well (or at all) with nonlinear data.
- It is relatively easy to fit a line to data - there are just two important values to determine: the slope and intercept of the data.
:::
:::

::: {.question #ph212-data-analysis:linearized-plot}
**The given model predicts that T is proportional to** $\sqrt{\mathbf{L}}$ **. Create a linearized plot to test this relationship using the 5˚ data and an appropriate fit. Insert the plot into your report, with all the required elements.**
:::

::: hint
- If you need help with this process, ask your instructor! Linearizing is an important technique we’ll use throughout the course.
:::

## Part 5: Draw Conclusions

We can now compare the linearized fit to the best fit line that you first determined.

::: {.question #ph212-data-analysis:y-intercepts}
**Analyze the y-intercepts.**

a.  **Based on your understanding of pendulums (not an equation), what should the period be when** $\mathbf{L}\mathbf{= 0}$**? In other words, what should the y-intercept be? Explain your physical reasoning.**
b.  **What are the y-intercepts from the fits to your two plots of 5˚ data (general best fit and linearized)? Which more closely matches your physical expectations? Is the difference between the two significant?**
:::

::: {.question #ph212-data-analysis:compare-r-squared}
**Compare the linearized fit to the best fit you chose for the non-linearized data in question 11. Which one has a higher *R^2^* value? Is the difference between the two significant?**
:::

::: {.question #ph212-data-analysis:best-fit-conclusion}
**Considering both the R^2^ value and the y-intercepts, which fit seems to best represent the data, and why? What mathematical relationship does this indicate between T and L?**
:::

::: {.question #ph212-data-analysis:individual-reflection}
**Each lab member should write an individual concise paragraph reflecting on the lab. Identify each contribution by name. Each should specifically address the following:**

::: action
- **One new thing you've learned about analyzing data.**
- **Any unanswered questions you still have.**
- **Your comfort working with Excel as we continue in the course.**
:::
:::

## Part 6: Submit Your Group’s Lab Report

Make sure everyone’s name is on your group’s lab report. If you submit through Gradescope remember to add everyone in your group to the assignment. This is done at the end of the submission process.
