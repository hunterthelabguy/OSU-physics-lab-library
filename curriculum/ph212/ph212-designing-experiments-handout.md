---
id: ph212-designing-experiments-handout
title: "Lab 3 – Designing Experiments (2 weeks)"   # the original title text; see ledger 22
course: PH212
sequence: 3
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH212/Lab 3 - Designing Experiments - Handout.docx"
source_sha256: "4713cbfe3ebb4e3cdb2fe2ef80534268122710295b65c9b56ae18a87418ac76f"
status: converted
images:
  - file: "ph212-designing-experiments-handout-media/excel-linest-entry.png"
    source_part: "word/media/image3.png"
    sha256: "c1780b525dfb75b82a35a2a45e8e329389f45c132621068f1f7d0bceb778e883"
  - file: "ph212-designing-experiments-handout-media/excel-linest-output.png"
    source_part: "word/media/image4.png"
    sha256: "fd741e1f619325033a14d34fdda0682abde6956a971f00bb528137f8b7b9724f"
---

# Lab 3 – Designing Experiments (2 weeks)

## PH212 – General Physics with Calculus

**[Experimental goals]{.underline}**

**Week 1: Explore different methods of collecting data to identify the best experimental design to answer a given question.**

**Week 2: Determine the moment of inertia of a flywheel.**

This is a two-week lab. The first week, you will develop a model of the system, determine how the moment of inertia relates to quantities you can measure, and explore physical considerations before coming up with an experimental design.

The second week, you will collect data using the procedure you determined, calculate the moment of inertia (with uncertainty), and use the experimental value to predict future motion of the flywheel.

## Learning Objectives

**[Learning goals]{.underline}**

**Week 1: Evaluate and compare different measurement methods with a goal of minimizing uncertainty in data.**

**Week 2: Understand what it means to find an experimental value for a quantity of interest and evaluate the validity of experimental results.**

This lab activity is designed to help you practice the following skills:

1.  Understand relationship between measurements and quantities of interest.
2.  Design experimental procedures to mitigate uncertainty.
3.  Identify simplifying assumptions and understand when they are appropriate.
4.  Use a model to predict experimental results.
5.  Extract physical parameters from fits to a model, e.g., the slope of a graph.

## Equipment

::: action
- Flywheel
- String
- Mass hanger (50 g) and masses
- Meter stick and calipers
- Masking tape
- Stopwatch
- Motion detector and shield
- Photogate and table clamp
:::

## Week 1 – Exploring the system

### Introduction: Designing a Combustion Engine

You are a team of engineers helping design a combustion engine in the industrial era. One key component of your design is the flywheel, but you need to know the moment of inertia very precisely. The moment of inertia of a disk or cylinder can be easily calculated using formulas. But because your flywheel has several pieces and is partly hollow this approach isn’t as accurate. So the project supervisor has asked you to find the value experimentally.

**Your first task is to investigate the system (in this case, a flywheel and a mass) and determine the best procedure for collecting data** for the ultimate goal of determining the moment of inertia of the flywheel. We will also be considering assumptions about the system and seeing when they are valid. Remember, part of being a good scientist is being willing to change your thinking in response to new information, so don’t feel like you need to stick with the first procedure that you come up with.

The system we will start with is a mass hanging from a string wound around the center post of the flywheel. When you release the mass, it will increase the angular speed of the flywheel as it falls. Conversely, if the string winds up it will slow down the flywheel.

### Part 1: Build a Model

We start by building a model of this system identifying all the forces that act on the flywheel. With this model you can relate the moment of inertia of the wheel to the motion of the wheel and the hanging mass:

$I\alpha = mgr - mar$ \[Initial model equation\]

where $I$ is the moment of inertia of the flywheel, $m$ is the mass hanging from the string, $\alpha$ is the angular acceleration of the wheel, $a$ is the linear acceleration of the hanging mass, and $r$ is the distance from the attachment point of the string to the axis of rotation.

