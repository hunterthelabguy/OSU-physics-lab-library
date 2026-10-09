---
id: ph213-hypothesis-testing-handout
title: "Lab 2 – Hypothesis Testing"   # the original title text; see ledger 22
course: PH213
sequence: 2
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH213/Lab 2 - Hypothesis Testing - Handout.docx"
source_sha256: "52bb40c81369f95310ee1de828b3f83d5f787e1c4c6b64dab4e05f43156130fc"
status: converted
images:
  - file: "ph213-hypothesis-testing-handout-media/crt-schematic.png"
    source_part: "word/media/image1.png"
    sha256: "0e735c6862ec0e142c1d742e17136979947b6e3d73f42860eb2d894673bc0f74"
---

# Lab 2 – Hypothesis Testing

## PH 213 – General Physics with Calculus

**Experimental goal: Test whether a given model equation describes the behavior of electrons in a cathode ray tube (CRT).**

A CRT accelerates and deflects a beam of electrons, which in turn creates a spot on the screen of the CRT.

The CRT itself is a glass vessel which contains: (1) an electron gun that emits electrons into a beam that travels along the tube, (2) a deflection system to change the direction of the beam, and (3) a viewing screen. CRTs are used in displays such as oscilloscopes and old TV sets and monitors.

## Learning Objectives

**Learning goal: Identify and test multiple predictions based on a given hypothesis, and use the combined results to support or refute the hypothesis.**

This lab activity is designed to help you practice the following skills:

1.  Understand relationship between measurements and quantities of interest.
2.  Identify testable predictions in a physical model.
3.  Extract physical parameters from fits to a model, e.g., the slope of a graph.
4.  Use quantitative evidence such as R^2^ value for a particular fit to support conclusions.

## Equipment

::: action
- CRT
- Power supply
- Multimeter
- Cables
- Ruler (wooden or plastic)
:::

## Understanding the CRT

There are 3 stages to creating and controlling a beam of electrons in the CRT. Understanding these stages will help you understand the model being used to predict the electron behavior.

1.  In the first section of the tube the electrons leave a heated filament approximately at rest and are accelerated horizontally down the tube of length $L_{1}$ by a uniform accelerating electric field $E_{A}$. We assume that the electrons have reached a maximum constant speed just at the end of this distance $L_{1}$, and that the entire acceleration is due to the electric field.
2.  The electrons then enter the deflection region of length $L_{2}$, where they are bent from their path by a uniform deflecting electric field $E_{D}$. The deflection is perpendicular to the horizontal motion.
3.  Finally, the electrons enter another region of zero electric field, where they travel some distance $L_{3}$ at constant velocity until they hit the screen.

A schematic of the tube is shown below. A disassembled tube is also available for inspection. The electric fields are established by parallel plate capacitors. In this experiment you cannot measure the value of electric field, but you can measure the voltage across the capacitor, $\Delta V$. The electric field is proportional to this voltage, $E\  = \ \Delta V/d$, where $d$ is the distance between the two plates.

In this experiment, you will test a model describing the effects of the electric fields on the total deflection of the electron beam. The results of the model are below; your task is to design and perform an experiment that will test it.

![Schematic diagram of a cathode ray tube. An electron beam is generated on the left hand side by a source, then passes through a horizontal accelerating region, labeled with a potential difference VA. The electron beam then passes through a vertical deflecting region, labeled with a potential difference VD, causing the beam to bend upwards. The electron beam ends on the right hand side at a screen. The difference between the height of the electron source and the height of where the beam ends is the total deflection.](ph213-hypothesis-testing-handout-media/crt-schematic.png){width="5.7507in" height="3.5819in"}

## Part 1: Explore a Model

The model starts with the force $\overset{⃑}{F_{E}}$ on a charge $q$ in an electric field $\overset{⃑}{E}$ where $\overset{⃑}{F_{E}} = \ q\overset{⃑}{E}$. This is combined this with the Newton’s second law, $\overset{⃑}{F} = \ m\overset{⃑}{a}$, and the kinematics of an object undergoing constant acceleration to determine the motion and time spent by the charge in each section of the tube. The result is that the charge will deflect a total distance ∆𝑦 given by

$$\Delta y\  = \ \Psi\ \left\lbrack \frac{E_{D}d_{D}}{E_{A}d_{A}} \right\rbrack\ \ \ \ (1)$$

where the subscripts $D$ and $A$ refer to the deflecting capacitor and the accelerating capacitor respectively. The quantity $\Psi$ depends only on the geometry of the tube ($L_{1}$, $L_{2}$ , etc.) and is a constant for a given tube.

In the tube the electric fields are established by parallel plate capacitors. In this experiment you cannot measure the value of electric field, but you can measure the voltage across the capacitor, $\Delta V$. The electric field is proportional to this voltage, $E\  = \ \Delta V/d$, where $d$ is the distance between the capacitor plates. By measuring the effects of the voltage, you can confirm the effects of the electric field.

We rewrite the above equation for the deflection in terms of the voltage across each capacitor, $\Delta V_{D}$ and $\Delta V_{A}$.

