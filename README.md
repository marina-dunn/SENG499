# SENG499
The repository to hold the code for the SENG 499 Capstone Project.
https://github.com/marina-dunn/SENG499

face-recognition installation:
-Python3
-pip3
-cmake
-dlib

    apt-get update
    apt-get install build-essential cmake
    apt-get install libopenblas-dev liblapack-dev 
    apt-get install libx11-dev libgtk-3-dev
    apt-get install python python-dev python-pip
    apt-get install python3 python3-dev python3-pip
    
    Install dlib (can take some time to build)
    ------------------------------------------
    cd ~
    mkdir temp
    cd temp
    git clone https://github.com/davisking/dlib.git
    cd dlib
    mkdir build; cd build; cmake ..; cmake --build .
    cd ..
    python3 setup.py install
    
    face-recognition (will take some time to install)
    -------------------------------------------------
    pip3 install face_recognition
    
Potential libraries for machine learning:
-scikit-learn
-numpy 
-scipy 
-matplotlib 
-pandas

face_test.py
-sample code for face-recognition, outlines facial features of given image

proc_face.py
-given single image outputs csv with processed data points

gen_test_data.py
-given a directory of face images outputs proccessed data points for each

Processed data format:
sample number, facial feature, x:y, x:y, ...

Classified Images (/media/identified_gestures/)
Classes: Smiles, Neutral, Frown, Other

Other - gestures that do not fit into any category or have some object obscuring the face

First pass, good selection of smiles and neutral. May need more frowning samples. Often neutral class can contain some abiguity so should be passed over again.

Processed data points are currently relative to first data point (x0 - x:y0 - y). Some ideas for other point references, center of cluster (k-means), mean point.
Could also repfresent points at distance angle from a mean point (could perhaps identify convex or concave curve of mouth)


# Docker
Docker compose has been setup to run the facial and gesture recognition server as well as the webserver
The facial and gesture recognition server is setup to build off a server_base image which contains the built dlib library and other requirements

Run the following command to build the server_base image
Windows: build_base.bat
Linux: ./build_base.sh

Once the base image has been created it will not need to be recreated unless the dlib library or other requirements have updated/changed

To build the server suite
docker-compose build

To run the server suite
docker-compose up

To build and run the server suite in one go
docker-compose up --build

Launch server in gathering mode, connect client and be smiling/frowning
docker-compose run --service-ports facial_features -s 127.0.0.1 -p 40000 -g {ACTION}
{ACTION} is either 0, 1, or 2

Image trainer can be used with prepared images while server is in gather mode and also for confirmation
python image_trainer.py -s 127.0.0.1 -p 40000 -a {ACTION}
{ACTION} is either 0, 1, or 2 same as server
The script can be edited to look at different folders