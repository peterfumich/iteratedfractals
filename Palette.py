from PIL import Image
import os
import numpy as np
def get_palette(frame_index,scaling = 512,palette_folder='test'):
    pictures = os.listdir(f'palettes/{palette_folder}')
    palette = []
    for picture in pictures:
        extension = picture.split('.')[-1].upper()
        if extension=='PNG' or extension=='JPG' or extension=='JPEG':
            img = Image.open(f'palettes/{palette_folder}/{picture}')
            img = img.resize((scaling, scaling), Image.ANTIALIAS)
            horizontal = -int(scaling/2)
            vertical = -int(scaling/2)
            #img = img.transform(img.size,Image.AFFINE,(1,0,horizontal,0,1,vertical))
            #img = img.crop((-(frame_index+1)%2*horizontal,-(frame_index+1)%2*vertical,-(frame_index+1)%2*horizontal+128,-(frame_index+1)%2*vertical+128))#-((frame_index+1)%2+1)*horizontal,-((frame_index+1)%2+1)*vertical))
            if frame_index==1:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif frame_index==2:
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            elif frame_index==3:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
                img = img.transpose(Image.FLIP_TOP_BOTTOM)
            imag_array = np.array(img)
            d1,d2,d3 = imag_array.shape
            flat_imag = imag_array.flatten().reshape((d1*d2,d3))
            palette.append(flat_imag)
    return(palette)
