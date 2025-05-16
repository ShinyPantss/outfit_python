from U2Net.model import U2NET
import torch
import numpy as np
from PIL import Image
import cv2

def load_model():
    model_path = './u2net.pth'
    net = U2NET(3,1)
    net.load_state_dict(torch.load(model_path, map_location='cpu'))
    net.eval()
    
    return net

def remove_background(img: Image.Image, net):
    original_size = img.size
    image_resized = img.resize((320, 320))

    arr = np.array(image_resized, dtype=np.float32) / 255.0          # (320,320,3)
    tensor = torch.from_numpy(arr.transpose(2,0,1)).unsqueeze(0).float()   # (1,3,320,320)

    with torch.no_grad():
        d1, *_ = net(tensor)
        pred = d1[:,0,:,:]
        pred = (pred - pred.min()) / (pred.max() - pred.min())
        mask = pred.squeeze().cpu().numpy() * 255
        mask = cv2.resize(mask.astype(np.uint8), original_size)

    original = np.array(img)
    R, G, B = original[:,:,0], original[:,:,1], original[:,:,2]
    rgba = np.stack([R, G, B, mask], axis=2)
    
    result = Image.fromarray(rgba.astype(np.uint8), mode='RGBA')
    
    return result