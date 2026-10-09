---
id: ph212-hypothesis-testing-handout
title: "Lab 4 – Hypothesis Testing"   # the original title text; see ledger 22
course: PH212
sequence: 4
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH212/Lab 4 - Hypothesis Testing - Handout.docx"
source_sha256: "8bdb32d3f8eb751bdd6f8d795bcce11247addb395a283e0c34447c1d7f9fc42a"
status: converted
images:
  - file: "ph212-hypothesis-testing-handout-media/connection-icon.png"
    source_part: "word/media/image1.png"
    sha256: "d71d2df031ec532d9a6da88703c2dc8b097733a7597076e05836fc65bc2c7541"
---

# Lab 4 – Hypothesis Testing

## PH212 – General Physics with Calculus

**Experimental goal: Develop and test a model of the relationship between the oscillation period of a cart on a ramp and the ramp angle.**

::: box
In a reliable **scientific experiment**, you should:

::: action
- Identify the quantity or quantities to measure – the dependent variables.
- Identify the quantity to control and change – the independent variable. A good experiment changes only one quantity at a time, so that it’s clear what causes any changes to the dependent variables.
- Identify the quantities to be held constant. These are the things that shouldn’t be changed from trial to trial so that you can expect the same outcome each time. While your outcome will in fact vary, if you’ve done a good job here the variations should be small. (Large variations are often a sign of something unexpected.)
- Describe your experimental set-up, explaining what is held constant, how you’ll vary the dependent variable(s) and over what range, and how you’ll measure the independent variable. Often, this will include a well-labeled diagram.
- Perform multiple trials, in which you repeat the same experiment, taking data each time.
:::
:::

## Learning Objectives

**Learning goal: Use your experience in physics to develop your own hypothesis and design and perform an experiment to check its validity.**

This lab activity is designed to help you practice the following skills:

1.  Predict dependence of data on particular variables.
2.  Choose an appropriate model of a physical system to be tested.
3.  Determine what data needs to be collected.
4.  Use quantitative evidence such as R^2^ value for a particular fit to support conclusions.

## Equipment

::: action
- Digital cart (with attachable masses)
- Track
- Spring(s) and mounts
- Meter stick
:::

::: hint
- When resting the cart on the table, put it on its side or upside-down - not on its wheels. When placed on its wheels, it might roll off the table and break. These carts are expensive to replace!
:::

## Part 0: Characterize the system

We will begin by investigating oscillations using the cart and spring. Although we use a cart in this activity to minimize friction, over longer times the effects of friction become evident and cause damping (the amplitude of the oscillation decreases).

For this lab, you’ll keep the time scales short enough that friction isn’t significant. This allows us to say that damping is negligible (small enough to ignore).

::: box
### How to connect carts to Graphical Analysis

When connecting wireless sensors in Graphical Analysis, do *not* connect using the computer’s Bluetooth settings. Connection should be done through the Graphical Analysis app either when it’s opened or by clicking on the Connection icon ![](ph212-hypothesis-testing-handout-media/connection-icon.png){width="0.3229in" height="0.2363in"} in the lower right corner.
:::

Before we can conduct any experiments, we want to make sure we fully understand the system that we are working with. This includes determining the values of any important physical parameters. For any spring-based oscillator that includes the spring constant.

