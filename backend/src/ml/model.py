import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 8, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(8 * 8 * 8, 32)
        self.fc2 = nn.Linear(32, 2)

    def forward(self, x):
        out = F.max_pool2d(torch.tanh(self.conv1(x)), 2)
        out = F.max_pool2d(torch.tanh(self.conv2(out)), 2)
        out = out.view(-1, 8 * 8 * 8)
        out = torch.tanh(self.fc1(out))
        out = self.fc2(out)
        return out

# model = Net()
# model.load_state_dict(torch.load("FreshnessDetector.pt", map_location='cuda'))
# model.eval()

# transform = transforms.Compose([
#     transforms.Resize((32, 32)),
#     transforms.ToTensor(),
#     transforms.Normalize((0.7369, 0.6360, 0.5318),
#                          (0.3281, 0.3417, 0.3704))
# ])

# classes = ['Normal', 'Podre']

# img_path = 'fruta podre.jpeg'
# img = Image.open(img_path).convert('RGB')
# img_tensor = transform(img).unsqueeze(0) 

# with torch.no_grad():
#     output = model(img_tensor)
#     prob = F.softmax(output, dim=1)
#     pred = torch.argmax(prob, dim=1)

# print(f"Classe: {classes[pred.item()]} ({prob[0][pred.item()]*100:.2f}%)")