$$\mathbf{\mathrm{\Delta}y\  = \ \Psi\ }\left\lbrack \frac{\mathbf{V}_{\mathbf{D}}}{\mathbf{V}_{\mathbf{A}}} \right\rbrack\ \ \ \ (2)\ $$

Your task, then, is to check whether Equation (2) correctly describes the behavior of the CRT.

## Part 2: Plan the Experiment

::: box
### Using the CRT

This box describes how to use the CRT to generate data. Your instructor should explain; it’s repeated here for reference. The CRTs are delicate and difficult to repair and replace. *If you’re not sure about how to properly use your CRT, check with your instructor before proceeding.*

• There is a grid on the front of the CRT. The thick lines are 1cm apart and the thin lines are 1mm apart. You may find this helpful for measuring deflections.

• Voltage control knobs are labeled in *Figure 1*.

• Before turning on the power supply to the CRT, verify the connections of your apparatus. (You can ask your instructor.) Turn all knobs on the power supply to the left (counterclockwise). All devices must be correctly wired and set before applying power.

• Once your set-up has been verified, turn on the power supply. Let the heating element warm up for about 45 seconds before adjusting voltages.

• To create an electron beam, slowly turn the control for the accelerating voltage $\Delta V_{A}$ until the display reads approximately 350 volts. (See *Figure* *1*). You should get a spot on the screen.

• Adjust the focus knob on the CRT for the best spot size.

• You can move the beam using the control for the deflection voltage $\Delta V_{D}$ (see *Figure 1*). The voltmeter will display the value of the applied deflection voltage.

• If you have a black spot on your screen, it will probably fix itself with time. But you can try sweeping the electron beam back and forth across the spot using the deflection voltage setting.
:::

Your objective is to find and test the relationship between the deflection of the electrons and values of the applied voltages 𝛥𝑉~𝐴~ and 𝛥𝑉~𝐷~ as given above. You’ll do this by

::: action
- predicting what a graph of the deflection vs. each voltage should look like.
- taking enough data to plot the dependences.
- comparing the plotted data to your predictions.
:::

When discussing the CRT in your write-up, refer to the figure given above.

