---
id: ph211-describing-an-experiment-handout
title: "Lab 6 – Describing an Experiment"   # the original title text; see ledger 22
course: PH211
sequence: 6
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH211/Lab 6 - Describing an Experiment - Handout.docx"
source_sha256: "cf18da95fc358c0c1006d8a9a42e2d027a27889363bc44a3fcdc8f5487754c19"
status: ruled-change
ruled_omissions:
  - text: "between a block and a carpet square."
    ledger: "D-0169"
  - text: "between a wooden block and piece of carpet, but"
    ledger: "D-0169"
  - text: "the block on a piece of carpet on a ramp."
    ledger: "D-0169"
  - text: >-
      Wooden block Piece of carpet Meter stick Masses Balance Some stations:
      Ramp, or Force sensor
    ledger: "D-0169"
  - text: "between a wooden block and piece of carpet (both supplied)"
    ledger: "D-0169"
  - text: >-
      Before taking data using the force sensor, you need to prepare it:
      Open Graphical Analysis Choose your probe setting. Choosing 10 N will
      give you better precision for smaller forces, but it will give you
      incorrect values if the force is more than 10 N. In that case choose
      50 N, reset the probe and repeat the measurement. Do not subject the
      probe to more than 50 N of force. Connect the Force Sensor. If the
      sensor is wireless, do not connect it using the computer’s Bluetooth
      settings. Connection should be done through the Graphical Analysis
      app. Zero the probe. Place it flat on the table with nothing touching
      the sensor end (the hook). In Graphical Analysis, click on the display
      at the bottom right of the screen showing the force sensor reading.
      Choose “Zero” from the menu. You can zero as often as you like and
      should do so anytime you get a non-zero reading when the probe has no
      force on it. You should typically zero anytime you change the setting.
    ledger: "D-0169"
ruled_additions:
  - text: "between a block and a whiteboard."
    ledger: "D-0169"
  - text: "between a wooden block and a whiteboard, but"
    ledger: "D-0169"
  - text: "Your instructor will tell your group which face of the block to put down."
    ledger: "D-0169"
  - text: "the block on a whiteboard on a ramp."
    ledger: "D-0169"
  - text: >-
      Wooden block (two wood faces, two felt faces) Whiteboard Meter stick
      Balance Some stations: Adjustable ramp with the whiteboard clamped to
      it, and a protractor, or Cart with a built-in force sensor, and masses
    ledger: "D-0169"
  - text: "between a wooden block and a whiteboard (both supplied)"
    ledger: "D-0169"
  - text: >-
      Before taking data using the cart’s force sensor, you need to prepare
      it: Open Graphical Analysis (graphicalanalysis.app) in Chrome or
      Edge. Choose Sensor Data Collection, click Wireless, and select your
      cart. Do not connect it using the computer’s Bluetooth settings. Open
      Sensor Setup. Open Sensor Channels. Select Force. Deselect Position.
      Click Done. At the bottom left, click Mode to open Data Collection
      Settings. Change End Collection from a set duration to Manually, and
      click Done.
    ledger: "D-0169"
images:
  - file: "ph211-describing-an-experiment-handout-media/graphical-analysis-view-icon.png"
    source_part: "word/media/image1.png"
    sha256: "7a85a2239d2a80de52693e4df786a1a22c14eff78027951153a8b42bdf2c941a"
  - file: "ph211-describing-an-experiment-handout-media/graphical-analysis-graph-tools-icon.png"
    source_part: "word/media/image2.png"
    sha256: "36df8e6bdf281576cc60c1e819bfc8b499fad38ed8027eaee5ca5e8dc9a32b4f"
---

# Lab 6 – Describing an Experiment

## PH 211 – General Physics with Calculus

**Experimental goal: Find the coefficient of static friction between a block and a whiteboard.**

In this activity you will devise and describe an experiment, take data and find results, and then give your experimental description to another group. The other group will repeat it and compare their results to yours. At the same time, you’ll repeat their experiment using their description, and compare your results with theirs.

