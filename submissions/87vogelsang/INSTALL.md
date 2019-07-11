## Installation Instructions

* This software requires Linux (tested with Ubuntu 16.04.1 LTS)
* CUDA 9.0 and cuDNN 7.1.4 are required for GPU acceleration

* Create virtual environment with Python 3.6 (!)
* Install the dependencies denoted in the requirements.txt file via pip3
* Run ml.py and provide the path to a configuration file (see /conf directory) as the first parameter
* Results are saved as a report in the /reports directory
* The dataset used for the paper as well as the word2vec model are not included and must be replaced by your own data. However, a sample dataset is provided.
* If a pre-trained w2v model shall be used, this must be specified in the configuration files (example in "pvm-multi-pretrained.conf"), Format: gensim
* Otherwise, the w2v model will be retrained on each pass (based on the specified corpus file)

## Running without GPU support

* If you do not want to use GPU acceleration (and thus skip CUDA installation), replace tensorflow-gpu with tensorflow in requirements.txt

## Running on Windows

* We did not test the software on Windows.
* However, if you want to try to run the software on Windows, you can replace the tensorflow dependency with 'Theano==1.0.2' and adjust the keras configuration file (HOME/.keras/keras.json) as follows:

{
"floatx": "float32",
"epsilon": 1e-07,
"backend": "theano",
"image_data_format": "channels_last"
}
