import torch
from torchvision import transforms
from PIL import Image
import torchvision.models as models

class_names = ['Alluvial', 'Black', 'Clay', 'Laterite', 'Red', 'Sandy']

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.efficientnet_v2_m(weights=models.EfficientNet_V2_M_Weights.DEFAULT).to(device)
output_shape = len(class_names)
model.classifier = torch.nn.Sequential(
    torch.nn.Dropout(p=0.2, inplace=True),
    torch.nn.Linear(in_features=1280, out_features=output_shape, bias=True)
).to(device)
model.load_state_dict(torch.load("soil_classifier_EfficientNet_V3_M.pth", map_location=device, weights_only=True))
model.eval()

preprocess = models.EfficientNet_V2_M_Weights.DEFAULT.transforms()

def classify_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
        class_idx = predicted.item()
        return class_names[class_idx]
