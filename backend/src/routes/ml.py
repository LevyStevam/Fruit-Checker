from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import io
import os

# Importar a classe Net do modelo
from src.ml.model import Net

router = APIRouter()

# Carregar modelo e transform apenas uma vez
model_path = os.path.join(os.path.dirname(__file__), '../ml/FreshnessDetector.pt')
model = Net()
model.load_state_dict(torch.load(model_path, map_location='cuda'))
model.eval()

transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize((0.7369, 0.6360, 0.5318),
                         (0.3281, 0.3417, 0.3704))
])

classes = ['Normal', 'Podre']

@router.post('/classify-fruit')
async def classify_fruit(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail='O arquivo enviado não é uma imagem.')
    try:
        image_bytes = await file.read()
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        img_tensor = transform(img).unsqueeze(0)
        with torch.no_grad():
            output = model(img_tensor)
            prob = F.softmax(output, dim=1)
            pred = torch.argmax(prob, dim=1)
        result = {
            'classe': classes[pred.item()],
            'probabilidade': float(prob[0][pred.item()])
        }
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Erro ao classificar a imagem: {str(e)}') 