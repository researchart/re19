# FESRAS
This repository contains the files of the Software Framework for Eliciting Security Requirements in Agile Specifications (FESRAS). To extract the keywords of the agile specifications in format of user story, we developed the software framework that uses the Stanford CoreNLP tool (see more at https://github.com/stanfordnlp/CoreNLP) through a library that provides a set of natural language analysis tools written in Java. The library represents each sentence as a directed graph where the vertices are words and the edges are the relationships between them. Thereby, the software framework can take the verbs and nouns of the user story and then analyze them in order to link security properties. 

In the following we describe the main purpose of the framework.

## Objective
The goal of this work is to map OWASP high-level security requirements from text documents that describe desired software behaviors (user stories) in the context of agile methods.

The main features of FESCARS are briefly described as follows:

* **Insert file.** The software framework must allow the user to load TXT and Word files.
* **Process file.** The software framework must allow the user to read TXT and Word files that contain software behaviors (user stories).
* **Extract assets and operations.** The software framework must allow the user to process natural language to extract relevant verbs and nouns from the files.
* **Map security objective.** The software framework must allow the user to map security objectives from the assets and operations extracted.
* **Map security controls.** The software framework must allow the user to map security controls from the security objectives extracted.

## Installation Instructions

All our scripts are contained in directory that contains the files needed to run the software framework. Please follow the steps mentioned below:

* Users need to install an integrated development environment (IDE), preferably, download Eclipse (go to https://www.eclipse.org/downloads/).

* Download the public git repository (https://github.com/hrguarinv/FESRAS/tree/master/Framework_pss) in your local machine and then, import the repository downloaded as a "Existing Maven Project". 

* Run the project opened in the IDE. The framework will show a JFrame (Java Frame). 

* Please choose any of the TXT files (UserStory_1.txt, UserStory_2.txt, UserStory_3.txt) that are part of the root of the public repository downloaded.

* Wait a few minutes for the output of the software framework (OWASP high-level requirements that address the security specification mentioned in the user story).