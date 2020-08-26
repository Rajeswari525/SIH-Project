# Smart India Hackathon(SIH) 2020

# Problem Statement:- Baggage and other accessories Detection and Compilation in Database

## Solution Approach:-
This solution abstracts the automation of identification of the crime suspects without indulging the man power,thereby making it secured and fastened process. The software built will be taking the details of person baggage or other accessories and its features or an image of the baggage and then on the basis of the location and timestamp provided the software extracts the video footage from the CCTV's around that location of crime and suspected crime routes and then processes the video footage frame by frame and extracts the baggages along with their features which are present in the collected videos and then check each of the baggage attributes with the lost baggage and finds a list of baggages with similar attributes and then the person who lost his baggage checks out with the suspected baggages and if his baggage is found we can find the main culprit.

## Technologies Used:-
Languages - Python (Python being flexible and open sourced has a massive collection of libraries for processing complex operations on data )

Frameworks - TensorFlow,OpenCV (Tensorflow provides an entire ecosystem to help you solve challenging,real world problems like object detection) 

Deep Learning - Convolutional Neural Networks ( CNNs together helps to improve the performance and accuracy of model )

User Interface - Tkinter (Tkinter is the Python interface to the Tk GUI toolkit shipped with Python that helps in easy development of Graphical User Interface(GUI) )

DataBase - Firebase Realtime Database,Firebase Storage ( The Firebase Realtime Database lets you build rich, collaborative applications by allowing secure access to the database directly from client-side code and also giving the end user a responsive experience when the user is offline )

![Image 1](https://github.com/Rajeswari525/SIH/blob/master/pic-1.png?raw=true)

![Image 2](https://github.com/Rajeswari525/SIH/blob/master/pic-2.png?raw=true)


# References
## Faster_RCNN Architecture
1) https://www.analyticsvidhya.com/blog/2018/10/a-step-by-step-introduction-to-the-basic-object-detection-algorithms-part-1/
2) https://medium.com/object-detection-using-tensorflow-and-coco-pre/object-detection-using-tensorflow-and-coco-pre-trained-models-5d8386019a8
## Inception Architecture
1) https://www.geeksforgeeks.org/inception-v2-and-v3-inception-network-versions/
## Multi Output Multi Label Classification
1) https://www.pyimagesearch.com/2018/06/04/keras-multiple-outputs-and-multiple-losses/
