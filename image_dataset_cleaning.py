from struct import unpack
import os
from tqdm import tqdm

marker_mapping = {
    0xffd8: "Start of Image",
    0xffe0: "Application Default Header",
    0xffdb: "Quantization Table",
    0xffc0: "Start of Frame",
    0xffc4: "Define Huffman Table",
    0xffda: "Start of Scan",
    0xffd9: "End of Image"
}


class JPEG:
    def __init__(self, image_file):
        with open(image_file, 'rb') as f:
            self.img_data = f.read()
    
    def decode(self):
        data = self.img_data
        while(True):
            marker, = unpack(">H", data[0:2])
            # print(marker_mapping.get(marker))
            if marker == 0xffd8:
                data = data[2:]
            elif marker == 0xffd9:
                return
            elif marker == 0xffda:
                data = data[-2:]
            else:
                lenchunk, = unpack(">H", data[2:4])
                data = data[2+lenchunk:]            
            if len(data)==0:
                raise TypeError("issue reading jpeg file")            


# list all files in directory
folder_path = '/home/haroon/Desktop/bf_dataset/train/not fractured'
image_paths = os.listdir(folder_path)

corrupted_jpegs = []

for img_path in tqdm(image_paths):
  full_image_path = os.path.join(folder_path, img_path)
  image = JPEG(full_image_path) 
  try:
    image.decode()   
  except:
    corrupted_jpegs.append(img_path)
    print(f"Corrupted image: {img_path}")

for imgs in corrupted_jpegs:
    os.remove(os.path.join(folder_path, imgs))

for imgs in image_paths:
    path = os.path.join(folder_path, imgs)
    print(path)