Each experiment will determine the coefficient of static friction between a wooden block and a whiteboard, but in different ways. Your instructor will tell your group which face of the block to put down.

1.  By placing the block on a whiteboard on a ramp.
2.  By measuring force on the block.

## Learning Objectives

**Learning goal: Describe your experiment in such a way and with enough detail that the other group can do it *without any input other than the written description.***

You’ll also practice the following skills:

1.  Design an experiment to test a hypothesis.
2.  Collect and analyze data following someone else’s description of an experiment.
3.  Determine if your results match someone else’s within experimental uncertainty.

## Equipment

You will have access to different equipment depending on which experiment you’re doing.

All stations:

::: action
- Wooden block (two wood faces, two felt faces)
- Whiteboard
- Meter stick
- Balance
:::

Some stations:

::: action
- Adjustable ramp with the whiteboard clamped to it, and a protractor, or
- Cart with a built-in force sensor, and masses
:::

You must design an experiment you can perform using only the equipment at your station.

## Part 1: Explore a Model

Two objects in contact but not moving relative to one another will exert a frictional force on each other. This is known as *static friction* because it’s the friction that occurs when the objects don’t move relative to each other. It is different from the friction between two objects that are moving against each other.

Each object exerts a force of static friction $F^{s}$ on the other as a pair of equal and opposite forces (Newton’s third law). Each force is parallel to the contact surface between the objects.

The magnitude of the static friction is given by $\mathbf{F}^{\mathbf{s}}\mathbf{\leq \ }\mathbf{\mu}_{\mathbf{s}}\mathbf{F}^{\mathbf{N}}$***.***

Here $F^{N}$ is the *normal force*, the total of all forces *perpendicular* to the surface between the two objects, and $\mu_{s}$ is the *coefficient of static friction*, a dimensionless number that depends only on the contacting surfaces of the two objects.

**[Note]{.underline}: The coefficient depends on which surfaces are in contact and how they’re oriented.**

Notice that the expression has a less-than-or-equal-to sign. It gives the maximum *possible* frictional force. The frictional force will oppose other forces acting on the object parallel to the surface, and it will be only as large as needed to keep the object stationary.

::: hint
- **At the moment the other forces exceed the maximum possible value given by the expression above, the object will begin to move.** (Once it starts moving, the friction typically gets smaller, and its behavior is no longer described by the above equation.)
:::

When an object is on a ramp at an angle $\theta$ from the horizontal, gravity creates both a force parallel to the surface (which tries to move the object down the ramp) and a force perpendicular to the surface (which creates a normal force).

::: hint
- Using a free-body diagram with the force of gravity and the force of static friction, you can show that the object will not move if $\mathbf{tan(\theta)\  \leq \ }\mathbf{\mu}_{\mathbf{s}}$.
:::

*These two statements are the underlying principles to the experiments in this lab (see below). In both cases, the key is noting values just as the block begins to move.*

## Part 2: Plan the Experiment

Below are two possible experiments. You should do the one that fits the equipment at your station. (Your lab instructor may move you to a different station to even out the number of groups doing each experiment.)

In both experiments, your objective is to determine the coefficient of static friction between a wooden block and a whiteboard (both supplied)

**[Experiment 1 (Ramp):]{.underline} Use the block on the ramp to determine the coefficient of static friction. Use the fact that the block will start moving at a ramp angle** $\theta$ **related to the coefficient by** $\mathbf{\tan}\left( \mathbf{\theta} \right)\mathbf{= \ }\mathbf{\mu}_{\mathbf{s}}$**.**

**[Experiment 2 (Force sensor):]{.underline} Measure the force necessary to move the block to determine the coefficient of static friction. Use the fact that the block will start moving when the force just overcomes the maximum possible static friction,** $\mathbf{F}_{\mathbf{\max}}^{\mathbf{s}}\mathbf{= \ }\mathbf{\mu}_{\mathbf{s}}\mathbf{F}^{\mathbf{N}}$**.**

