# import torch
# from torchvision import models, transforms
# from PIL import Image
# import json

# MODEL_PATH = "models/image_model/model.pth"
# LABELS_PATH = "models/image_model/labels.json"

# with open(LABELS_PATH) as f:
#     LABELS = json.load(f)

# model = models.resnet50()
# model.fc = torch.nn.Linear(model.fc.in_features, len(LABELS))
# model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
# model.eval()

# transform = transforms.Compose([
#     transforms.Resize((224, 224)),
#     transforms.ToTensor()
# ])

# def classify_image(image_path: str) -> dict:
#     """
#     Classifies image into a product/content category
#     """
#     image = Image.open(image_path).convert("RGB")
#     image = transform(image).unsqueeze(0)

#     with torch.no_grad():
#         outputs = model(image)

#     probs = torch.softmax(outputs, dim=1)
#     confidence, label_id = torch.max(probs, dim=1)

#     return {
#         "type": "image",
#         "domain": LABELS[str(label_id.item())],
#         "confidence": round(confidence.item(), 3)
#     }

def classify_image(image_path: str) -> dict:
    # Mock image prediction
    return {
        "type": "image",
        "domain": "Automobile",
        "confidence": 0.88
    }