We show how to find this equation at the end of this handout. It makes use of the fact that the rotation of the flywheel is related to the linear acceleration of the mass by

$a = \alpha r$

\[The general form of this equation includes a factor of *sin(θ)*. Since we defined *r* as the perpendicular distance from the axis to the string, *sin(θ) = 1*.\]

::: {.question #ph212-designing-experiments:model-variables}
**In the model equation**

a.  **Which quantity might be used as the independent variable in an experiment to find the moment of inertia? That is, what can you change in a controlled way?**
b.  **Which two quantities might be the dependent variable in an experiment? That is, what could you measure as you change the independent variable?**
:::

::: {.question #ph212-designing-experiments:dependent-variables-relation}
**How are the dependent variables that you identified related to each other – what is the equation that expresses one in terms of the other?**
:::

::: {.question #ph212-designing-experiments:implicit-assumption}
**There is a physical assumption implicit in our model equation. What is it? (Look for a physical quantity you would expect to affect the system, but that is not in the equation.)**
:::

### Part 2: Explore the Physical System

**Your goal in this part of the lab is to explore different ways of collecting data to select the method that works “best,” where you decide what that means based on your explorations.**

When designing an experiment, it is typically important to explore the system before creating your experimental procedure. You can’t always know exactly what you need to test until you start trying things out. So we will start with an exploration of the system.

::: hint
- **It won’t be necessary to run a full set of trials.** Multiple trials are needed only to determine statistical uncertainty, and 3 or 4 should be enough. Your objective is not to take data, but simply to analyze the uncertainty in the data from each method so you can decide which to use for your experiment.
- **You are *not* trying to find the moment of inertia this week.** You are only designing the experiment you will use next week to do that.
:::

::: box
#### Estimating Measurement Uncertainty

We will be estimating uncertainty in linear and angular accelerations measured by different methods to help determine which method is best.

1.  Start by determining the uncertainty in your measurement.
    a.  If you choose to measure the acceleration directly in Graphical Analysis, GA will also give you the uncertainty. You can either i) take half of the range between the minimum and maximum or ii) have GA calculate a standard deviation. To get this information, highlight the region of the graph with your data and click “View Statistics”. (If you don’t highlight any data, GA will analyze the entire graph.)
    b.  If you choose to find acceleration from the slope of the velocity vs. time data, Graphical Analysis can give you the uncertainty in the slope. After you click “Apply Fit”, select “Options”, and check the box to show the uncertainty in the fit parameters.
    c.  If you calculate the acceleration from measured data (e.g., time), you can find both the acceleration and its uncertainty by
        i.  Estimate the uncertainty in your measurement.
        ii. Calculate the acceleration using the measurement *minus* its uncertainty.
        iii. Calculate the acceleration using the measurement *plus* its uncertainty.
        iv. The acceleration is an average of the two accelerations you just calculated. The uncertainty in acceleration is half of the difference between them.
:::

**[Measuring linear motion]{.underline}** – by hand and with a motion detector

::: {.question #ph212-designing-experiments:linear-by-hand}
**Using your knowledge of linear kinematics, find the acceleration of the hanging mass as it falls using only hand-based measurement tools (*no computer-related data collection equipment*).**

a.  **What quantities will you measure and how will you calculate acceleration?**
b.  **What sources do you expect to contribute significantly to the uncertainty in a single measurement of the time? List the source(s) and estimate a value for each. If there is more than one source, find the total measurement uncertainty by adding in quadrature.**
c.  **Use the method described above (under Estimating Uncertainty) to estimate the uncertainty in the acceleration. Note that because you are only doing a single measurement, there is no statistical uncertainty. Report the average acceleration you found in the $\mathbf{A \pm \mathrm{\Delta}A}$ format.**
:::

::: {.question #ph212-designing-experiments:linear-motion-detector}
**Now connect the motion detector to the computer. Set the switch on the detector to the cart. Use the motion detector to determine the acceleration of the mass as it falls.**

a.  **What quantity is the motion detector measuring directly and what quantities are being calculated in Graphical Analysis? How will you find a value for the average acceleration from the data it records?**
b.  **Use the method described above (under Estimating Uncertainty) to estimate the uncertainty in the acceleration.**
c.  **Report the average acceleration you found in the $\mathbf{A \pm \mathrm{\Delta}A}$ format.**
:::

Now compare the measurements you got using each method to determine which is more reliable – which is more consistent over time and more consistent from run to run. Don’t get caught up in the number of digits provided by the measuring instrument. Focus on the precision to which you believe the results.

::: {.question #ph212-designing-experiments:compare-linear}
**Compare the two linear accelerations that you found. What are the total uncertainties in the two measurements? Which method seems like the better choice for your experiment and why?**
:::

Before going on, save any data you may want to access later.

**[Measuring rotational motion]{.underline}** – by hand and with a photogate

::: action
- Disconnect the motion detector from the computer. Connect the photogate.
:::

::: hint
- If Graphical Analysis doesn’t recognize the photogate, close the application and restart it.
:::

::: {.question #ph212-designing-experiments:rotational-by-hand}
**Using your knowledge of rotational kinematics, find the angular acceleration of the flywheel while the mass is falling using only hand-based measurement tools (*again, nothing computer-related*).**

a.  **What quantities will you measure and how will you calculate the angular acceleration?**
b.  **What sources do you expect to contribute to the uncertainty in a single measurement of the time? List the source(s) and determine a value for each, then find the total measurement uncertainty.**
c.  **Use the method described above (under Estimating Uncertainty) to estimate the uncertainty in the acceleration, including statistical uncertainty. Then report the average acceleration you found in the $\mathbf{A \pm \mathrm{\Delta}A}$ format.**
:::

::: {.question #ph212-designing-experiments:rotational-photogate}
**Now connect the photogate to the computer. In Graphical Analysis, set the mode to “Angular Motion”. Check that the number of spokes is set to one. Use the photogate to determine the angular acceleration of the flywheel.**

a.  **What quantity is the photogate measuring directly and what quantities are being calculated in Graphical Analysis? How will you find a value for the average angular acceleration from the data it records?**
b.  **Use the method described above (under Estimating Uncertainty) to estimate the uncertainty in the acceleration.**
c.  **Report the average acceleration you found in the $\mathbf{A \pm \mathrm{\Delta}A}$ format.**
:::

Compare the two measurement methods using the same ideas as before.

::: {.question #ph212-designing-experiments:compare-rotational}
**Compare the two rotational accelerations that you found. What are the total uncertainties in the two measurements? Which method seems like the better choice for your experiment and why?**
:::

::: hint
- [When you are done taking data, unplug your sensors from the LabQuest Mini box.]{.underline}
:::

### Part 3: Design the Experiment

You should now be ready to select a dependent variable for your experiment.

**[Rewrite the model equation]{.underline}**

Start by making sure your model equation is written in a form that expresses the dependent variable in terms of the other quantities of the experiment (the independent variable and constants). *There should only be one dependent variable left in your equation!* This means we will need to use the expression $a = \alpha r$ to eliminate either *α* or *a* from the model equation.

::: {.question #ph212-designing-experiments:rearranged-model}
**Choose whether to measure linear or angular acceleration and rearrange the model equation to isolate the dependent variable you chose. This should be the only quantity on the left side of the equation, and it should not appear on the right side of the equation. When you’re done, you should have an equation of the form:**

**dependent variable = function of (independent variable and parameters)**

**in which only *α* or *a* are present, but not both. Again, the only thing on the left-hand side should be the dependent variable you chose, and the only things on the right-hand side should be quantities you can control.**
:::

#### Create a procedure

::: action
- Design an experiment to check your model equation and to use it to find the moment of inertia. In it you should vary the independent variable and measure the dependent variable. Remember to restrict yourself to values of the independent variable that allow you neglect friction.
:::

::: box
#### Describing an Experiment

A good description includes all the details needed for someone reading your report to reproduce your experiment. Typically, that includes your equipment. For this course you can assume the reader has access to the same equipment as you, so you don’t need to describe it in detail. But you should mention which equipment you use and how you use it.

::: hint
- It is helpful to write your procedure as a list of steps that can be followed.
- Describe how to set up the equipment, how to collect data for one trial, which conditions should be tested, and how many trials will be done for each condition.
:::

Describing your experiment well is part of all the labs in this course, not to mention all well-documented scientific experiments.
:::

::: {.question #ph212-designing-experiments:procedure}
**Read the box above on how to describe an experiment. Then, write a procedure for your experiment. Be sure to include:**

::: action
- **What will you hold constant and their values, if you determine them.**
- **The independent variable you will change in a controlled manner, and what range of values you will test.**
- **Which dependent variable will you measure and what you will calculate.**
:::
:::

::: hint
- Remember that a good experiment includes multiple repetitions of each instance to improve the accuracy of the results.
:::

### Part 4: Submit Your Group’s Lab Report

Make sure everyone’s name is on your group’s lab report. If you submit through Gradescope remember to add everyone in your group to the assignment. This is done at the end of the submission process.

**STOP HERE: This concludes the lab activities for the first week.**

**Submit your lab report for this week.**

## Week 2 – Determining the moment of inertia

We are going to continue our investigation of the moment of inertia of the flywheel that we began during the last lab. Last time we looked at an initial model of the system and explored the physical system to develop an experimental procedure. **This week we will collect data to determine the moment of inertia and validate the calculated value by using it to predict additional accelerations. We will also check some of the underlying assumptions in your model.**

### Part 1: Plan your Analysis

Your model equation is likely *not* linear in the independent variable. While you can investigate a nonlinear model, it can be helpful, when appropriate, to simplify the equation and find a model equation that *is* linear in the independent variable.

1.  Identify where the independent variable occurs in your equation. It may occur more than once, but it should only be to the right of the equal sign.
2.  Which terms would you need to eliminate to make your equation linear in this variable?
3.  By eliminating these terms, you are making an approximation. What should be true physically in order for you to justify this approximation (i.e., for the approximation to be a good one)? Consider the value of masses, radii, distances, etc. in your system. Do you think the approximation you identified is physically valid for the system you’re investigating?
4.  If so, you can eliminate some terms to make your model linear.

::: {.question .restart #ph212-designing-experiments:simplified-model}
**Rewrite your model equation from the end of last week using the approximation(s) needed to simplify it. Explain the approximation that you made.**
:::

**\*\*\* Check in with your instructor to make sure your equation is on the right track before proceeding \*\*\***

One way of checking the validity of the approximation is to proceed as if it were true, and then check the data to see if it is linear as expected. This is what we will do.

Now consider your simplified model equation. It should contain the moment of inertia. This moment is constant throughout the experiment; it’s a parameter related to your equipment. How can you use your data to determine the moment of inertia?

::: hint
- Hint: If your system is linear as expressed by your model, it means a plot of the dependent vs. independent variable will be a straight line.
:::

::: {.question #ph212-designing-experiments:inertia-method}
**Describe how you can use your simplified equation to determine the moment of inertia of the flywheel. What graph(s) will you need to make? What part of the graph(s) will allow you to calculate the moment of inertia? How?**
:::

### Part 2: Check your Assumptions

You have made two assumptions about the system. We should check their validity.

Our model is based on an assumption that the (slowing) acceleration due to friction in the flywheel is negligible. This needs to be checked.

::: {.question #ph212-designing-experiments:friction-check}
**Start the flywheel spinning slowly. Check if you can measure any (slowing) acceleration due to friction. Describe what you found and how. Compare the size of any acceleration due to friction to the acceleration from the hanging mass. What values of the independent variable (mass) will allow you to neglect friction? What *quantitative* criteria did you use to make this decision?**
:::

::: hint
- **The mass hanger itself is 50 g.**
:::

::: {.question #ph212-designing-experiments:other-assumption}
**What other assumption did you make today to simplify the model equation? Comment on its validity in your experiment. . What values of the independent variable (mass) are necessary for this assumption to be valid? What *quantitative* criteria did you use to make this decision?**
:::

::: {.question #ph212-designing-experiments:mass-range}
**Use the above to choose a range of values you will test when you perform the full experiment. Explain how you made this decision by referencing your previous answers about assumptions**
:::

### Part 3: Collect Data

::: {.question #ph212-designing-experiments:data-table}
**Perform your experiment and record the data in a table that you include in your report. At this point you should be reporting only data that you measure, not calculated data. All data should be from this week, not your exploratory activities last week. Be sure to include the uncertainty for each measurement. (Refer to last week for a reminder of the uncertainty associated with the methods you chose.)**
:::

NOTE: You should be varying the mass as your independent variable. You chose a range of masses to use so that you could neglect friction but not significantly affect the moment of inertia of your system. Make sure the masses you use masses in this range.

::: {.question #ph212-designing-experiments:procedure-review}
**Now that you have run your experiment, was any part of your description unclear? Are there additional details that you think should have been included? If so, discuss them here.**
:::

### Part 4: Analyze the Data

Analyze your data. Here is where you calculate quantities and create plots useful for exploring the model.

::: {.question #ph212-designing-experiments:plot}
**Create a plot of the independent variable vs. dependent variable, complete with any fits you will use, and add it to your report.**
:::

::: {.question #ph212-designing-experiments:graph-description}
**Give a written description of your graph. What does it show? Does your data follow your model? In particular, is your data linear? How do you know?**
:::

::: {.question #ph212-designing-experiments:moment-of-inertia}
**Find moment of inertia:**

a.  **Use your graph to determine a single, final [result for the moment of inertia based on *all* your data.]{.underline} Explain and/or show how you found this result.**
b.  **Use one of the methods below to find the uncertainty in the slope. State what method you used and report the value.**
c.  **Because the slope is equal to the moment of inertia multiplied by constants that don’t have significant uncertainties, the *relative* uncertainties of the slope and moment are equal. Mathematically:**

    $$\frac{\mathbf{\mathrm{\Delta}}_{\mathbf{slope}}}{\mathbf{slope}}\mathbf{\approx}\frac{\mathbf{\mathrm{\Delta}}_{\mathbf{I}}}{\mathbf{I}}$$

    **Use this equation to determine the uncertainty in the moment of inertia.**
:::

#### Finding uncertainty in a slope:

1.  Using Graphical Analysis: Highlight the data on the plot and select “Apply Fit”, then hit the options button and select the “Display Fit Parameters” box.

    ![](ph212-designing-experiments-handout-media/fit-options.svg){.drawn drawings="484604076 2090172472 475339996 389621496" label="Two Graphical Analysis screenshots. Left, a linear fit's results box, with an arrow pointing to the gear button in its lower right corner. Right, the Fit Options dialog that button opens, with an arrow pointing to its checkbox, Show Uncertainty of Fit Parameters."}

2.  Using Excel: Type the function shown below into a cell in your Excel spreadsheet.

=LINEST(*y-data range*, *x-data range*, TRUE, TRUE)

![Excel sheet with two columns of data on the left and the LINEST function on the right](ph212-designing-experiments-handout-media/excel-linest-entry.png){width="3.2028in" height="1.4833in" crop="0 3262 0 0"}

The function outputs two columns of values. The uncertainty in the slope is the second box down in the left column.

![Output of the Excel LINEST function. An arrow labeled "slope" is pointing to the first cell in the first column, and an arrow labeled "uncertainty in slope" is pointing to the second cell in the first column. ](ph212-designing-experiments-handout-media/excel-linest-output.png){width="2.8705in" height="1.3083in"}

### Part 5: Check the Validity of the Model

We can’t measure the moment of inertia of the flywheel directly, but we would still like to validate our results. Using results to make predictions is one way of doing so. Once again, we use the hypothesis to make a prediction, this time in our new situation, and then take data to see if the prediction is correct. If it does, we’ve extended the reach of our model. If it doesn’t, we have found limits to our model.

::: {.question #ph212-designing-experiments:prediction}
**Pick a value of accelerating mass that you *did not* use when taking data in Part 1. Think about whether you want this mass to be within the range of values you tested or outside the range.**

a.  **Calculate an expected acceleration for that mass using your experimental value for the flywheel’s moment of inertia. Show symbolically the equation you used to do so and report your answer.**
b.  **Calculate the range of possible accelerations for the minimum expected moment of inertia ($\mathbf{I - \mathrm{\Delta}I}$) and the maximum expected moment of inertia ($\mathbf{I + \mathrm{\Delta}I}$). Use this to write down your prediction in $\mathbf{A \pm \mathrm{\Delta}A}$ format.**
:::

::: {.question #ph212-designing-experiments:prediction-test}
**Perform your experiment with the new mass and measure the acceleration of the system. Include the uncertainty in your measurement. How does the result compare to your prediction? Are they similar? How did you decide? If the result differs from the prediction, what does that suggest, i.e., what might explain the difference?**
:::

::: {.question #ph212-designing-experiments:experimental-value}
**The value you found for moment of inertia is called an experimental value because you found it by doing measurements and analysis. How is this different from a theoretical value that you could find by using a formula? Which value would you trust more, and why?**
:::

### Part 6: Submit Your Group’s Lab Report

Make sure everyone’s name is on your group’s lab report. If you submit through Gradescope remember to add everyone in your group to the assignment. This is done at the end of the submission process.

## Appendix A – Derivation of the model equation for this activity

Here we show how to get the model equation for the motion of the flywheel given at the beginning of the handout

$I\alpha = mgr - mar$.

The physics principle we will use is Newton’s second law. For the rotational motion of the wheel this is:

$$I\alpha = \sum_{}^{}\tau_{i} = \sum_{}^{}F_{i}d_{i}\sin\theta_{i}$$

where $\tau_{i}$ are the individual torques acting on the wheel, and each torque is due to an external applied force *F~i~* acting at a distance *d~i~* from the axis of the wheel at an angle *θ~i~*.

*If we ignore friction*, the only external force acting on the wheel is the tension *F^T^* due to the string, which acts at 90° a distance *r* from the axis. The tension exists because of the mass hanging on the other end of the string. (No mass means no tension, and then the wheel doesn’t rotate.) So Newton’s second law for the rotation of the wheel becomes

$$I\alpha = F^{T}r$$

where we have chosen rotation caused by a downward tension to be positive.

To get the magnitude of the tension we use Newton’s second law for the linear motion of the mass:

$$ma = \ \sum_{}^{}F_{i}$$

where $F_{i}$ are the individual forces acting on the mass.

The only forces acting on the mass are gravity pulling it down, *F^g^ = mg*, and the tension *F^T^* pulling it up. So Newton’s second law for the mass becomes

$$ma = mg - \ F^{T}$$

where we have chosen down to be positive to match the sign convention of the rotational motion.

Solving for *F^T^* and substituting into Newton’s second law for the rotational motion of the wheel gives

$I\alpha = (mg - ma)r$,

the equation at the beginning of this handout for the motion of the flywheel in the absence of friction.

## Appendix B – Reference Information

This section contains key information from previous labs.

1.  Required Plot Elements
2.  What Is Uncertainty?
3.  Sources of Uncertainty
4.  Linearization

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

When you fit data with a linear trendline, you are essentially checking whether the two variables are proportional to each other. To check a nonlinear hypothesis, we can instead check if one variable is proportional to *a function of* the other variable.

In practice, **linearization is done by calculating a new column of data** that gives the values of a *function* of the input variable. Typically, the input variable is the independent variable, and the function is chosen so that the resulting quantity is proportional to the dependent variable.

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