::: {.question #ph213-hypothesis-testing:sense-making}
**Use sense-making techniques to explain why the proposed dependence of** $\mathbf{\Delta}\mathbf{y}$ **on** ${\mathbf{\Delta}\mathbf{V}}_{\mathbf{A}}$ **and** $\mathbf{\Delta}\mathbf{V}_{\mathbf{D}}$ **is reasonable (just discussing units is not enough!). Describe your thinking.**
:::

::: hint
- Note on notation: In this lab, all potentials will be measured from zeroFor the rest of the handout we will refer to the change in potential *ΔV* as simply *V*.
:::

A single equation (in this case Equation 2) can result in many predictions. In this lab, we are predicting that:

i.  $\Delta y = a*V_{D}$ (is proportional to $V_{D}$)
ii. $\Delta y = b*\left( \ \frac{1}{V_{A}} \right)$ (is proportional to $\frac{1}{V_{A}}$)
iii. $\Psi$ is constant
iv. The y-intercepts of both $\Delta y = a{*V}_{D}$ and $\Delta y = b*\frac{1}{V_{A}}$ are zero.

**Compare the expressions above to the model equation (2). What is** $\mathbf{a}$**? What is** $\mathbf{b}$**? How do they relate to** $\mathbf{\Psi}$**?** You don’t need to answer these questions in your report, but you should understand the answers before you proceed. If you’re not sure, check with your instructor.

::: {.question #ph213-hypothesis-testing:predictive-graphs}
**Next, use Equation (2) to sketch two linear predictive graphs:**

a.  **The deflection** $\mathbf{\Delta}\mathbf{y}$ **as you change the deflection voltage** $\mathbf{V}_{\mathbf{D}}$ **while holding the accelerating voltage** $\mathbf{V}_{\mathbf{A}}$ **constant, and**
b.  **The deflection** $\mathbf{\Delta}\mathbf{y}$ **as you change the accelerating voltage** $\mathbf{V}_{\mathbf{A}}$ **while holding the deflection voltage** $\mathbf{V}_{\mathbf{D}}$ **constant. Note that the dependence of** $\mathbf{\Delta}\mathbf{y}$ **on** $\mathbf{V}_{\mathbf{A}}$ **is *nonlinear*, but we are basing our predictions and analysis on a *linear* plot. This means we will be linearizing with respect to** $\mathbf{V}_{\mathbf{A}}$**.**
c.  **For each graph, discuss how you can use the graph and/or the fit equation to determine** $\mathbf{\Psi}$ **in terms of** $\mathbf{a,\ b,}$ **and / or known parameters**
:::

::: {.question #ph213-hypothesis-testing:measurement-plan}
**Discuss how you will make measurements using the available equipment. In your discussion, include an explanation of how you’ll find the zero point from which to measure** $\Delta y$ **in each of your two experiments.**
:::

Hint: Each time you change $V_{A}$ you will change the zero-point on the screen. Make sure you make each measurement from the new zero point.

::: {.question #ph213-hypothesis-testing:testing-predictions}
**How will you use the measurements to test each of the four predictions? What will you look for to see if the data supports your predictions/predicted graphs?**
:::

## Part 3: Collect Data

First, we will explore the system to understand it (and our equipment) better. *Don’t forget to read the box at the beginning of the lab for tips about using the CRT.*

::: {.question #ph213-hypothesis-testing:nearby-devices}
**What happens to the electron beam if you move another electronic device (such as a phone, smartwatch, laptop, etc.) close to the CRT? Why might this occur? What does this mean for your experimental set up?**
:::

::: {.question #ph213-hypothesis-testing:reversed-wires}
**Discuss what you think would change in this experiment if you reversed the wires for the deflecting voltage. [(Don’t actually do this without checking with your instructor. If you change the wrong wires you can damage the equipment, which is difficult to replace.)]{.underline}**

![Photograph of the front panel of the power supply, labeling the relevant dials and displays](ph213-hypothesis-testing-handout-media/power-supply-panel.svg){.drawn drawings="188406814"}
:::

::: box
**The maximum value for** $\mathbf{V}_{\mathbf{A}}$ **is 400 V!**
:::

::: {.question #ph213-hypothesis-testing:data-and-uncertainty}
**Perform your experiments and record your data. Include in your report any data tables that you create.**

a.  **Refer to the box below to refresh yourself on common sources of uncertainty. Quantify the measurement uncertainty in your data and identify the biggest source(s) (see the box below for help). Include any statistical uncertainty in your data. Combine the measurement and statistical uncertainties to determine and report the total uncertainty in your average measurements by combining all sources as described in the box.**
:::

::: box
### Sources of uncertainty

The uncertainty in a measurement can be due to a combination of several factors. A crucial aspect of experimentation is to identify all such sources of uncertainty and to numerically estimate their effect on your measurement result.

Common sources of uncertainty include:

1.  your judgement in reading analogue instruments
2.  the effects of environmental conditions on the measurement
3.  the sensitivity of your instruments (e.g. a digital scale, a meter stick)
4.  the rating or stated calibration of the instrument
5.  approximations and assumptions that you make while doing the experiment
6.  variations in repeated readings made under apparently identical conditions (statistical uncertainty)

A measurement uncertainty is not meant to be an indication of “mistakes” that you might make in an experiment. If you are aware that you have made a mistake, then you should repeat your experiment. **“Human error” is not a valid source of uncertainty**. If you know that you did something “wrong”, then the right course of action is to redo it correctly.

When a measurement has multiple sources of uncertainty, we can combine them by:

$$\Delta t_{total} = \sqrt{\left( \Delta t_{1} \right)^{2} + \ \left( \Delta t_{2} \right)^{2} + \ \left( \Delta t_{3} \right)^{2} + \ldots}$$

This is called *adding in quadrature*.
:::

## Part 4: Analyze the Data and Draw Conclusions

Recall that in this lab, we are testing the predictions that:

i.  $\Delta y = a{*\ V}_{D}$
ii. $\Delta y = b*\ \left( \ \frac{1}{V_{A}} \right)$
iii. $\Psi$ is constant
iv. and the y-intercepts of both $\Delta y = a{*V}_{D}$and $\Delta y = b*\frac{1}{V_{A}}$ are 0

You are now ready to go through each prediction and see if it is supported by your data.

::: {.question #ph213-hypothesis-testing:graphs-and-fits}
**Use your data to create each of the graphs you described before. Include the uncertainty in your average measurements as error bars. Fit the data in each graph with the expected mathematical relationship between what’s plotted on the x- and y-axes. This will require linearizing the plot for** $\mathbf{V}_{\mathbf{A}}$**!**
:::

::: {.question #ph213-hypothesis-testing:compare-predictions}
**Compare the graphs to your predictions. Do your results support your relationship? That is, were your predictions for the graphs correct? Your answer should include a comparison to the expected graphs you sketched at the beginning of the lab.**
:::

::: {.question #ph213-hypothesis-testing:psi-values}
**Use your fits to extract a value of the constant** $\Psi$ **from each graph. Show and/or explain how you found these values. Are the values you found for** $\Psi$ **consistent? Defend your answer.**
:::

::: {.question #ph213-hypothesis-testing:y-intercepts}
**Consider the y-intercepts of the two fits that you found. What does the y-intercept physically represent for each fit equation? If they do not align with your predictions, what can explain the discrepancy?**
:::

::: {.question #ph213-hypothesis-testing:model-verdict}
**Based on your plots, do you think that the model introduced at the beginning of the lab (and thus the equations in the predictions) are a good representation of the CRTs? Be sure to justify your response with references to your data and analysis.**
:::

::: {.question #ph213-hypothesis-testing:difficulties}
**What was the most difficult step when collecting data and/or the most significant source of uncertainty? How that might have affected your conclusions?**
:::

## Part 4: Submit your group’s lab report

Make sure everyone’s name is on your group’s lab report. If you submit through Gradescope remember to add everyone in your group to the assignment. This is done at the end of the submission process.

## Appendix – Reference Information

This section contains key information from previous labs:

1.  Required Plot Elements
2.  Linearization

**[Required Plot Elements]{.underline}**

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
