---
id: ph211-hypothesis-testing-handout
title: "Lab 4 – Hypothesis Testing"   # the original title text; see ledger 22
course: PH211
sequence: 4
audience: student
visibility: public
layer: curriculum
source_file: "originals/PH211/Lab 4 - Hypothesis Testing - Handout.docx"
source_sha256: "ced38c004f3745e17a4850ab223519960a67b79659e95783b44d0f14d5b61d18"
status: converted
images:
  - file: "ph211-hypothesis-testing-handout-media/cliff-river-town-diagram.png"
    source_part: "word/media/image1.png"
    sha256: "67125ffe2526ba417e45d31b4293f3592cec69d9bda15a37725dc80dad21473d"
---

# Lab 4 – Hypothesis Testing

## PH211 – General Physics with Calculus

**Experimental goal: Determine which hypothesis is supported and make a recommendation based on your conclusion.**

A fundamental part of the scientific process is hypothesis testing – using experimental results to determine whether a certain model is a good description of reality. A hypothesis, or model, is used to make predictions about expected behavior of a system. To test the hypothesis, scientists design an experiment to check those predictions. The data collected and analyzed in the experiment will either support or refute the predictions of the model.

## Learning Objectives

**Learning goal: Use quantitative evidence (such as R^2^ and/or the y-intercept for a particular fit) to decide whether a model is supported by experimental results.**

This lab activity is designed to help you practice the following skills:

1.  Determine what data needs to be collected.
2.  Use available equipment to collect data in a systematic way.
3.  Linearize data and create a linearized plot.
4.  Determine to what degree data supports a hypothesis.

## Equipment

::: action
- Inclined metal ramp
- Metal ball
- Landing pad
- Sticky tabs to mark ramp
- Paper
- Carbon paper
- Plumb bob (a pointed weight hanging directly below where the ball leaves the ramp)
- Measuring tape / meter stick
- Tape
:::

## Introduction: A Bitter Controversy

A new housing development is being built along the banks of the York River. Overlooking the river, across a river from where the houses are being planned, is a cliff with a small hill on top of it. Part way through construction of the new homes, workers dig up some boulders perched on the hillside across the river. They talk to the head of the project to express concern over the possibility that the boulders could roll down the hill, off the cliff, across the river, and hit them while they build new homes.

The project head is dismissive of their worries and tells the workers to go back to work. Still unsure of their safety, the workers approach their union - if the rocks roll down the hill, are they at risk of being hit by them? They are particularly worried about a boulder about halfway up the hill that they noticed did move a little bit after a recent rainstorm.

The union reaches out to a group of engineers and a group of geologists for their thoughts. The engineers did a quick study and concluded that the height of the rocks up the hill is directly proportional to the distance they’ll travel across the river $(d\  \propto \ h)$. This puts the workers at risk of the rocks hitting them (or eventually hitting the new homes being built). However, the geologists repeated the study and concluded that the height of the rocks is proportional to the distance they’ll travel squared $(d^{2}\  \propto \ h)$, which would cause the rocks to land in the river, rather than reach the workers. These two possibilities are sketched below.

**Your goal is to determine how the distance *d* depends on the height *h*, whether either of the two hypotheses are correct, and if any boulders could present a danger to the town.**

![A diagram showing the cliff on the left, a river in the center, and a town on the right. Above the cliff there is a hill with four boulders and the height between the boulders and the ledge of the cliff is labeled h. Two dotted lines extend from the cliff, one ends in the river and is labeled "h proportional to d squared" and the second ends on the town and is labeled "h proportional to d". The distance between the cliff and the end of the dotted line is labeled d.](ph211-hypothesis-testing-handout-media/cliff-river-town-diagram.png){width="6.5000in" height="3.3056in"}

Figure 1: The York River.

## Part 1: Review the Hypotheses

Both sets of experts investigated the situation using apparatus consisting of a slope and a steel ball. In both cases, the steel ball was rolled down the slope from different heights *h* and the resulting distance *d* was measured. The Head of the Physics Department at OSU has been approached to resolve the controversy and urgently asks you to investigate the situation with the same apparatus.

The Department Head wants a full report detailing all aspects of the experiments: measurements, calculations, and graphs as well as your findings on who is right or wrong. In particular, she would like you to pay careful attention to the graph of *d* vs. *h* compared to the graph of *d^2^* vs. *h*, and how these graphs were used to determine the proportionality, as she will be showing them to workers at a union meeting later this week. She also advises that you should measure wide ranges of values for your controlled variable(s), and that you should check that your results make sense as *h* approaches zero.

::: box
### Predictions, Hypotheses, and Models

Experiments are designed to check our understanding of the physical world. An idea about how the world works is a hypothesis and is often represented by a model that quantifies this idea. In physics, a model is usually an equation. Based on a hypothesis, scientists make specific predictions about what will happen in their experiment.

In this activity, you are given two hypotheses to test. Each predicts that the behavior of a falling boulder can be described by a particular model, either d ∝ h or d\^2 ∝ h.

