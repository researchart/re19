# Labelled_Forum_Sentences (Artifact RE-2019)
## Contact details

RE Submission ID: 17

## Overview
This repository contains "Artifacts" from our research on software product forums. The research is described in our paper "Can A Conversation Paint A Picture? Mining Requirements In Software Forums", submitted to the Requirements Engineering conference 2019.

The Artifact is the manually labelled, software product forum feedback, created in our research and used as the truth set for RQ2 and RQ3. The feedback is labelled per sentence, with 1 of 18 forum feedback classifications, detailed in our paper. 

## Database file

The labelled sentences are contained in "VLC_labelled_sentences_4RE.sqlite". The database contains three tables: (1) labelled_sentences; (2) verbs; (3) POS.

The "labelled_sentences" table contains the feedback sentences and the manual labels.
Each DB table's contents are described below.

### labelled_sentences

| Column Names  | Description           | 
| ------------- |:-------------:| 
| id     | Links the three DB tables | 
| topic_forum   | The forum/subforum the feedback is from     | 
| post_position | Forum field the feedback is from: title, initial post, reply, etc      | 
| user_level     | User level of the feedback author | 
| sentence   | Feedback sentence      | 
|label | Manually given sentence label      | 

### verbs
This table contains the verb counts for each feedback sentence. The tables are linked via the id column

| Column Names  | Description           |
| ------------- |:-------------:| 
| id     | Links the three DB tables | 
| |     | 

### POS

This table contains the POS counts for each feedback sentence. The tables are linked via the id column

| Column Names  | Description           | 
| ------------- |:-------------:| 
| id     | Links the three DB tables | 
| |     | 
