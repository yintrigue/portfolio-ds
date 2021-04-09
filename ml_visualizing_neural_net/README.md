# Visualizing EfficientNet-B0 
**v1.0.1**

**Algorithms:** PCA, Convolutional Neural Network, EfficientNet-B0, Focal Loss
**Tech Stack:** TensorFlow, Keras, TPU, GCS, Python  

## Description
The project explores ways to visualize the learning progress of EfficientNet-B0, a convolutional neural network published by Google in 2019. The training dataset consists of a total of **33,126 images**, of which there are only **584 positive examples**. More information about the dataset can be found on the  [homepage](https://www.kaggle.com/c/siim-isic-melanoma-classification/overview) of Kaggle's competition, *SIIM-ISIC Melanoma Classification*.

## Methodology

Embeddings from EfficientNet-B0 are extracted and projected onto a 2D plane using PCA prior to entering the dense layer with sigmoid activation. The PCA-reduced 2D plane is then plotted and images close to each other (by Euclidean Distance) within the same region are rendered for examination. 

<img src="./img/pca.jpeg" width="700"/>

## Results

Clusters start to form with just one epoch of training on Efficient-B0. The separation between the Benign and Melanoma examples starts roughly from the 6th epoch.

<img src="./img/efficientnet_b0_learning.gif" width="700"/>

In addition, images close to each other at the end of the first epoch of training strongly resemble to each other visually. Two randomly selected regions are plotted to demonstrate the observation.

**Region 1:**

![results_1](./img/results_1.png)

![results_1](./img/results_2.png)

**Region 2:**

![results_3](./img/results_3.png)

![results_4](./img/results_4.png)

However, by the end of the 10th epoch, examples close to each other **no longer look similar** even when they are correctly classified by EfficientNet-B0. Why? My hypothesis is that with 10 epochs of training, EfficientNet-B0 is now picking up subtitle details that can no longer be understood by my untrained eyes. 

Wow! EfficientNet-B0 is on its way to become an expert on diagnosing Melanoma!

![results_5](./img/results_5.png)

![results_6](./img/results_6.png)

## Repository 

- `nn_visualization.ipynb` is the notebook for the analysis.
- `lib.py` is the Python module that contains all the classes and functions used for constructing the CNN model.
- `./img` contains the images used for the readme markdown.  

