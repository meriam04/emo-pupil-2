import cv2
from pathlib import Path

def crop(image_path: Path, output_dir: Path):
    img = cv2.imread(str(image_path))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    face = face_classifier.detectMultiScale(gray_img, 1.1, 5, minSize=(100, 100))

    if len(face) > 0:
        x, y, w, h = face[0]
        #cv2.rectangle(gray_img, (x, y), (x + w, y + h), (0, 255, 0), 4)
        cropped_img = gray_img[y:y+h, x:x+w]

        output_image_path = image_path.stem + "_c" + image_path.suffix
        cv2.imwrite(str(output_dir / output_image_path), cropped_img)