We do not refer to hypotheses as “correct” or “incorrect”, rather we discuss the degree to which data support our hypotheses. Models are always just that - a model to describe what we observe. Experiments help us determine to what degree our model works.
:::

For an experiment to be a valid test of a hypothesis, it must be designed so that the data (and subsequent analysis) can either agree or disagree with the prediction. If the data agree, then we say the hypothesis is supported by the data, if not, it is refuted.

[In this lab the hypotheses and models have been provided to you.]{.underline} The engineers and geologists have proposed different models of how the distance *d* depends on the height *h*. **The prediction is that in your experiment, the height the ball starts at will be either i) proportional to *d*, or ii) proportional to *d^2^*.** You will focus on supporting or refuting each hypothesis by seeing whether the data agrees with either prediction.

The experiment to run has also been described, though you still need to determine the details of the experimental procedure and a method for analyzing your data. Once you’ve decided on a procedure, you’ll take data and use it to decide which group, if either, is correct.

## Part 2: Plan the Experiment

::: {.question #ph211-hypothesis-testing:experimental-setup}
**Describe your experimental set-up. Include a clearly labeled diagram that defines the relevant variables (such as *h* and *d*) and represents all important aspects of the experiment, including angles.**
:::

::: {.question #ph211-hypothesis-testing:data-to-collect}
**What data do you need to collect in order to choose between the different hypotheses – or in other words, what quantities will you need to measure and what range of values will you test? List the steps you will follow to collect your data.**
:::

It is important that you:

::: hint
- measure a large range of starting heights, from near the top to very close to the bottom. (It’s usually a good idea to explore as wide a range of values as possible.)
- repeat measurements to check results
- finish in the allotted time. This can conflict with the other points, so it’s important to think through your experiment. Talk to your instructor if you’re unsure of what to do.
:::

As you learned in the previous lab, all measurements have inherent uncertainty – there is a limit to what we can know about the measurand. For your reference, here is the list of common sources of uncertainty to consider:

a)  the effects of environmental conditions on the measurement
b)  your judgement in reading analogue instruments
c)  the sensitivity of your instruments (e.g. the digital scale)
d)  the rating or stated calibration of the instrument
e)  approximations and assumptions that you make while doing the experiment
f)  variations in repeated readings made under apparently identical conditions (statistical uncertainty)

