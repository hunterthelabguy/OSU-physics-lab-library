# Presentation evidence review

Status: draft for owner rulings, 2026-09-19. Nothing here is ruled; rulings
go in [../LEDGER.md](../LEDGER.md). Scope: how the converted curriculum
should look and be structured once the faithful conversion is done, weighed
against the previous coordinator's Lab Handout Style Guide (July 2024) and
the Lab Skills Matrix (July 2024), both in the original materials.

Every citation below was checked against a publisher or index page on
2026-09-19. Where a recommendation goes beyond what a source tested, it is
marked as an inference.

## Sources

1. Lorch, R. F. (1989). Text-signaling devices and their effects on reading
   and memory processes. *Educational Psychology Review, 1*(3), 209-234.
   doi:10.1007/BF01320135. Review across headings, previews, typographical
   cues and more: signals improve memory for the cued content; memory for
   uncued content is often unaffected.
2. Lorch, R. F., Jr., et al. (1995). Effects of
   typographical cues on reading and recall of text. *Contemporary
   Educational Psychology, 20*(1), 51-64. Light underlining of targets
   improved cued recall over no cues; heavy underlining (targets plus half
   the other sentences) did not differ from no cues.
3. Schneider, S., Beege, M., Nebel, S., & Rey, G. D. (2018). A meta-analysis
   of how signaling affects learning with media. *Educational Research
   Review, 23*, 1-24. 103 studies, N = 12,201: signaling improves retention
   and transfer and reduces cognitive load; prior knowledge was not a
   moderator.
4. Rey, G. D., Beege, M., Nebel, S., Wirzberger, M., Schmitt, T. H., &
   Schneider, S. (2019). A meta-analysis of the segmenting effect.
   *Educational Psychology Review, 31*, 389-419.
   doi:10.1007/s10648-018-9456-4. Learner-paced, meaningful segments beat
   continuous presentation (small to medium effects on retention and
   transfer). The studies are mostly multimedia and animation, not printed
   handouts.
5. Rey, G. D. (2012). A review of research and a meta-analysis of the
   seductive detail effect. *Educational Research Review, 7*(3), 216-237;
   and Sundararajan, N., & Adesope, O. (2020). Keep it coherent: A
   meta-analysis of the seductive details effect. *Educational Psychology
   Review, 32*(3), 707-734. doi:10.1007/s10648-020-09522-4. Interesting but
   nonessential material reduces learning (small to medium effects).
6. Kalyuga, S., Ayres, P., Chandler, P., & Sweller, J. (2003). The expertise
   reversal effect. *Educational Psychologist, 38*(1), 23-31.
   doi:10.1207/S15326985EP3801_4. Guidance that helps novices can hinder
   learners with more knowledge.
7. Delgado, P., Vargas, C., Ackerman, R., & Salmerón, L. (2018). Don't throw
   away your printed books: A meta-analysis on the effects of reading media
   on reading comprehension. *Educational Research Review, 25*, 23-38.
   Comprehension is lower on screen than on paper, with a stable effect for
   expository text.
8. Dyson, M. C. (2004). How physical text layout affects reading from
   screen. *Behaviour & Information Technology, 23*(6), 377-393. Review of
   line length, columns, window size, and line spacing; characters per line
   is the variable that matters for line length.
9. Meyer, A., Frederick, S., et al. (2015). Disfluent fonts don't help
   people solve math problems. *Journal of Experimental Psychology: General,
   144*(2), e16-e30. The original experiment pooled with 16 replications
   showed no benefit from hard-to-read fonts.
10. Wery, J. J., & Diliberto, J. A. (2017). The effect of a specialized
    dyslexia font, OpenDyslexic, on reading rate and accuracy. *Annals of
    Dyslexia*; and Kuster, S. M., van Weerdenburg, M., Gompel, M., & Bosman,
    A. M. T. (2018). Dyslexie font does not benefit reading in children with
    or without dyslexia. *Annals of Dyslexia*. doi:10.1007/s11881-017-0154-6.
    Neither specialty font improved reading.
11. W3C. WCAG 2.2, Success Criterion 1.4.8 Visual Presentation (Level AAA):
    a mechanism for lines of at most 80 characters, no full justification,
    line spacing at least 1.5, paragraph spacing at least 1.5 times line
    spacing, and resizing to 200 percent without horizontal scrolling.

