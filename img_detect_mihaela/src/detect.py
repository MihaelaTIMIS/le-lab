# from PIL import Image
# import face_recognition

# image = face_recognition.load_image_file("biden.jpg")

# face_locations = face_recognition.face_locations(image)

# print("I found {} face(s) in this photograph.".format(len(face_locations)))

# for face_location in face_locations:
#     top, right, bottom, left = face_location
#     print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

#     face_image = image[top:bottom, left:right]
#     pil_image = Image.fromarray(face_image)
#     pil_image.show()

# import numpy as np
# import cv2

# cap = cv2.VideoCapture(0)
 
# while(True):
#     ret, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
#     cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



# import face_recognition

# # Load the jpg files into numpy arrays
# biden_image = face_recognition.load_image_file("biden.jpg")
# obama_image = face_recognition.load_image_file("obama.jpg")
# unknown_image = face_recognition.load_image_file("obama2.jpg")


# # Get the face encodings for each face in each image file
# # Since there could be more than one face in each image, it returns a list of encodings.
# # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
# try:
#     biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
#     obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
#     unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
# except IndexError:
#     print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
#     quit()

# known_faces = [
#     biden_face_encoding,
#     obama_face_encoding
# ]

# # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
# results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

# print("Is the unknown face a picture of Biden? {}".format(results[0]))
# print("Is the unknown face a picture of Obama? {}".format(results[1]))
# print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))






# import face_recognition
# import cv2
# import numpy as np

# # This is a super simple (but slow) example of running face recognition on live video from your webcam.
# # There's a second example that's a little more complicated but runs faster.

# # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# # Get a reference to webcam #0 (the default one)
# video_capture = cv2.VideoCapture(0)

# # Load a sample picture and learn how to recognize it.
# obama_image = face_recognition.load_image_file("obama.jpg")
# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# miha_image=face_recognition.load_image_file("miha.jpg")
# miha_face_encoding= face_recognition.face_encodings(miha_image)[0]

# # Load a second sample picture and learn how to recognize it.
# biden_image = face_recognition.load_image_file("biden.jpg")
# biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# # Create arrays of known face encodings and their names
# known_face_encodings = [
#     miha_face_encoding,
#     obama_face_encoding,
#     biden_face_encoding
# ]
# known_face_names = [
#     "Mihaela TIMIS",
#     "Barack Obama",
#     "Joe Biden"
# ]

# while True:
#     # Grab a single frame of video
#     ret, frame = video_capture.read()

#     # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#     rgb_frame = frame[:, :, ::-1]

#     # Find all the faces and face enqcodings in the frame of video
#     face_locations = face_recognition.face_locations(rgb_frame)
#     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#     # Loop through each face in this frame of video
#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#         # See if the face is a match for the known face(s)
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

#         name = "Unknown"

#         # If a match was found in known_face_encodings, just use the first one.
#         # if True in matches:
#         #     first_match_index = matches.index(True)
#         #     name = known_face_names[first_match_index]

#         # Or instead, use the known face with the smallest distance to the new face
#         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#         best_match_index = np.argmin(face_distances)
#         if matches[best_match_index]:
#             name = known_face_names[best_match_index]

#         # Draw a box around the face
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#         # Draw a label with a name below the face
#         cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

#     # Display the resulting image
#     cv2.imshow('Video', frame)

#     # Hit 'q' on the keyboard to quit!
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release handle to the webcam
# video_capture.release()
# cv2.destroyAllWindows()



try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from pytesseract import Output
import cv2
simage = r'./saveimage/buletin.jpg'
# image_original = cv2.imread(simage)
img = cv2.imread(simage)
d = pytesseract.image_to_data(img, output_type=Output.DICT)
NbBoites = len(d['level'])
print ("Nombre de boites: " + str(NbBoites))
print(pytesseract.image_to_string(img, lang='fra'))
# plt.imshow(image_original,'gray')

for i in range(NbBoites):
    # Récupère les coordonnées de chaque boite
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    # Affiche un rectangle
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow('img', img)
cv2.waitKey(0)

cv2.destroyAllWindows()
