import cv2

# asks user how many people they would like to capture in the photo
people_count = int(input('How many people will be in the photo?\n'))

# initializes the device's camera to capture video
capture = cv2.VideoCapture(0)

# loop to run the capture until a frame that meets the criteria has been saved
while True:
    frame_captured, frame = capture.read()

    # checks if the frame was captured without any errors
    if frame_captured:
        cv2.imshow('Live video', frame)

        # edits frame for more effective smile recognition
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), cv2.BORDER_DEFAULT)

        # detects the number of smiles using haar cascades
        haar_cascade = cv2.CascadeClassifier('haar_smile.xml')
        smile_count = haar_cascade.detectMultiScale(blur, scaleFactor=1.1, minNeighbors=500)

        # prints the frame with the rectangles detecting the smiles
        for (x, y, w, h) in smile_count:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
        cv2.imshow('Detected faces', frame)

        # captures single image once the smiles have met the people count given as input
        if len(smile_count) >= people_count:
            cv2.waitKey(20)
            cv2.imwrite('xD.jpg', frame)
            break

        if cv2.waitKey(20) & 0xFF == ord('d'):
            break

capture.release()
cv2.destroyAllWindows()
