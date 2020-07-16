import face_recognition
import sys
from PIL import Image
import glob

gesture = sys.argv[1]

with open('{}.csv'.format(gesture),'w') as file:
    for filename in glob.glob('media/identified_gestures/{}/*.jpg'.format(gesture)):

        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(filename)

        # Find all facial features in all the faces in the image
        face_landmarks_list = face_recognition.face_landmarks(image)

        print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

        for face_landmarks in face_landmarks_list:
            file.write("{}".format(gesture))
            for facial_feature in face_landmarks.keys():
                
                if(facial_feature == 'top_lip' or facial_feature == 'bottom_lip'):
                        
                    for points in face_landmarks[facial_feature]:
                        file.write(",{},{}".format(points[0], points[1]))
            
            file.write("\n")
