---
id: ph213-data-taking-handout
title: "Lab 3 – Data Collection"   # the original title text; see ledger 22
course: PH213
sequence: 3
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH213/Lab 3 - Data Taking - Handout.docx"
source_sha256: "d1b09d299bcc9fc9fdbc48c06cb7949eb5b82dc9f230fd382adfd4f5588ac6d2"
status: converted
images:
  - file: "ph213-data-taking-handout-media/electrode-configurations.png"
    source_part: "word/media/image1.png"
    sha256: "f15bbbfb170a7cbe5807e12a20a0bea3b75f8df3b9456f31c9f8403c62026a26"
---

# Lab 3 – Data Collection

## PH 213 – General Physics with Calculus

**Experimental goal: Use equipment to determine and draw equipotential lines and vector fields for different electrode configurations.**

In this activity you will carefully map the equipotential lines for a configuration of electrodes in a two-dimensional system. You’ll then calculate the electric field for that some configuration of electrodes. This should allow you to explore a geometric relationship between the lines of constant potential (equipotential lines) and the electric field lines.

## Learning Objectives

**Learning goal: Systematically collect data and use it to understand the relationship between related quantities in the system.**

This lab activity is designed to help you practice the following skills:

1.  Understand the relationship between measurements and quantities of interest.
2.  Use available equipment to collect data in a systematic way.
3.  Identify significant sources of measurement uncertainty and quantify them.
4.  Calculate error propagation.

## Equipment

::: action
- Conductive paper with electrodes painted in highly conductive ink – 3 patterns on cork backing
- Power supply
- Multimeter with probes
- Cables with alligator clips
- Conductive push pins
- Graph paper
- Probe holder
:::

## Generating electric fields and mapping electric potential

You should have leads coming from the power supply. When you connect the leads to electrodes on a sheet of conductive paper, you can apply a potential difference $\Delta V$ from one electrode to the other. You will also create an electric field in the paper as if each electrode were charged.

Since the paper is a conductor and air is an insulator, virtually all the electric field lines are contained in the paper. This allows us to treat the paper and electrodes as a two-dimensional system.

The electrodes are each an equipotential surface. When a lead is connected to an electrode, it holds that electrode at a fixed value of electric potential. The potential and electric field it creates will be the same as if it were uniformly charged.

You can use the meter to read the potential difference between the electrodes by touching each with the probes. You can also measure the potential difference between an electrode and any point on the paper by placing one probe on the electrode and the other on the paper at the point of interest.

::: hint
- Your multimeter should be set to the 20𝑉 *D*𝐶 setting.
:::

[Use the metal push pins to connect a lead to an electrode]{.underline}.

::: hint
- Push the pin firmly and vertically into the electrode. The base of the pin should make complete contact with the electrode. Clip the lead to the pin head to complete the connection.
  - Using an existing hole will minimize damage to the electrode.
:::

**Warning:** To avoid a possible short circuit, be careful not to touch the leads to each other. It will trigger the fuse in your power supply and turn it off. If this happens, ask your instructor to help you reset the fuse.

## Part 1: Explore a Model

**\*\*You will be completing this part of the lab as a class\*\***

Before we can determine the electric field around the more complicated configuration(s) that we will be using, we need to figure out how to use the potential to find the electric field. We know that the *magnitude* of the electric field can be estimated by

$$\left| E \right| = \ \frac{\Delta V}{\Delta r}$$

where $\Delta V$ is the potential difference between two points in space and $\Delta r$ is the distance between those two points. But how do we determine the direction of the electric field.

We can start by considering a very simple configuration: a point charge.

::: action
- **Sketch the electric field lines around a single point charge. Don’t include the sketch in your report yet.**
:::

We can now set up an equivalent configuration in the water.

::: action
- **Find the conductive sheet with the large ring and point at the center. Place one lead at its center and the other lead on the ring.**
:::

If the red (positive) lead is at the center, it acts like a single positive charge at the center of the ring. If the black (negative) lead is at the center, it acts like a single negative charge.

You will use the meter to determine the potential in the region around the electrodes. In particular, you will map out equipotential lines of the system. Start by making a scale mapping of the electrodes on a sheet of graph paper. You will add your potential readings to the map.

Using the meter probes, measure the potential difference between two points in the region inside the ring. Using the probe holder allows us to keep the distance between the two probes fixed. Thus, the measurement on the multimeter when using the holder is the *potential difference between two points at a* *fixed distance*. This in turn gives the size of the electric field around the point.

::: action
- **Turn on the power supply and set the output to 10 V.**
:::

