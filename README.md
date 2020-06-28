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
