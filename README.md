# emotion-recognition-iemocap

Deep neural networks have been shown to be effective for emotion recognition when encoding information from multiple modalities.
In this work, we measure the contribution of each modality to the overall performance of a model that encodes the information using a modern self-supervised transformer-based architecture.
In particular, our classifier encodes audio using the latest wav2vec 2.0 model, as well as transcribed text using BERT. 
The encoded information from both models are combined into a single feature vector which we use for training a deep neural classifier.
We measure the contribution of this composition and compare it with the performance of models that use single modalities.
Additionally, we measure the contribution of each encoded modality in the multi-modal settings, by intentionally hiding information from the input at inference time which may be important for emotion recognition (e.g., pitch modulation, masking specific word categories), and measure the overall performance of the model. 
We show that the performance of the multi-modal classifier is more resilient to corrupted inputs than the single-modality models, suggesting that the modalities are encoded in such way that allows the multi-modal classifier to dynamically balance the encoded information, to compensate for the missing information. 

![image](https://github.com/dror-co/emotion-recognition-iemocap/blob/master/multi-modal-architecture.png)

## Before Executing

* Downloal iemocap at <a herf="https://sail.usc.edu/iemocap/">iemocap</a>
* Go to Data directory
* Execute the following script to summarize the data `python3 get_data.py <PATH-TO-LOCAL-IEMCOAP-DB>`

## Train models
Each model has directory which contains notebook for define and train the neural network and the other notebook tesst the model performances including cases for corrupted data.

You can use our source code to train your own models and test them by yourself.