::: {.question #ph213-data-taking:probe-sweep}
**Place the red probe in various spots on the paper and swing the black probe in a circle around it using the holder. On your sketch of the point charge electric field, mark roughly where you placed the red probe and the position of the black probe that gave the largest potential difference. Mark the placement of the black probe that gives you the smallest potential difference. After repeating this process for multiple points on the paper, include your sketch in the report.**
:::

::: {.question #ph213-data-taking:compare-prediction}
**Compare your prediction of the electric field to the directions of maximum and minimum** $\mathbf{\Delta}\mathbf{V}$**. How are they related?**
:::

## Part 2: Calculate the Electric Field

You should have two more sheets of conductive paper, one with each of the configurations shown in the diagram below. *Choose one to use for the rest of the lab.* Put the other aside.

![Two possible configurations of electrodes. The configuration on the left has two bars creating a 90 degree angle, with a 5 cm gap between the bottom bar and the bar on the right. The configuration on the right has a vertical bar on the left, and a circle 10 cm to the right.](ph213-data-taking-handout-media/electrode-configurations.png){width="5.4938in" height="3.5944in"}

::: action
- Connect one lead to each of the electrodes in your chosen configuration. Again, using an existing hole will minimize damage to the electrode. Have your instructor check your set up.
- Draw your configuration *to scale* on graph paper or an electronic grid. (If you use graph paper, make sure it matches the units in your tray – cm or inches).
:::

We can now start looking at the electric field in the region of interest. Recall that the *magnitude* of the electric field is given by:

$$\left| E \right| = \ \frac{\Delta V}{\Delta r}$$

But the electric field is a vector and needs a direction in addition to the magnitude!

::: {.question #ph213-data-taking:field-direction-method}
**Describe how you can use the probe holder and multimeter to find the magnitude *and* direction of the electric field for an arbitrary point in the region of interest. (Hint: The field is in the direction of the largest slope in the potential, i.e., the direction in which it changes fastest.)**
:::

Calculate the electric field magnitude for one point in your diagram. Estimate the uncertainty in your value. Sketch an arrow to represent the electric field at the point where you calculated the magnitude. The arrow should point in the direction of the field as determined using the method you described above. You also want the arrow to represent the strength of the field (see below).

[Representing field strength, finding the uncertainty:]{.underline}

::: hint
- Length: Often the strength of the field is represented by making the length of the arrow proportional to its magnitude at that point.
- Width or color: If you don’t have room to do this on your graph paper you may find it easier to make all the arrows the same length, using heavier arrows or different colors for larger values of the field.
:::

The choice of representation is up to you. If you do this for a large number of points, you end up with the *electric field vector map* of your configuration.

::: {.question #ph213-data-taking:vector-map}
**Now that you have a process for determining the electric field, calculate and mark the field for reasonably spaced points throughout the region of interest. You get to decide what is reasonably spaced, but remember that your goal is to create an accurate vector map of the electric field. When you’re done, include your diagram of the vector field (either a photo or screenshot) in your report.**
:::

::: {.question #ph213-data-taking:measurement-uncertainties}
**Pick one of your electric field calculations and estimate the measurement uncertainties in the potential difference and in the displacement. Find the statistical uncertainty in each. Combine the measurement and statistical uncertainties to determine and report the total uncertainty in each quantity, potential difference and displacement. (Remember, these should be combined in quadrature, as described in the reminders at the end of the handout.)**
:::

::: {.question #ph213-data-taking:field-uncertainty}
**Use the general equation for uncertainty propagation (shown in the box below) to determine an expression for the uncertainty in the electric field magnitude. Use your expression to find the uncertainty in your calculated magnitude. Which part of the electric field seems like it has more uncertainty, the magnitude or the direction? Comment on why you believe this.**
:::

::::: box
### Uncertainty in a Calculated Quantity (Propagating Uncertainty)

Suppose we have a quantity $w$ that depends on three other quantities $x,\ y,\ z$, such that

$w = \frac{x^{\alpha}y^{\beta}}{z^{\gamma}}$.

Each measured quantity has its own uncertainty, $\Delta x,\ \Delta y,\ \Delta z$. Then the uncertainty in $w$ is given by the equation:

$$\Delta w = w*\sqrt{{\alpha\left( \frac{\Delta x}{x} \right)}^{2} + {\beta\left( \frac{\Delta y}{y} \right)}^{2} + {\gamma\left( \frac{\Delta z}{z} \right)}^{2}\ }$$

This is very similar to the equation used to find total uncertainty from multiple sources, with a few important changes.

::: hint
- Each quantity likely has different units, so by dividing each uncertainty by the measured value, everything in the square root is unitless. You can also think of this as adding the percent uncertainties together (also called relative uncertainty), instead of the uncertainties themselves.
- Exponents are just repeated multiplication – for example, $x^{2} = x*x$. In this case, the uncertainty in $x$ would come up twice in the square root, so we would add $\left( \frac{\Delta x}{x} \right)^{2} + \left( \frac{\Delta x}{x} \right)^{2} = 2\left( \frac{\Delta x}{x} \right)^{2}$, which is why exponents become multiplication factors.
:::
:::::

## Part 3: Map the Electric Potential

In this part of the activity you will determine the electric potential around the electrode configuration.

The negative probe of the multimeter should be attached to one electrode. The positive probe of the multimeter then measures the difference in the potential between it and the negative electrode. Since the zero point of electrical potential is arbitrary, we will choose the negative probe as zero. In other words, the electrode it’s attached to will be at *V =* 0. Then the meter tells us the value of the potential at the measured point.

::: action
- Use the graph paper to make a scale drawing of your electrode configuration. Mark the point of zero potential on the drawing.
- Use the positive probe to find locations of the integer-valued potentials (the places with potential values of 1 V, 2 V, 3 V, …, 10 V.)
- Mark the location and value of the electric potential at each point that you measure on the grid with the scale drawing of your configuration. Find enough points that you can accurately draw the equipotential lines for each integer potential value. You do not need to include the scale drawing in your report yet.
:::

When you’re done you should have a two-dimensional map of the electric potential throughout the region of interest.

::: {.question #ph213-data-taking:equipotential-lines}
**Follow the bullet points above to take data throughout the entire region of interest, on the same drawing as your vector field. Use your values to sketch the equipotential lines (connect all the dots that have the same potential) and label each line with the potential of that line. Include your updated diagram (either a photo or screenshot) in your report.**
:::

## Part 4: Conclude and Reflect

::: {.question #ph213-data-taking:geometric-relationship}
**Based on your diagram, what is the geometric relationship between the direction of the electric field and the equipotential lines? Does this align with what you found when considering a single point charge?**
:::

::: {.question #ph213-data-taking:individual-responses}
**Each group member should write an individual, concise response to the following questions.**

::: action
- **One new thing you’ve learned about collecting data to learn about relationships between variables.**
- **Any unanswered questions you still have about the relationship between electric field and electric potential.**
:::
:::

## Part 5: Submit your group’s lab report

Make sure everyone’s name is on your group’s lab report. If you submit through Gradescope remember to add everyone in your group to the assignment. This is done at the end of the submission process.

## Appendix – Reference Information

This section contains key information from previous labs:

1.  Required Elements in a Plot
2.  Linearization
3.  Uncertainty

**[Required Elements in a Plot]{.underline}**

::: action
- Do not connect the data points with lines.
- Make sure you create *Scatter Plots* and not *Line Plots*.
- Evaluate if the plot makes sense. Are the axes correct? Do you have the right number of data points?
- Include a descriptive title and labels on each axis, always including physical units.
- Add a legend, unless you only have one set of data and the title describes it.
- Display the equation and R^2^ value for any trendline you include.
:::

**[Linearization]{.underline}**

In the context of data analysis, “linear” refers to a directly proportional relationship between the dependent and independent variables in an equation.

::: action
- Mathematically, if two variables $x$ and $y$ have a linear relationship, we can express this as $y = mx + b$ where m and b are constants.
- More simply, we can write this as $y \propto x$ where $\propto$ means “is proportional to”.
- When graphed, data with a linear relationship falls on a straight line.
:::

**Linearization comes in handy when your data or hypothesis is *not* linear.**

When you fit data with a linear trendline, you are essentially checking whether the two variables are proportional to each other. To check a nonlinear hypothesis, can we instead check if one variable is proportional to *a function of* the other variable.

In practice, **linearization is done by calculating a new column of data** that gives the values of a function of the input variable (you will practice this below, so don’t worry if you don’t understand what this means yet). Then, the linearized data can be plotted and analyzed.

**[Why Linearize?]{.underline}**

::: action
- Linear data is typically easier to understand and analyze.
- There are analysis methods we can apply to linear data that don’t work as well (or at all) with nonlinear data.
- It is relatively easy to fit a line to data - there are just two important values to determine: the slope and intercept of the data.
:::

**[Sources of Uncertainty:]{.underline}**

The uncertainty in a measurement can be due to a combination of several factors. A crucial aspect of experimentation is to identify all such sources of uncertainty and to numerically estimate their effect on your measurement result.

Common sources of uncertainty include:

1.  your judgement in reading analogue instruments

<!-- -->

1.  the effects of environmental conditions on the measurement
2.  the sensitivity of your instruments (e.g. a digital scale, a meter stick)
3.  the rating or stated calibration of the instrument
4.  approximations and assumptions that you make while doing the experiment
5.  variations in repeated readings made under apparently identical conditions (statistical uncertainty)

A measurement uncertainty is not meant to be an indication of “mistakes” that you might make in an experiment. If you are aware that you have made a mistake, then you should repeat your experiment. **“Human error” is not a valid source of uncertainty**. If you know that you did something “wrong”, then the right course of action is to redo it correctly.

When a measurement has multiple sources of uncertainty, we can combine them by:

$$\Delta t_{total} = \sqrt{\left( \Delta t_{1} \right)^{2} + \ \left( \Delta t_{2} \right)^{2} + \ \left( \Delta t_{3} \right)^{2} + \ldots}$$

This is called *adding in quadrature*.
