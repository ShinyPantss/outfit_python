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

def remove_background(image_path, net):
    image = Image.open(image_path).convert('RGB')
    original_size = image.size
    image_resized = image.resize((320, 320))

    image_np = np.array(image_resized) / 255.0
    tmpImg = np.zeros((320, 320, 3))
    tmpImg[:,:,0] = image_np[:,:,0]
    tmpImg[:,:,1] = image_np[:,:,1]
    tmpImg[:,:,2] = image_np[:,:,2]
    tmpImg = tmpImg.transpose((2, 0, 1))
    tmpImg = torch.from_numpy(tmpImg).unsqueeze(0).type(torch.FloatTensor)

    with torch.no_grad():
        d1, *_ = net(tmpImg)
        pred = d1[:,0,:,:]
        pred = (pred - pred.min()) / (pred.max() - pred.min())
        mask = pred.squeeze().cpu().numpy() * 255
        mask = cv2.resize(mask.astype(np.uint8), original_size)

    original = np.array(image)
    b, g, r = original[:,:,0], original[:,:,1], original[:,:,2]
    a = mask
    rgba = np.stack([b, g, r, a], axis=2)
    result = Image.fromarray(rgba.astype(np.uint8), mode='RGBA')
    
    return result