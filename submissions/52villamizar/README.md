# SUBMISSION 52

This repository contains the instrumentation of the controlled experiment that was conducted in the study named "An Approach for Reviewing Security Related Aspects in Agile Requirements Specifications of Web Applications". You can access to the following artifacts:

* Characterization Questionnaire: The overall goal of the questionnaire is to characterize the experience of the students. The answers were obtained through the questionnaire with the aim at identifying some key characteristics about four knowledge areas: agile software development, requirements engineering, software security and inspections.

* Follow-up questionnaire. This questionnaire was based on TAM (Technology Acceptance Model). We wanted to know if the approach was useful for them and if they found it easy to use. Additionally, we included some open text questions to gather participant feedback about difficulties, benefits and disadvantages of using our approach.

* Training. The training material focused on the OWASP security properties and high-level security requirements and on the defect types. No specific training was provided on using the reading technique; therefore, the feasibility of using it without specific training was also indirectly evaluated.

* Task description. This description explains the participants about the received material and asks them to conduct the review according to their treatment, filling out the defect reporting form. Both treatments received the same requirements specification. For one treatment, the reading technique was generated according to the user story description and its related OWASP highlevel security requirements. For the other treatment the list of OWASP security properties and their related high-level security requirements was provided together with the description of the defect types to be located.

* Defect reporting form. This form was used by participants to record the start and end time of the inspection, as well as the defects by location, type and description. The defect reporting form for the experimental group was the one generated for applying the reading technique.

The artifacts were organized in 3 phases. This depends on the phase where the artifact is used.

* Pre-experiment
* Experiment
* Post-experiment

In addition, this repository contains the results of the controlled experiments for any validation procedure.

In order to make available the experiment package with all the instruments and the results, we followed open science policies that are available on [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3273298.svg)](https://doi.org/10.5281/zenodo.3273298)

# FESRAS

This repository also contains the files of the Software Framework for Eliciting Security Requirements in Agile Specifications (FESRAS). To extract the keywords of the agile specifications in format of user story, we developed the software framework that uses the Stanford CoreNLP tool (see more at https://github.com/stanfordnlp/CoreNLP) through a library that provides a set of natural language analysis tools written in Java. The library represents each sentence as a directed graph where the vertices are words and the edges are the relationships between them. Thereby, the software framework can take the verbs and nouns of the user story and then analyze them in order to link security properties. 

In the following we describe the main purpose of the framework.

## Objective

The goal of this framework is to map OWASP high-level security requirements from text documents that describe desired software behaviors (user stories) in the context of agile methods.

The main features of FESCARS are briefly described as follows:

* **Insert file.** The software framework must allow the user to load TXT and Word files.
* **Process file.** The software framework must allow the user to read TXT and Word files that contain software behaviors (user stories).
* **Extract assets and operations.** The software framework must allow the user to process natural language to extract relevant verbs and nouns from the files.
* **Map security objective.** The software framework must allow the user to map security objectives from the assets and operations extracted.
* **Map security controls.** The software framework must allow the user to map security controls from the security objectives extracted.

## Installation Instructions

All our scripts are contained in directory that contains the files needed to run the software framework. Please follow the steps mentioned below:

* Users need to install an integrated development environment (IDE), preferably, download Eclipse (go to https://www.eclipse.org/downloads/).

* Download the public git repository (https://github.com/hrguarinv/FESRAS/tree/master/Framework_pss) in your local machine and then, import the repository downloaded as an "Existing Maven Project" in Eclipse. 

* Run the project opened in the IDE. The framework will show a JFrame (Java Frame). 

* Please choose any of the TXT files (UserStory_1.txt, UserStory_2.txt, UserStory_3.txt) that are part of the root of the public repository downloaded.

* Wait a few minutes for the output of the software framework (OWASP high-level requirements that address the security specification mentioned in the user story).