:::: {.question #ph211-hypothesis-testing:uncertainty-sources}
**Consider sources of uncertainty in your planned experiment. For now, don’t include statistical uncertainty (item f). We’ll look at that later.**

a.  **You will be measuring the distance *d* that the ball travels. Which items from the list above are likely to be a significant source of uncertainty in your individual measurements?**
b.  **For each source you said was significant, estimate a value for the uncertainty associated with it and provide a justification for that value. Then, combine the values by adding in quadrature.**

::: hint
- Remember, independent uncertainties for any quantity *x* add in quadrature using the formula

$$\mathbf{\Delta}\mathbf{x}_{\mathbf{total}}\mathbf{=}\sqrt{\left( \mathbf{\Delta}\mathbf{x}_{\mathbf{1}} \right)^{\mathbf{2}}\mathbf{+ \ }\left( \mathbf{x}_{\mathbf{2}} \right)^{\mathbf{2}}\mathbf{+ \ldots}}$$
:::
::::

In addition to planning how you will collect data, it’s useful to consider how you can analyze that data to achieve your experimental goals before you start collecting it. Graphing is often an important part of analysis. Consider what graphs will help you test the hypotheses.

::: hint
- In physics, graphs are most often scatter plots. Convention is to put the variable you control on the x-axis and the result that you measure on the y-axis.
- **[Strong Recommendation for this experiment]{.underline}**: One of the hypotheses is *nonlinear*. You can check the validity of the hypothesis by *linearizing* the data. (You learned how to do this in the Data Analysis lab, refer to the appendix for a [reminder on how to linearize](#_Linearization).)
:::

::: {.question #ph211-hypothesis-testing:analysis-plan}
**Plan your analysis, taking the suggestions above into account. Your analysis should allow you to make a conclusion about which hypothesis is most supported by your data.**

a.  **Describe the graphs you will use (state what quantities go on each axis) to analyze your data to check each of the two predictions.**
b.  **Discuss how you will use them to check the hypotheses, stating explicitly the outcomes that would either support or refute each of the two hypotheses. Note: the outcomes should be quantitative – saying a plot “looks linear” is not enough.**
:::

## Part 3: Collect Data

You are now ready to perform your experiment.

::: {.question #ph211-hypothesis-testing:data-table}
**For each run that you do, record your measurements in the form of a data table with labeled columns, including units. This should include only what you measured (no analysis/calculations). It should also include the uncertainty in each measurement, which you estimated for one of the questions in Part 2. You can report each value in** $\mathbf{A \pm \mathrm{\Delta}A}$ **format, or you can use separate columns with your measurement in one column and the uncertainty in another.**
:::

## Part 4: Analyze the Data

Now that you have made repeated measurements, item f) from the list of uncertainty sources may be relevant.

::: {.question #ph211-hypothesis-testing:statistical-uncertainty}
**Incorporate statistical uncertainty.**

a.  **For each height, what was the range (difference between highest and lowest value) of your measured values of d?**
b.  **Does this spread represent a significant source of uncertainty? Compare the value to the values you estimated for other significant sources to justify your response.**
c.  **If the answer to part b was yes, incorporate this value by taking half of the range and adding it in quadrature with the other uncertainties you identified.**
:::

::: {.question #ph211-hypothesis-testing:analyze-data}
**Analyze your data:**

a.  **Analyze each set of data using the graphs and procedure you described above. Report your results in a way that will most clearly help you justify your conclusion about which relationship is more likely to be correct.**
b.  **What distance would you expect for a starting height of zero? Do sense-making on your results by checking how well each fit matches your expectations. That is, according to your analysis of the data, what distance is predicted for a starting height of zero for each model you are testing? Does that make sense?**
c.  **Your analysis should include at least two graphs. Attach them to this question.**
:::

## Part 5: Draw Conclusions

::: {.question #ph211-hypothesis-testing:conclusion}
**Make a conclusion: In light of what you found for zero height, along with the quality of the fits in your graphs, does your data support either of the hypotheses? If so, which one? If not, what does the data suggest for the relationship between height and distance? Support your conclusion using specific evidence from your analysis such as the R^2^ value and/or y-intercept for a particular fit.**
:::

*[For the rest of the activity, assume the hypothesis that you chose correctly describes the situation.]{.underline}*

## Part 6: Predict Future Behavior

It turns out that there is a dangerous looking boulder perched on the hill. You’ve been asked to use your data to predict where it will land if it comes loose.

Assume your experimental setup is a scale model of the actual situation:

A)  The cliff at the bottom of the hill is 20 m above the town.
B)  The highest boulders on the hill are *h* = 13 m above the bottom of the hill.
C)  The river at the bottom of the hill is 20 m wide.

::: {.question #ph211-hypothesis-testing:recommendation}
**Make a recommendation.**

a.  **Determine the scaling factor that relates your experimental results in cm to real-world distances in m. Do this by dividing the height of the cliff in the actual real-world situation (A) by the height from the floor to the bottom of the ramp in your experiment. What is the scaling factor? You can now use this to translate distances from your experiment to the real world, and vice versa.**
b.  **Use the scaling factor to determine the height on the ramp that corresponds to the height of the highest boulder (B). Then use your experimental results to determine how far a ball placed at that height on the ramp will travel before hitting the floor. Use your scaling factor (now in the opposite way) to determine how far that would be in the actual situation.**
c.  **Are the workers and the development in danger of being hit by a boulder? (Hint: How does your answer above compare to the distance from the bottom of the hill to the town?) What recommendation should the department head give to the union to ensure worker safety? Justify your recommendation with evidence from your data analysis.**
:::

### Check your prediction experimentally.

Finally, test your calculations above using your apparatus. What is the starting height of a ball that corresponds to 13 m? According to your calculations, what is the distance it should travel? Mark your predicted spot on the floor with tape or some other removable method.

::: {.question #ph211-hypothesis-testing:catching-cup}
**Ask your instructor to bring you the “catching cup.” Place a ball at the height you calculated. Then place the cup where you predicted it should land. With your instructor watching, launch the steel ball from the given height. Your goal is to have the ball land in the cup. (It might help to tilt it forward.) See how many adjustments it takes for you to successfully catch the ball. Did you catch it on the first try?**
:::

## Part 7: Reflect on the activity

This activity is meant to show how an experiment tests a hypothesis or model by checking a prediction.

:::: {.question #ph211-hypothesis-testing:reflection}
**Each lab member should write an individual concise paragraph reflecting on the lab. Identify each contribution by name. Each should specifically address the following:**

::: action
- **What is one thing you learned about hypothesis testing during this activity?**
- **How is the uncertainty in your measurements incorporated into the conclusions you make?**
:::
::::

## Part 8: Submit Your Group’s Lab Report

Make sure everyone’s name is on your group’s lab report. If you submit through Gradescope remember to add everyone in your group to the assignment. This is done at the end of the submission process.

## Appendix – Reference Information

This section contains key information from previous labs:

1.  Required Plot Elements
2.  Linearization
3.  What is Uncertainty?
4.  Sources of Uncertainty

### Required Plot Elements

::: action
- Do not connect the data points with lines.
- Make sure you create *Scatter Plots* and not *Line Plots*.
- Evaluate if the plot makes sense. Are the axes correct? Do you have the right number of data points?
- Include a descriptive title and labels on each axis, always including physical units.
- Add a legend, unless you only have one set of data and the title describes it.
- Display the equation and R^2^ value for any trendline you include.
:::

### Linearization {id="_Linearization"}

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
