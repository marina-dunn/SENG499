import face_recognition
import sys

filename = sys.argv[1]

# Load the jpg file into a numpy array
image = face_recognition.load_image_file(filename)

# Find all facial features in all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(image)

print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

with open('poc_data.csv','w') as file:
    for face_landmarks in face_landmarks_list:
        # Print the location of each facial feature in this image
        for facial_feature in face_landmarks.keys():
            file.write("1,{}".format(facial_feature))
            
            ref_x = face_landmarks[facial_feature][0][0]
            ref_y = face_landmarks[facial_feature][0][1]
            for points in face_landmarks[facial_feature]:
                file.write(",{}:{}".format(ref_x-points[0],ref_y-points[1]))
            
            file.write("\n")
