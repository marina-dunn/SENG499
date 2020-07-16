import face_recognition
import sys
from PIL import Image
import glob

gesture = sys.argv[1]

with open('{}.csv'.format(gesture),'w') as file:
    face_num = 0;
    for filename in glob.glob('media/identified_gestures/{}/*.jpg'.format(gesture)):

        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(filename)

        # Find all facial features in all the faces in the image
        face_landmarks_list = face_recognition.face_landmarks(image)

        print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

        for face_landmarks in face_landmarks_list:
            face_num += 1
            
            for facial_feature in face_landmarks.keys():
                if(facial_feature != 'chin' and facial_feature != 'nose_bridge' and facial_feature != 'nose_tip'):
                    file.write("{},{}".format(face_num,facial_feature))
                    
                    norm_x = []
                    norm_y = []
                    
                    max_x = face_landmarks[facial_feature][0][0]
                    min_x = max_x
                    max_y = face_landmarks[facial_feature][0][1]
                    min_y = max_y
                    
                    for points in face_landmarks[facial_feature]:
                        if(max_x < points[0]): max_x = points[0]
                        elif(min_x > points[0]): min_x = points[0]
                        
                        if(max_y < points[1]): max_y = points[1]
                        elif(min_y > points[1]): min_y = points[1]
                        
                    for points in face_landmarks[facial_feature]:
                        file.write(",{},{}".format( (points[0]-min_x)/(max_x-min_x), (points[1]-min_y)/(max_y-min_y)))
            
                    file.write("\n")