## What the evidence says about the style guide

The style guide mixes two kinds of rules.

**Semantic rules** give the reader a consistent code: round bullets for
things to do, arrows for hints, bold "1)" for graded questions, unbolded
numbered procedures, boxes for key concepts, alt text on every image, and a
consistent section order (create a model, plan, collect, analyze,
conclude). A consistent code is signaling, which has the strongest support
here (sources 1, 3). The conversion already encodes the bullet and question
rules as data (ledger 19, 23).

**Physical rules** are Word settings: Calibri Light 28 pt titles, Times New
Roman 12 pt body, indents in inches, 6 and 12 pt spacing. They were tuned to
a printed Word page. On the web, the display decides these, and the evidence
gives no support for tuning them beyond ordinary legibility: deliberately
hard fonts do not help (9), specialty dyslexia fonts do not help (10), and line
length and spacing matter mainly at the extremes, which WCAG 1.4.8 bounds
(8, 11).

One style-guide rule is a Word workaround that the web replaces: the box
drawn as a one-cell table with the box text copied into the table's alt
text. A web page can mark a box as a labeled aside, which screen readers
handle natively, so the duplicated alt text goes away.

## Findings that need owner judgment

1. **Keep the semantic rules, retire the physical ones?** Lean: yes. The
   semantic rules become the conversion format (already partly done), and
   the physical rules become web defaults set from source 11 and the OSU
   palette. The style guide itself is kept as an original, credited.
2. **Bold is overloaded (ledger 25), and the evidence supports your doubt.**
   Light, consistent cueing helps; heavy cueing is no better than none
   (source 2). The handouts use bold for graded questions and also for
   instructions, labels, and emphasis, and the style guide allows "bold or
   underline when needed" in body text. Inference: if a student must answer
   exactly the cued items, the cue should mean one thing. The content-change
   phase could give graded questions their own labeled block (the format
   already marks them) and free bold for emphasis. Decision for that phase,
   not now.
3. **Screen or paper for the handout in the room?** Source 7 says
   comprehension of expository text is lower on screen. Lab handouts are
   read before and during lab; how students read them now (paper, laptop,
   phone) is not known and would be worth asking. Lean: the printed
   form (Word or PDF) stays a first-class output, not an afterthought, and
   the web version is for finding, linking, and reference. This affects what
   the site treats as the primary student artifact.
4. **Density: segment and move optional material off the main path?** The
   segmenting and seductive-detail findings (4, 5) favor meaningful chunks
   and keeping nonessential material out of the main line. Inference: the
   web can collapse the optional appendix in Lab Guidance for Students ("For
   the advanced student") and link to it, not interleave it. The segmenting
   evidence is mostly from animations, so treat this as a hypothesis to try,
   not a settled result. Content-change phase.
5. **The skills matrix is the fading map; make it data?** The README says
   the labs give less guidance as the year goes on, which is the
   expertise-reversal logic (source 6). The matrix's codes (Tells, Shows,
   Teaches, Scaffolds, Asks, Expects) record exactly that fading, lab by lab.
   Lean: convert it to a data file in the instructor repo, with competencies
   given descriptor ids and columns keyed to lab ids instead of lab numbers
   (ledger 14), so that "does competency X fade properly across the year"
   becomes a query. Two cautions below.
6. **Which competency list is canonical?** The matrix has 65 competency
   rows. 38 of them do not match the wording in Lab Guidance for Instructors
   exactly; some are rewordings ("within the group" versus "within a
   group"), others appear only in the matrix (for example "Find the
   uncertainty in a slope", "Metacognition"). Ledger 5 applies: you rule
   which list is canonical before either is converted.

## Cautions on the matrix as a source

- Cell colors carry meaning ("Needs attention or is a missed opportunity";
  "Too broad to specify"); a text extraction loses them. The conversion
  must read fills, and the check must compare them.
- Many comments are attributed to a named person. Under roles-not-names,
  the comments convert with the name replaced by a role, which is a ruled
  change. The sheet "Full Curr." repeats the other sheets with numeric codes
  (1 to 6); convert one form, not both.
