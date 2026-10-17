---
id: ph213-data-analysis-handout
title: "Lab 1 – Data Analysis"   # the original title text; see ledger 22
course: PH213
sequence: 1
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH213/Lab 1 - Data Analysis- Handout.docx"
source_sha256: "d634444391c35b3afc8bfe7808e19a5b73f69261c1d139779a240dd6c4ec3356"
status: converted
---

# Lab 1 – Data Analysis

### PH213 – General Physics with Calculus

**Experimental goal: Determine an equation that describes the electrostatic force using data from alternate universe.**

Many experiments start from a model or equation that needs to be tested. In this lab, you have been transported to an alternate universe where your physics knowledge no longer applies. Here you must instead use observations to try to develop a model of your own.

### Learning Objectives

**Learning goal: Learn and practice fundamental data analysis skills.**

This lab activity is designed to help you practice the following skills:

1.  Identify the qualities of a good group member

2.  Generate data needed to create a hypothesis.

3.  Linearize and fit simple functions to a data set.

4.  Determine a model equation for a system based on data.

### Equipment

::: action
- A computer with data analysis software (Excel & Graphical Analysis)
- *Excel Skills* document
:::

:::: box
#### As you work through the lab:

::: legend-question
1)  Numbered items reference things that need to be included in your lab report.
:::

::: action
- Bulleted items are activities or tasks you’ll need to do to answer questions.
:::

::: hint
- Items with an arrow are hints or suggestions.
:::

Boxed information is about either the expectations for your lab reports or key concepts for the course.
::::

## Installing Excel Software

All the lab computers have Excel installed on them, but you are welcome to work on your own computer if you prefer. Here is how to get Excel if you need it.

