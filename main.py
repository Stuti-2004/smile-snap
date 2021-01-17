import cv2


# Checks if an input meets a set of criteria; returns validated input
def validate_input(prompt="Enter a valid input: ", type_=None, range_=None, min_=None, max_=None):
    if range_ is not None and not range_:
        raise ValueError("argument for 'range_' is an empty sequence")
    if min_ is not None and max_ is not None and min_ > max_:
        raise ValueError("argument for 'min_' is greater than argument for 'max_'")
    while True:
        input_ = input(prompt)
        if type_ is not None:
            try:
                input_ = type_(input_)
            except ValueError:
                print(f"Input type must be {type_.__name__}.")
                continue
        if range_ is not None and input_ not in range_:
            if isinstance(range_, range):
                print(f"Input must be between {range_.start} and {range_.stop - 1}.")
            else:
                elements = [str(element) for element in range_]
                if len(range_) < 3:
                    selection = " or ".join(elements)
                else:
                    elements[-1] = " ".join(("or", elements[-1]))
                    selection = ", ".join(elements)
                print(f"Input must be {selection}.")
        elif min_ is not None and input_ < min_:
            print(f"Input must be greater than or equal to {min_}.")
        elif max_ is not None and input_ > max_:
            print(f"Input must be less than or equal to {max_}.")
        else:
            return input_


# Asks user how many people they would like to capture in the photo
people_count = validate_input("How many people will be in the photo? ", int, min_=1)
show_rectangles = validate_input("Would you like to show the rectangles in the photo (y/n)? ", str.lower,
                                 range_=["y", "n", "yes", "no"])
print("Press 'd' to exit capture.")

# Initializes the device's camera to capture video
capture = cv2.VideoCapture(0)

# Runs the capture until a frame that meets the criteria has been saved
while True:
    frame_captured, frame = capture.read()

    # Checks if the frame was captured without any errors
    if frame_captured:

        # Edits frame for more effective smile recognition
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), cv2.BORDER_DEFAULT)
        edited_frame = cv2.dilate(blur, (7, 7), iterations=3)

        # Detects the number of smiles using haar cascades
        haar_cascade = cv2.CascadeClassifier("haar_smile.xml")
        smile_count = haar_cascade.detectMultiScale(edited_frame, scaleFactor=1.1, minNeighbors=350)

        # Prints the frame with or without the rectangles detecting the smiles
        if show_rectangles.startswith("y"):
            for (x, y, w, h) in smile_count:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)
        cv2.imshow("Live video", frame)

        # Captures single image once the smiles have met the people count given as input
        if len(smile_count) >= people_count:
            cv2.waitKey(20)
            cv2.imwrite("xD.jpg", frame)
            break

        if cv2.waitKey(20) & 0xFF == ord("d"):
            break

capture.release()
cv2.destroyAllWindows()
