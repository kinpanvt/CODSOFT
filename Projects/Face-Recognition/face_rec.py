import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torchvision import transforms
from PIL import Image
import os

# Initialize MTCNN and InceptionResnetV1
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(keep_all=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Transformation for face images
transform = transforms.Compose([
    transforms.Resize((160, 160)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# Load and preprocess images from the folder to create a database of embeddings
def load_face_database(path='Face-Recognition/images'):
    database = {}
    for filename in os.listdir(path):
        if filename.lower().endswith(('jpg', 'png', 'jpeg')):
            name = os.path.splitext(filename)[0]
            img = Image.open(os.path.join(path, filename))
            img_cropped = mtcnn(img)
            if img_cropped is not None:
                if img_cropped.ndim == 4:
                    img_cropped = img_cropped[0]
                embedding = resnet(img_cropped.unsqueeze(0).to(device))
                database[name] = embedding.detach().cpu()[0]
    return database

# Compare face embedding to the database and find the closest match
def recognize_face(embedding, database, threshold=0.8):
    min_dist = float('inf')
    name = "Unknown Person"
    embedding = embedding.to('cpu')
    for db_name, db_embedding in database.items():
        dist = torch.nn.functional.pairwise_distance(embedding, db_embedding.unsqueeze(0)).min().item()
        if dist < min_dist:
            min_dist, name = dist, db_name
    if min_dist > threshold:
        return "Unknown Person", min_dist
    return name, min_dist

database = load_face_database()

def main():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), 2)

            face = frame[y:y+h, x:x+w]
            face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face_pil = Image.fromarray(face_rgb)
            face_tensor = transform(face_pil).unsqueeze(0).to(device)
            embedding = resnet(face_tensor)
            name, distance = recognize_face(embedding, database)
            match_percentage = max(0, 100 - distance * 100)

            cv2.putText(frame, f"{name}: {match_percentage:.2f}%", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        cv2.imshow('Face Detection and Recognition', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
