An important aspect of engineering research is the study and production of research *artifacts*. An artifact is the tangible part of the research process, either produced in the domain of study, or produced by the researcher during the study. By tangible, we mean the artifact can be manipulated and exists independently of the study itself.

The open science era recognizes that artifacts are critical to the reproducibility of engineering research. It is difficult to validate claims about novel or important new findings without being able to analyze the underlying artifacts that were studied or created. This is why the notion of Artifact Evaluation Committees (AEC) has grown in importance. An AEC assesses the artifacts associated with a study (typically as part of a conference submission). As part of this assessment, AECs can assign a badge or marker indicating how suitable the artifacts are for reproducing the results of the study, ranging from the fact that artifacts exist (functional), all the way to artifacts that have been used in new studies (reproduced).

For the first time, the Requirements Engineering conference in 2019 will include artifact evaluation for those authors who wish to participate. A small AEC will evaluate accepted research papers that submit for badging, and assign one or more of the five ACM/IEEE artifact badges.

# Why Now? The Drift From Artifacts in RE Research

# What Is An Artifact?
This naturally raises the question of what an RE artifact is. The wider software engineering community has created a [list of artifacts](https://github.com/researchart/all/blob/master/ListOfArtifacts.md) for AECs at ICSE18, FSE18, and ICSE19. The list, ranked in order of size, includes:
* research hypotheses
* statistical tests
* baseline results
* the actual paper itself
* data generated in the research, raw or derived
* executable models, and 
* delivery tools, such as containers and virtual machines.

Furthermore, this list makes the point that not all artifacts are equally interesting or relevant (for the purpose of open science), and that an artifact submission must include metadata, including rationale for why this is an important artifact, how to use it, and provenance.

# What Is An Artifact in RE? 
Some of these artifacts are less obviously applicable to the RE community. Accordingly, the RE AEC devised the following table as a guideline.

| Artifact | Example |
| --------- | ----- |
Software (implementations of systems or algorithms potentially useful in other studies) | Tool which searches for optimally consistent requirements specifications |
| Machine readable requirements models | IstarML or UML interchange formats |
| Human readable requirements models | PNG of large conceptual model |
| Traceability relations between artifacts | Excel spreadsheet linking requirements to source code |
| Data repositories | Requirements models, requirements text, survey raw data |
| Requirements in natural language form |  Textual requirements in a spreadsheet, DOORS, JIRA export.|
| User reviews  | Text repository of app reviews, product changelogs, and release notes. |
| Frameworks and APIs | A web-based service to highlight inconsistencies in natural language. |

This is not an exhaustive list, and other types of artifacts, including those in the link above, are welcomed. The purpose of the AEC process is to encourage and reward repeatable and open science practices. 

We look forward to your submissions! 

# FAQs
**Q1.** Badging (and reproduction) is silly. It fetishizes trivial results and ignores the big picture.

**A:** That is not a question. But seriously, badging has turned out to be a crazy-strong motivation for reproducibility. Better question is to ask "what is a better badge to award"?

**A**: Plenty of interesting results: see [ICSE Rose Track 2019](), [FSE ROSE Track 2019](), SANER RENE Track 2018]().

**A:** Badges improve artifact availability, as shown [in this study](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1002456).

**A**: Badges improve citations. More reproductions of the paper implies more citations. 

----

**Q2:** Not every study lends itself to reproducibility. Isn't badging implicitly impugning these studies?

**A:** There is a risk that badges confer status, and studies without badges are seen as inferior, even if a badge would be hard to earn (for example, on a purely theoretical result). However, we trust that the community would be able to discern the differences between an empirical study with no badge, and a theoretical study with no badge.
----
**Q3:** Requirements research is less amenable to reproducibility than other software engineering research, like repository mining or defect prediction.

**A:** See the "Drift Away" section above for a longer answer. But in general, as an engineering discipline, most RE research should have some implications for practice, and thus reproducibility of the results is important. 
----
**Q4**: Reproducibility implies criticism of the original study and leads to bad feeling in the community. 

**A:** It is certainly *possible* to conduct a replication, contradict the original findings, and deeply annoy the original authors. There are two responses to this. One, repeated tests of hypotheses are part and parcel of good scientific practice, and the fallibility of the original work should not imply any criticism of the researchers who conducted that work. But secondly, collegiality and etiquette suggest that prior to formal publication of a replication, the original study authors should be given an opportunity to comment on the new results. See Kahnemann, "A New Etiquette For Replication", Soc. Psych. 45, 310, (2014).
