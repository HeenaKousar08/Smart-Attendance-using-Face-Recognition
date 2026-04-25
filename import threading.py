import threading

import cv2

from deepface import DeepFace


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)



counter = 0

face_match = False


reference_img = cv2.imread("photo.jpg")


def check_face(frame):

    global face_match

    try:

        if DeepFace.verify(frame, reference_img.copy())['verified']:

            face_match = True

        else:

            face_match = False



    except ValueError:

        face_match =False


while True:

    ret, frame = cap.read()


    if ret:

        if counter %30 == 0:

            try:
                jls_extract_var = frame
                threading.Thread(target= check_face, args=(jls_extract_var.cop(),)).start()
            except ValueError:
                pass

        counter +=1


        if face_match:

            cv2.putText(frame, "MATCH!", (20, 250), cv2.FRONT_HERSHEY_SIMPLEX, 2, (0, 255, 0),3)

        else:

            cv2.putText(frame, "NO MATCH!", (20, 250), cv2.FRONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),3)


        cv2.imshow("video", frame)    
        
        pass

    key =cv2.waitKey(1)

    if Key == ord("q"):

        break



cv2.destroyAllWindows()