::: {.question #ph212-hypothesis-testing:spring-constant-method}
**Describe a method to find the spring constant of the spring that you are using. We don’t want to make any assumptions about periodic motion (yet), so the method that you use should rely on physical principles other than oscillations.**
:::

::: {.question #ph212-hypothesis-testing:spring-constant-value}
**Collect and analyze the data using the method you outlined. What is the spring constant?**
:::

::: {.question #ph212-hypothesis-testing:ideal-spring}
**One of the assumptions in our model for oscillating springs is that the spring is ideal. That is, we assume force is directly proportional to displacement and the spring constant does not depend on displacement (Hooke’s law). Does this appear to be true for your spring? Support your answer with evidence.**
:::

## Part 1: Develop a Model

Using the spring and cart, make an oscillator on an inclined plane. Discuss with your lab group the physics principles related to the problem. In particular, we are interested in how the oscillation period depends on the angle of the ramp.

::: {.question #ph212-hypothesis-testing:sketch-and-hypothesis}
**Sketch a mass connected to a spring on an inclined plane. Use your sketch and your understanding of the relevant physical principles to predict whether and how the oscillation period will depend on the angle of the track. This is your hypothesis, or model.**
:::

## Part 2: Plan your Experiment

Now design a reliable experiment using the available equipment to check your prediction. Remember that a good experiment repeats a test many times and explores a wide range of values for the independent variable.

::: {.question #ph212-hypothesis-testing:describe-experiment}
**Describe your experiment.**

a.  **Include a clearly labeled diagram of your experimental set-up.**
b.  **Identify the independent and dependent variables, as well as any quantities or conditions that will be held constant.**
c.  **Describe your procedure for data collection.**
:::

::: {.question #ph212-hypothesis-testing:analysis-plan}
**Describe how you will analyze your data. Make sure you address how you will be able to tell if the data supports your prediction about the dependence of period on angle.**
:::

## Part 3: Collect Data

Now you’re ready to run your experiment.

::: {.question #ph212-hypothesis-testing:record-observations}
**Perform the experiment and record your observations in a clear form. If there are any significant sources of measurement uncertainty in the dependent variable, estimate and record those values as well and state the sources.**
:::

::: {.question #ph212-hypothesis-testing:statistical-uncertainty}
**Find the statistical uncertainty in your measurement for each value of the dependent variable. If you identified other significant sources in the previous question, add all of these in quadrature to find the total uncertainty.**
:::

## Part 4: Analyze the Data

::: {.question #ph212-hypothesis-testing:analyze-results}
**Analyze your results to check your prediction. Include any plots that you create and describe what the plots show.**
:::

## Part 5: Conclude and Reflect

::: {.question #ph212-hypothesis-testing:conclusion}
**Draw a conclusion about the dependence of period on angle. Support your conclusion using your data and compare it to your prediction. If your prediction wasn’t correct, discuss where you think your reasoning may have gone astray and propose a revised explanation.**
:::

::: {.question #ph212-hypothesis-testing:applies-universally}
**Can the conclusions you drew from this experiment be applied universally? That is, do all oscillating objects on a spring follow the model or prediction you discussed in the previous question? If not, give an example of a case that may not be described by your model.**
:::

## Part 6: Submit Your Group’s Lab Report

Make sure everyone’s name is on your group’s lab report. If you submit through Gradescope remember to add everyone in your group to the assignment. This is done at the end of the submission process.

## Appendix – Reference Information

This section contains key information from previous labs.

1.  Required Plot Elements
2.  What Is Uncertainty?
3.  Sources of Uncertainty
4.  Linearization
5.  Assumptions

### Required Plot Elements

::: action
- Do not connect the data points with lines.
- Make sure you create *Scatter Plots* and not *Line Plots*.
- Evaluate if the plot makes sense. Are the axes correct? Do you have the right number of data points?
- Include a descriptive title and labels on each axis, always including physical units.
- Add a legend, unless you only have one set of data and the title describes it.
- Display the equation and R^2^ value for any trendline you include.
:::

### What is Uncertainty?

*Uncertainty* is the acknowledgement that we cannot measure things exactly, and so any conclusion based on measurements will always include a range of possible answers. When making a measurement, there is no single “true value” of the measurand (measured quantity) that we can determine. Instead, we can define an interval that defines the range of values that we think are *probable* for the measurand. The narrower the interval, the more precisely we can approximate the measurand.

When including uncertainty in a value, we report it as **A ± Δ~A~**. We believe the value is **A**, but we’re unable to rule out the possibility that it’s higher or lower by an amount **Δ~A~**. (Sometimes it’s written +Δ~1~ / -Δ~2~ if the higher and lower ranges are different.) For example, a time might be reported as 2.45 s ± 0.03 s.

### Sources of Uncertainty

The uncertainty in a measurement can be due to a combination of several factors. A crucial aspect of experimentation is to identify all such sources of uncertainty and to numerically estimate their effect on your measurement result.

Common sources of uncertainty include:

1.  your judgement in reading analogue instruments
2.  the effects of environmental conditions on the measurement
3.  the sensitivity of your instruments (e.g. a digital scale, a meter stick)
4.  the rating or stated calibration of the instrument
5.  approximations and assumptions that you make while doing the experiment
6.  variations in repeated readings made under apparently identical conditions (statistical uncertainty)

A measurement uncertainty is not meant to be an indication of “mistakes” that you might make in an experiment. If you are aware that you have made a mistake, then you should repeat your experiment. **“Human error” is not a valid source of uncertainty**. If you know that you did something “wrong”, then the right course of action is to redo it correctly.

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

**Why Linearize?**

::: action
- Linear data is typically easier to understand and analyze.
- There are analysis methods we can apply to linear data that don’t work as well (or at all) with nonlinear data.
- It is relatively easy to fit a line to data - there are just two important values to determine: the slope and intercept of the data.
:::

### Assumptions

A hypothesis typically includes assumptions about the situation being modeled. This could be ignoring a force or assuming it’s constant, or making some other simplification.

For example:

::: action
- In free fall, we assume air resistance is negligible (so small that its effects can be ignored).
- Hooke’s law assumes the elasticity of a spring is constant – the spring constant.
- Calculations of Earth’s gravity may assume a perfectly spherical planet.
:::

These assumptions may or may not be justified. For example:

::: action
- A billiard ball on Earth falls for at least short distances with an acceleration of g, the same as in a vacuum, as if there were no air. Assuming air resistance is negligible is valid when considering its motion.
- A sheet of paper falls much more slowly. The assumption that air resistance is negligible is not valid – predictions made from a model that ignores air resistance will not match what is observed.
:::

Identifying, justifying, and checking assumptions is an important part of an experiment.
