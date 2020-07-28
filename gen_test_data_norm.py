import face_recognition
import sys
from PIL import Image
import glob
import time 

gesture = sys.argv[1]
label = 0

start = time.time()

if(gesture == 'smile'): label = 0
elif(gesture == 'neutral'): label = 1
elif(gesture == 'frown'): label = 2

with open('./datasets/{}_low_res_gestures.csv'.format(gesture),'w') as file:
    for filename in glob.glob('media/low_res_gestures/{}/*'.format(gesture)):

        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(filename)

        # Find all facial features in all the faces in the image
        face_landmarks_list = face_recognition.face_landmarks(image)

        print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

        for face_landmarks in face_landmarks_list:
            file.write("{}".format(label))
            
            cluster_x = []
            cluster_y = []
            
            for facial_feature in face_landmarks.keys():
                if(facial_feature == 'top_lip' or facial_feature == 'bottom_lip'):
                        
                    for points in face_landmarks[facial_feature]:
                        cluster_x.append(points[0])
                        cluster_y.append(points[1])
            
            min_x = cluster_x[0]
            max_x = cluster_x[0]
            for x in cluster_x:
                if(max_x < x): max_x = x
                elif(min_x > x): min_x = x
                
            min_y = cluster_y[0]
            max_y = cluster_y[0]    
            for y in cluster_y:
                if(max_y < y): max_y = y
                elif(min_y > y): min_y = y
            
            for x,y in zip(cluster_x, cluster_y):
                file.write(",{},{}".format( ((x-min_x) / (max_x-min_x)) , ((y-min_y) / (max_y - min_y))))
            
            file.write("\n")
            
end = time.time()
print(end - start)
