## Installation Instructions

* Create virtual environment with Python 3.6 (!)
* Install the dependencies denoted in the requirements.txt file via pip3
* Run ml.py and provide the path to a configuration file (see /conf directory) as the first parameter
* Results are saved as a report in the /reports directory
* The dataset used for the paper as well as the word2vec model are not included and must be replaced by your own data. However, a sample dataset is provided.
* If a pre-trained w2v model shall be used, this must be specified in the configuration files (example in "pvm-multi-pretrained.conf"), Format: gensim
* Otherwise, the w2v model will be retrained on each pass (based on the specified corpus file)