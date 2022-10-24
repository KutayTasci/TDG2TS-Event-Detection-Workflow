# TDG2TS-Event-Detection-Workflow
Transforming Temporal-Dynamic Graphs Into Time-Series Data for Solving Event Detection Problems
This repository provides a reference implementation for my proposed workflow. This workflow aims to solve event detection problems on temporal-dynamic graphs. You can find comlete datasets (size>100MB) in; [Link](https://drive.google.com/drive/folders/1D8P9LBHXERWN_r-hiTWNU4HDe3VmVHbx?usp=sharing)

### Requirements
    python>=3.8
    networkx
    numpy
    pandas
    gensim==3.8.3
    node2vec
    matplotlib
    holoviews
    sklearn
    scipy
    merlion (InstallGuide is bellow)

### Merlion: A Machine Learning Library for Time Series
This implementation uses Merlion library for unsupervised time-series anomaly detection alogrithms. You can insatall the necessary libraries with using ``pip install salesforce-merlion[all]``. It is important to use ``[all]`` to able to use deep learning based methods.

For further information:

https://github.com/salesforce/Merlion
 
### tdGraphEmbed: Temporal Dynamic Graph-Level Embedding
In this study we have used tdGraphEmbed algorithm. Code in this repository is directly using the tdGraphEmbed implementation.

Futher information and source codes are available at:

https://github.com/moranbel/tdGraphEmbed

[Link](http://www.kiraradinsky.com/files/Temporal_Dynamic_Graph_Embedding__CIKM.pdf?fbclid=IwAR30gmFRxA8jqjOppnL1kGhUpwXKMQ1aJ1hUBR4lGprSTeroEHl7eTtAT0w)
