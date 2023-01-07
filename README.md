# markov-model
This repository constitutes a python implementation of a k-order Markov model for text-based speech recognition. The key files are:

### Hashtable.py
Contains a linear-probing hashtable, with logical deletion and default values for deleted/non-existent keys.

### Markov.py
Code for creating a Markov class that accepts input text to "build" a speaker model using on the hashtable.py. Markov.py also includes a function (identify_speaker) that calculates the most likely speaker of an unknown sample given two known samples.


### Benchmarking the Hashtable
Below is a graph benchmarking the performance of this hashtable implementation compared to Python's dictionary
![performance](https://user-images.githubusercontent.com/107568169/211171429-8c248c16-2c0c-4f1a-9109-a7df9113faf1.png)


