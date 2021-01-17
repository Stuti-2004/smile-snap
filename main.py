import cv2 as cv

capture = cv.VideoCapture(0)

while True:
    isTrue, frame = capture.read()

    cv.imshow('Live Video', frame)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (7,7), cv.BORDER_DEFAULT)

    haar_cascade = cv.CascadeClassifier('haar_smile.xml')

    faces_rect = haar_cascade.detectMultiScale(blur, scaleFactor=1.1, minNeighbors=500)

    print(f'Number of faces found = {len(faces_rect)}')

    for (x, y, w, h) in faces_rect:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

    cv.imshow('Detected Faces', frame)

    if cv.waitKey(20) & 0xFF == ord('d'):
        break

capture.release()
cv.destroyAllWindows()
