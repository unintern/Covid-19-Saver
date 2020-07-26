# USAGE
# python3 recognize_faces_image.py --encodings encodings.pickle --image examples/example_01.png 

# import the necessary packages
import face_recognition
import argparse
import pickle
import cv2
from guardian.models import *
from numpy import array
from random import randint
import os
# construct the argument parser and parse the arguments

def recognize_person(args):
	try:
		args["detection_method"]
	except KeyError:
		args["detection_method"]="cnn"

	# try:
	# 	args["encodings"]
	# except KeyError:
	# 	args["encodings"]="encodings.pickle"
		
	# load the input image and convert it from BGR to RGB
	image = cv2.imread(args["image"])
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes corresponding
	# to each face in the input image, then compute the facial embeddings
	# for each face
	print("[INFO] Detecting number of faces...")
	boxes = face_recognition.face_locations(rgb,model=args["detection_method"])
	encodings = face_recognition.face_encodings(rgb, boxes)
	# print(encodings[0])
	person_count=len(encodings)
	if person_count!=1:
		if person_count>1:
			print("More than one faces detected!")
		elif person_count==0:
			print("No face detected!")
		return "unknown"
	print("[INFO] Matching face with the database...")
	

	# data = pickle.loads(open(args["encodings"], "rb").read())
	# initialize the list of names for each face detected

	all_persons = MissingPersonImages.objects.all()
	data= {"encodings":[],"names":[]}
	for person in all_persons:

		data["encodings"].append(eval(person.pickel)[0])
		# data["encodings"].append(person.pickel)
		data["names"].append(person.addhar_card_number.addhar_card_number)
	# for aadhar_num in all_persons:
	# 	all_persons[aadhar_num]=eval()
	# print("all-p",all_persons)
	# loop over the facial embeddings
	# for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
	# print(data)
	match = face_recognition.compare_faces(data["encodings"],encodings[0])
	# print(matches,type(matches))
	name = "Unknown"
	# print(match)
	# check to see if we have found a match
	if True in match:
		# find the indexes of all matched faces then initialize a
		# dictionary to count the total number of times each face
		# was matched
		matchedIdxs = [i for (i, b) in enumerate(match) if b]
		counts = {}

		# loop over the matched indexes and maintain a count for
		# each recognized face face
		for i in matchedIdxs:
			name = data["names"][i]
			counts[name] = counts.get(name, 0) + 1

		# determine the recognized face with the largest number of
		# votes (note: in the event of an unlikely tie Python will
		# select first entry in the dictionary)
		name = max(counts, key=counts.get)
	
	# update the list of names
	print(name)
	
	for ((top, right, bottom, left), name) in zip(boxes, [name]):
		# draw the predicted face name on the image
		cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)

	# show the output image
	# cv2.imwrite("media/tmp")
	img_name=str(randint(0,1000000000))+"recognized_"+args["image"].split("/")[-1]
	img_path="static/tmp/"+img_name
	cv2.imwrite(img_path,image)
	# import pdb;pdb.set_trace()
	# cv2.imshow("Image", image)
	# cv2.waitKey(0)

	return (name,"tmp/"+img_name)

	
	# loop over the recognized faces
if __name__=='__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-e", "--encodings", type=str, default="encodings.pickle" ,help="path to serialized db of facial encodings")
	ap.add_argument("-i", "--image", required=True,help="path to input image")
	ap.add_argument("-d", "--detection-method", type=str, default="cnn",help="face detection model to use: either `hog` or `cnn`")
	args = vars(ap.parse_args())

	# load the known faces and embeddings
	recognize_person(args)
	# print(data)