# Visualizing EfficientNet

**Models:** EfficientNet-B0, PCA, [Focal Loss](https://arxiv.org/abs/1708.02002)
**Tech Stack:** TensorFlow, Keras, TPU, GCS, Python  

## Description
The study explores ways to visualize the learning progress of EfficientNet-B0, a convolutional neural network published by Google in 2019. The training dataset consists of a total of **33,126 images**, of which there are only **584 positive examples**. Note that the study is an extract of the project, [Classification Melanoma](https://github.com/yintrigue/portfolio-ds/blob/master/ml_melanoma).

## Methodology

Embeddings from EfficientNet-B0 are extracted and projected onto a 2D plane using PCA prior to entering the dense layer with sigmoid activation. The PCA-reduced 2D plane is then plotted and images close to each other (by Euclidean Distance) within the same region are rendered for examination. 

<img src="https://www.dropbox.com/s/m86wwr5a57gw1u4/pca.png?raw=1" width="800"/>

## Results

Clusters start to form with just one epoch of training on Efficient-B0. The separation between the Benign and Melanoma examples starts roughly from the 6th epoch.

<img src="https://www.dropbox.com/s/ue1zaqgep1ppxsf/v_efficientnet_01.jpg?raw=1" width="600"/>

<img src="https://www.dropbox.com/s/dgqkusay0tmcsll/v_efficientnet_02.jpg?raw=1" width="600"/>

<img src="https://www.dropbox.com/s/9swl54rxptbh0qs/v_efficientnet_03.jpg?raw=1" width="600"/>

In addition, images close to each other at the end of the first epoch of training strongly resemble to each other visually. Two randomly selected regions are plotted to demonstrate the observation.

**REGION 1**:

<img src="./img/results_1.png" width="500"/>
<img src="./img/results_2.png" width="700"/>

**REGION 2**:

<img src="./img/results_3.png" width="500"/>
<img src="./img/results_4.png" width="700"/>

However, by the end of the 10th epoch, examples close to each other **no longer look similar** even when they are correctly classified by EfficientNet-B0. Why? My hypothesis is that with 10 epochs of training, EfficientNet-B0 is now picking up subtitle details that can no longer be understood by my untrained eyes. 

Wow! EfficientNet-B0 is on its way to become an expert on diagnosing Melanoma!

<img src="./img/results_5.png" width="500"/>
<img src="./img/results_6.png" width="700"/>

## Repository 

- `nn_visualization.ipynb` is the notebook for the analysis.
- `lib.py` is the Python module that contains all the classes and functions used for constructing the CNN model.
- `./img` contains the images used for the readme markdown.  

