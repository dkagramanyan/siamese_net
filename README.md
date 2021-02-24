Classification with seamese network
===================================

Siamese networks are interesting as 
they make Euclidean distance between similar and different 
images equals to 1 ans 0 respectively 

Training architecture
---------------------

![training](architecture%20diagrams/training.JPG)

Data
----

I used 2 datasets

* Saint Georges (https://drive.google.com/drive/folders/1hXAjwpBj6shfWd1taWMFpSqelFCzi6KJ)
* SoF dataset (https://www.sites.google.com/view/sof-dataset)

Preprocess
---------

Saint George dataset was only resized to smaller shape

For SoF dataset was used segmentaion and face highlighting from dlib

Tests
-----

Model train extremely long. I train each model for 4 hours. 
As a result - accuracy for SoF and Saint Georges datasets 
equals 0.5

It means, model prediction is similar to coin flip probability

To increase accuracy of the model is necessary to train more complex 
model architecture and increase the number of epochs. 
In other words - more powerful GPU is required :)

Inference
---------
![inference 1](architecture%20diagrams/inference.JPG)