While the general approach for your experiment is given above, there are many details left to decide about exactly how you will take and analyze your data. Your group should start by determining a specific procedure. Think about what you need to measure and what analysis is needed to determine the coefficient of friction.

Your description should be such that someone familiar with the physical principles around friction, but not familiar with your experiment, could reproduce your results.

::: {.question #ph211-describing-an-experiment:describe-experiment}
**Describe your experiment in enough detail that someone else could reproduce it.**

a.  **Explicitly identify what you will vary and what you will measure. List the important parameters. (Hint: There are several parameters that should be the same each time the experiment is done.)**
b.  **Describe the procedure, including how to collect relevant data and what data to record.**
:::

::: action
- **If your experiment uses the force sensor, refer to the instructions below on how to set it up.**
:::

::: {.question #ph211-describing-an-experiment:statistical-uncertainty}
**For simplicity, we will assume that variation between seemingly identical measurements is the most significant source of uncertainty. Describe how you will determine this statistical uncertainty in your measurements.**
:::

::: {.question #ph211-describing-an-experiment:analysis-plan}
**Describe *how* you’ll analyze your data to find the coefficient of static friction. Remember, it’s always preferable to use a plot of your data for analysis instead of repeating a calculation for every data point. Don’t include the actual analysis here, just how you plan to do it.**
:::

::: action
- **Create a document that you will share with another lab group. Paste in your answers to questions 1, 2, and 3.**
:::

## Part 3: Collect Data

*[Experiment 1 (ramp):]{.underline}* Skip to Question 4 below.

*[Experiment 2 (force sensor):]{.underline}* Before taking data using the cart’s force sensor, you need to prepare it:

1.  Open Graphical Analysis ([graphicalanalysis.app](https://graphicalanalysis.app)) in Chrome or Edge. Choose *Sensor Data Collection*, click *Wireless*, and select your cart. Do *not* connect it using the computer’s Bluetooth settings.
2.  Open *Sensor Setup*.
3.  Open *Sensor Channels*.
4.  Select *Force*.
5.  Deselect *Position*.
6.  Click *Done*.
7.  At the bottom left, click *Mode* to open *Data Collection Settings*. Change *End Collection* from a set duration to *Manually*, and click *Done*.

Now you’re ready to run your experiment.

::: action
- **If necessary, prepare the force sensor as described above.**
:::

::: {.question #ph211-describing-an-experiment:our-data}
**Create a heading that says, “Our Data”. Under this, record your data in a table with labeled columns, including units. Include a description or value for each parameter in your list. \*\*\* [This should *not* be part of your shared document.]{.underline} \*\*\***
:::

**Don’t analyze your data yet. If you made any changes to your procedure, make sure you update it in the shared document. Reset your lab station so that it looks how you found it at the beginning of the lab.**

At this point, let your instructor know you’re ready to share your procedure. Your instructor will give you instructions on how to share your document with another group.

Once they have it, the other group will move to your lab station. They will use your apparatus to reproduce your experiment and find their own value for the coefficient of friction.

## Part 4: Reproduce Experimental Results

Your instructor will also give you a procedure from another group. You should [go to their station]{.underline} and run the experiment.

::: hint
- You cannot ask any questions; you must run the experiment using only the information in the procedure.
- If you are using the force sensor, see the note above about preparing it.
- If there is no procedure ready for you yet, you can analyze the results of your first experiment until a procedure is available.
:::

Run the new experiment, record your data, and analyze the results as described in the procedure.

**Be sure to run the experiment exactly as described, improvising only if and when it’s not clear what you should do. Do not change the procedure just because you think your idea will work better – that’s not the point and will invalidate the comparison of results later. [You may not ask the group who wrote the procedure for any guidance.]{.underline}**

::: action
- **Create a report on this experiment including the following:**
:::

::: report-item
1.  **Your data, neatly reported in a table with labeled columns.**
2.  **Your analysis.**
3.  **Your results including uncertainty, reported in** $\mathbf{A \pm \mathrm{\Delta}A}$ **format.**
4.  **Any confusion you had about what to do, assumptions you had to make, and any other problems you may have had. Be specific about any steps you had to improvise due to lack of information.**
:::

::: action
- **Paste this information directly into the shared document you were given.**
:::

## Part 5: Analyze the Data

Ask the instructor for the report of the other group that repeated your experiment.

::: {.question #ph211-describing-an-experiment:other-groups-report}
**Create a heading in your report called “Other Group’s Report”. Under it, paste the data, analysis, and results from the other group that used your description. *Make sure this is clearly distinguished from the data and results of your own experiment (it can help to change the color of text written by the other group).***
:::

::: {.question #ph211-describing-an-experiment:our-analysis}
**Create a heading that says, “Our Analysis”. Analyze your data from your original experiment (the one that you described) using the method in your procedure.**

a.  **Find the statistical uncertainty using the method you described in your procedure. Report your experimental value of the coefficient of friction in the** $\mathbf{A \pm \mathrm{\Delta}A}$ **format.**
b.  **Compare your results to the results of the group that repeated your experiment. Report the other group’s experimental value and uncertainty. Do your results agree? Defend your response using a quantitative comparison.**
c.  **Comment on any differences, considering any problems the other group may have had when repeating your experiment.**
:::

## Part 6: Reflect and Conclude

This activity is meant to help you understand the level of detail you need to include so that someone else can reproduce your work - an important part of reporting an experiment.

::: {.question #ph211-describing-an-experiment:better-explanation}
**As a group, choose one thing that you wish the other group had explained better, or some important or helpful detail that was missing. In addition, choose one thing your group could have explained better.**

a.  **For each item, explain how a better explanation would improve your ability to find a value for the coefficient of static friction. This might be improved consistency (less ambiguity in what to do), reduced uncertainty, or something else that gives you more confidence in your result.**
b.  **Be prepared to discuss some of your answers with the class. If there is no discussion today, bring a copy of your answers to the next class.**
:::

## Part 7: Submit Your Group’s Lab Report

Make sure everyone’s name is on your group’s lab report. If you submit through Gradescope remember to add everyone in your group to the assignment. This is done at the end of the submission process.

## Appendix – Reference Information

This section contains key information from previous labs:

1.  Required Plot Elements
2.  Linearization
3.  What is Uncertainty?
4.  Sources of Uncertainty
5.  Predictions, Hypotheses, and Models
6.  Tips for Using Graphical Analysis
7.  Variables and Parameters

### Required Plot Elements

::: action
- Do not connect the data points with lines.
- Make sure you create *Scatter Plots* and not *Line Plots*.
- Evaluate if the plot makes sense. Are the axes correct? Do you have the right number of data points?
- Include a descriptive title and labels on each axis, always including physical units.
- Add a legend, unless you only have one set of data and the title describes it.
- Display the equation and R^2^ value for any trendline you include.
:::

### Linearization

In the context of data analysis, “linear” refers to a directly proportional relationship between the dependent and independent variables in an equation.

::: action
- Mathematically, if two variables $x$ and $y$ have a linear relationship, we can express this as $y = mx + b$ where m and b are constants.
- More simply, we can write this as $y \propto x$ where $\propto$ means “is proportional to”.
- When graphed, data with a linear relationship falls on a straight line.
:::

**Linearization comes in handy when your data or hypothesis is *not* linear.**

When you fit data with a linear trendline, you are essentially checking whether the two variables are proportional to each other. To check a nonlinear hypothesis, can we instead check if one variable is proportional to *a function of* the other variable.

In practice, **linearization is done by calculating a new column of data** that gives the values of a function of the input variable. Typically, the input variable is the independent variable, and the function is chosen so that the resulting quantity is proportional to the dependent variable.

**Why Linearize?**

::: action
- Linear data is typically easier to understand and analyze.
- There are analysis methods we can apply to linear data that don’t work as well (or at all) with nonlinear data.
- It is relatively easy to fit a line to data - there are just two important values to determine: the slope and intercept of the data.
:::

### What is Uncertainty?

*Uncertainty* is the acknowledgement that we cannot measure things exactly, and so any conclusion based on measurements will always include a range of possible answers. When making a measurement, there is no single “true value” of the measurand (measured quantity) that we can determine. Instead, we can define an interval that defines the range of values that we think are *probable* for the measurand. The narrower the interval, the more precisely we can approximate the measurand.

When including uncertainty in a value, we report it as **A ± Δ~A~**. We believe the value is **A**, but we’re unable to rule out the possibility that it’s higher or lower by an amount **Δ~A~**. (Sometimes it’s written +Δ~1~ / -Δ~2~ if the higher and lower ranges are different.) For example, a time might be reported as 2.45 s ± 0.03 s.

### Sources of Uncertainty:

The uncertainty in a measurement can be due to a combination of several factors. A crucial aspect of experimentation is to identify all such sources of uncertainty and to numerically estimate their effect on your measurement result.

Common sources of uncertainty include:

a)  the effects of environmental conditions on the measurement
b)  your judgement in reading analogue instruments
c)  the sensitivity of your instruments (e.g. the digital scale)
d)  the rating or stated calibration of the instrument
e)  approximations and assumptions that you make while doing the experiment
f)  variations in repeated readings made under apparently identical conditions

**[Predictions, Hypotheses, and Models]{.underline}**

Experiments are designed to check our understanding of the physical world. An idea about how the world works is a **hypothesis** and is often represented by a **model** that quantifies this idea. In physics, a model is usually an equation. Based on a hypothesis, scientists make specific **predictions** about what will happen in their experiment.

For an experiment to be a valid test of a hypothesis, it must be designed so that the data (and subsequent analysis) can either agree or disagree with the prediction. If the data agree, then we say the hypothesis is **supported** by the data, if not, it is refuted.

We do not refer to hypotheses as “correct” or “incorrect”, rather we discuss the degree to which data support our hypotheses. Models are always just that - a model to describe what we observe. Experiments help us determine to what degree our model works.

### Tips for Using Graphical Analysis:

::: hint
- Adjust what is displayed using *View* icon, ![Graphical analysis view icon](ph211-describing-an-experiment-handout-media/graphical-analysis-view-icon.png){width="0.1437in" height="0.1437in"} (top right corner). This will allow you to change the number of graphs displayed and to display the data tables.
- Adjust the graph display and fit data using the *Graph Tools* ![graphical analysis graph tools icon](ph211-describing-an-experiment-handout-media/graphical-analysis-graph-tools-icon.png){width="0.1437in" height="0.1437in"} .
- Change what is shown on either axis of a graph by clicking on the axis label.
:::

Change the data collection by clicking on *Mode* (bottom left) and choosing *Data Collection Settings*. You can adjust other items as well using the *Mode* menu.

### Variables and Parameters

It will help you when designing your experiment to think about the different types of numerical quantities that are involved. It will make your explanation clearer if you label the different quantities appropriately.

*Independent variable*: In an experiment you will usually vary one quantity at a time in a controlled manner. This is the independent variable. Typically, you’re trying to discover how the independent variable affects the system.

*Dependent variables*: Your hypothesis should predict the behavior of other quantities in your system as the independent variable is changed. These other quantities are referred to as the dependent variables because their values depend on the value of the independent variable.

*Parameters*: There are other quantities you should specify because they may influence your results, but that will remain fixed throughout the experiment. These are referred to as parameters. Examples could be the length of a track or the mass of an object. The key is that a parameter doesn’t change at any time in the experiment.

In short, parameters are fixed, and variables change. The change is either under your control (independent) or a response to the experiment (dependent).
