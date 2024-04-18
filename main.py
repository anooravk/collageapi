# from fastapi import FastAPI
# import random


# app=FastAPI()

# @app.get('/')
# async def root():
#     return {"example":"this is an example api","data":0}



# @app.get('/random')
# async def getRandom():
#     rand:int=random.randint(0,100)
#     return {"random number":rand}



# @app.get('/random/{limit}')
# async def getRandom(limit:int):
#     rand:int=random.randint(0,limit)
#     return {"random number":rand,"limit":limit}


from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image
from io import BytesIO
import numpy as np
from typing import List
import random
import tempfile

app = FastAPI(debug=True)




def generate_collage(images):

    num_images = min(max(len(images), 2), 4)

    if len(images) < 4:
        images = images * (4 // len(images)) + random.sample(images, 4 % len(images))
    
    if num_images == 2:
        image_width = 384  
        image_height = 768 
    else:
        image_width = 384 
        image_height = 384  
    
    pil_images = [Image.open(BytesIO(img)).resize((image_width, image_height)) for img in images]
    
    collage = Image.new('RGB', (768, 768))
    
    offset_x, offset_y = 0, 0
    for idx, img in enumerate(pil_images):
        collage.paste(img, (offset_x, offset_y))
        offset_x += image_width
        if (idx + 1) % 2 == 0:  
            offset_x = 0
            offset_y += image_height
    
    collage_bytes = BytesIO()
    collage.save(collage_bytes, format='PNG')
    collage_bytes.seek(0)
    
    return collage_bytes


@app.post("/create_collage/")
async def create_collage(files: List[bytes] = File(...)):
    collage_bytes = generate_collage(files)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file.write(collage_bytes.getvalue())
        temp_file_path = temp_file.name
  
    return FileResponse(temp_file_path, media_type="image/png")

