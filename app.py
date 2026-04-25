from fastapi import FastAPI, UploadFile, File
from PIL import Image
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights

app = FastAPI()

# load model once
weights = ResNet18_Weights.DEFAULT
model = resnet18(weights=weights)
model.eval()

preprocess = weights.transforms()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    input_tensor = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor)

    probs = torch.nn.functional.softmax(outputs[0], dim=0)
    # top_prob, top_catid = torch.topk(probs, 1)
    # label = weights.meta["categories"][top_catid.item()]
    # return {"label": label, "confidence": float(top_prob)}


    top_probs, top_ids = torch.topk(probs, 2)
    results = []
    for prob, idx in zip(top_probs, top_ids):
        results.append({
            "label": weights.meta["categories"][idx.item()],
            "confidence": float(prob)
        })

    return {"predictions": results}