::: action
- Sign into Office 365 at [[https://is.oregonstate.edu/microsoft]{.underline}](https://is.oregonstate.edu/microsoft) using your ONID information.
- Click on the button on the top right that says "Install Office" and select "Office 365 apps".
- Follow the installation instructions to acquire Excel and any other Microsoft Office apps such as OneNote, Word, and PowerPoint.
:::

If you have trouble installing Excel, you may contact OSU help desk [[here]{.underline}](https://oregonstate.teamdynamix.com/TDClient/1935/Portal/Requests/TicketRequests/NewForm?ID=Dr9c0T7BaSI_). If you need help while going through this lab, reach out to peers in the class or your lab instructor.

If no one in your group can install a version of Excel, we recommend instead that you use Excel on the lab computer at your station.

### Part 0: Creating an Inclusive Learning Environment

We want to create an inclusive learning environment in lab, where everyone is able to contribute their ideas and feel respected by their peers.

::: {.question #ph213-data-analysis:group-member-qualities}
**In your lab group, list at least 3 qualities of a good group member. Put these in your lab report. Choose one to share with the class. Keep the others as backup contributions in case your first idea gets suggested by another group.**
:::

### Part 1: Create a Model

One day while working in the Wormhole, your entire lab group is transported through an actual wormhole to an alternate universe in which the laws of physics are not necessarily the same.

Abandoning your homework on the force between electric charges, which was based on the physics you had learned in your original universe, your group decides to determine this force in your new universe.

You observe that there are both positive and negative charges in this new universe, just as back home. From qualitative observation you can see that the force depends on both the charges *Q* and the distance *d* between them, though not quite like you’re used to. You suspect that the force depends on the charges and distance to different powers:

$$F = kQ_{1}^{\alpha}Q_{2}^{\beta}d^{\gamma}$$

where *k, α, β,* and *γ* are constants. **You decide to test this model by measuring the force for different combinations of charge and distance.**

Fortunately, your computer has access to a “[Force Calculator](http://osu-physics-lab.github.io/)” that will tell you the vector force between charges for any combination of charges and distance *(not* displacement)*.* The calculator uses the same sign convention as in our universe; positive is repulsive, and negative is attractive.

::: action
- Note: The Force Calculator includes random uncertainty, just as if you had to physically measure the force.
:::

**Your objective is to collect data using the Force Calculator to determine an equation you can use to predict the force for any combination of**

::: action
- **Charge 1 (*Q~1~*)**
- **Charge 2 (*Q~2~*)**
- **Distance (*d*)**
:::

**as well as the force constant (*k*).** Note that *k* in this universe is *not* the Coulomb constant!

Remember that force is a vector, so your equation should predict not only magnitude, but also whether the force is attractive (negative) or repulsive (positive).

Although your data is supplied electronically, you should design your experiment as if you were using real equipment. That includes multiple trials and separate runs to examine each variable under your control.

### Part 2: Collect Data

::: {.question #ph213-data-analysis:experiments-to-run}
**Describe the experiments you will run. Since you have a data generator, you don’t need to describe the experimental setup. But your description should list the independent variable(s) you will examine, what you will keep constant in each case, and why you’ve made these choices.**
:::

:::: box
#### What is Uncertainty?

*Uncertainty* is the acknowledgement that we cannot measure things exactly, and so any conclusion based on measurements will always include a range of possible answers. When making a measurement, there is no single “true value” of the measurand (measured quantity) that we can determine. Instead, we can define an interval that defines the range of values that we think are *probable* for the measurand. The narrower the interval, the more precisely we can approximate the measurand.

When including uncertainty in a value, we report it as **A ± Δ~A~**. We believe the value is **A**, but we’re unable to rule out the possibility that it’s higher or lower by an amount **Δ~A~**. (Sometimes it’s written +Δ~1~ / -Δ~2~ if the higher and lower ranges are different.) For example, a time might be reported as 2.45 s ± 0.03 s.

There are two main kinds of uncertainty: *measurement uncertainty* (from sources such as your judgement in reading analogue instruments and the rating or stated calibration of the instrument) and *statistical uncertainty* (variations in repeated readings made under apparently identical conditions).
::::

When recording data, we also want to keep track of the uncertainty in our measurements. In this lab, our data is being provided by a force generator, so we have no way of knowing what the measurement uncertainty is. However, we can still take repeated measurements and use this to find the statistical uncertainty.

::: {.question #ph213-data-analysis:data-tables}
**Create a data table for each run. (A run is a set of values for one independent variable.) Included with each table should be the values of other parameters that you hold constant. You'll need multiple runs to get an idea of the statistical uncertainty in the results. Include your data tables in your report.**

::: hint
- **One method for calculating statistical uncertainty is to take half of the difference between the largest and smallest measurement you made.**
- **Another method is to calculate the standard deviation of your measurements.**
:::
:::

### Part 3: Analyze the Data

[A few reminders about making and using plots to analyze data.]{.underline}

Whenever you create a plot, you should

::: action
- Evaluate if the plot makes sense. Are the axes correct? Do you have the right number of data points?
- Include a descriptive title and labels on each axis, always including physical units.
- Add a legend, unless you only have one set of data and the title describes it.
:::

You will want to fit a trendline to test your data. You can try a trendline based on expectations from a hypothesis. Or you can try functions that seem like they should fit the data.

One way to see which function fits best is to check the correlation coefficient, *R^2^*. Values close to 1 signify that the fit does a good job of predicting the data, whereas values below (roughly) 0.8 signify that the fit poorly predicts the data. Another thing to check is the y-intercept. Does it make physical sense for the system you’re examining?

**When examining fits, you may want to *linearize* your data. (It’s relatively easy to fit a line to data; there are just two important values to decide: the slope and intercept of the data.) The appendix at the end of the handout describes linearization.**

If you need help working with Excel refer to the section on Plotting and Fitting Data in the *Excel Skills* document or talk with your Instructor.

::: {.question #ph213-data-analysis:analysis-plots}
**Create plots to analyze your data. For each plot, be clear what is plotted, which fits you tried, which fit you ultimately chose, and why.**

::: action
- **When possible, add error bars to your plots to represent the uncertainty. Error bars are not required for linearized plots.**
:::
:::

[To add error bars to a plot in Excel:]{.underline}

1.  Click the data set you want to add error bars to, and then under “Chart Design”, select “Add Chart Element” → “Error Bars” → “More Error Bar Options”

2.  Both horizontal and vertical error bars will be added. We usually just want vertical error bars, so select the horizontal error bars and delete them

3.  Under “Format Error Bars” → “Error Amount” select “Custom”

4.  Click “Specify Value” and highlight the uncertainty values for both the positive and negative error bar values

5.  Repeat for each dataset that needs error bars

### Part 4: Conclude and Reflect

::: {.question #ph213-data-analysis:force-conclusions}
**Report your conclusions about the electric force in this universe. Include an equation that can be used to calculate the force for any given pair of charges *Q~1~* and *Q~2~* at a known distance *d* from each other, with a specified value for the force constant *k*. The equation should indicate direction, or you should state the direction of the force. Explain how your analysis led you to this equation.**
:::

::: report-item
**Think about your result:** What does it say about Newton’s laws in this universe? Does your result seem to violate any of Newton’s laws?
:::

::: {.question #ph213-data-analysis:individual-reflection}
**Each lab member should write an individual concise paragraph reflecting on the lab. Identify each contribution by name. Each should specifically address the following:**

::: action
- **One new thing you've learned about analyzing data.**
- **Any unanswered questions you still have.**
- **Your comfort working with Excel as we continue in the course.**
- **What things your group did well today to ensure inclusion of everyone in the group.**
:::
:::

### Part 4: Submit Your Group’s Lab Report

Make sure everyone’s name is on your group’s lab report. If you submit through Gradescope remember to add everyone in your group to the assignment. This is done at the end of the submission process.

### Appendix: Linearizing Data

In the context of data analysis, “linear” refers to data that is directly proportional. When graphed, this data falls on a straight line. Linear data is typically easier to understand and analyze, and there are methods we can apply to linear data that don’t work as well (or at all) with nonlinear data. **It is relatively easy to fit a line to data - there are just two important values to decide: the slope and intercept of the data**.

You can use this method even when the relationship between the variables is not linear. The "trick" is to find combinations of independent and dependent variables such that when you plot them the relationship is linear. We refer to this as *linearizing the data*, and it allows us to apply the tools we have for working with linear data to relationships that are not linear.

To do this, you must start by forming a hypothesis about the data. You might get this from a physical model, or you might get it by looking at a graph. Either way, you want to have a hypothesis that tells you how the y-value depends on the x-value.

[An Example]{.underline}

A hypothesis for the acceleration of a ball rolling down a ramp says acceleration should be proportional to the sine of the ramp angle. That means we could write a formula for the acceleration of the form

$$a\  = \ m\ \sin(\theta)$$

where m is some unknown number. If we plot *a* vs angle *θ* we would expect to see a sine curve. Simple software like Excel is not able to fit to a sine curve.

But if we plot *a* vs. *sin(θ)*, then we would expect a straight line. We do this by calculating the sine of the angle for each *θ*, and then y graphing *a* on one axis and $sin(\theta)$on the other axis. If we represent the function $sin(\theta)$ as simply $x$, then our graph would be of the form

$$a\  = \ m\ x$$

which is just the equation for a line! This is easy to fit, and then $m$ is just the slope of our line.
