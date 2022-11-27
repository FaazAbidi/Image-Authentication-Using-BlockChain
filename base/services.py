import requests
import base64
import cv2 as cv
import numpy as np
import hashlib
import imagehash
from PIL import Image

IMAGE_HOSTING_SERVICE_KEY =  "55d947aa16c695bc4e464c91a79f48b6"


def host_image(image_data):
    """Hosts an image on the image hosting service.

    Args:
        image_path (str): Path to the image to host.

    Returns:
        str: The URL of the hosted image.
    """
    with image_data.open("rb") as image_file:
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes)

    data = {
        "key" : IMAGE_HOSTING_SERVICE_KEY,
        "image" : image_base64
    }
    response = requests.post(
        f"https://api.imgbb.com/1/upload",
        data=data,
    )
    
    image_url = response.json()['data']['url']
    
    return image_url


def image_d_hash(image_data):
        
        image_file = image_data.open("rb")
        image_bytes = image_file.read()
        image_base64 = base64.b64encode(image_bytes)
        image_base64 = image_base64.decode('utf-8')
            
        image = cv.imdecode(np.frombuffer(base64.b64decode(image_base64), np.uint8), cv.IMREAD_COLOR)
        image = Image.fromarray(image)
        
        average_hash = str(imagehash.average_hash(image))
        phash =  str(imagehash.phash(image))
        dhash = str(imagehash.dhash(image))
        whash = str(imagehash.whash(image))
        colorhash = str(imagehash.colorhash(image)) 
        
        return {
            "average_hash" : average_hash,
            "phash" : phash,
            "dhash" : dhash,
            "whash" : whash,
            "colorhash" : colorhash
        }
    

def proof_of_work(previous_proof):
    new_proof = 1
    check_proof = False
    
    while check_proof is False:
        hash_operation = hashlib.sha256(
            str(new_proof**2 - previous_proof**2).encode()).hexdigest()
        if hash_operation[:5] == '00000':
            check_proof = True
        else:
            new_proof += 1
            
    return new_proof


def final_hash_generate(prev_hash, d_hash, proof_of_work):
    return hashlib.sha256(str(prev_hash + d_hash + proof_of_work).encode()).hexdigest()


def hamming_distance(hash1, hash2):
    
    if len(hash1) != len(hash2):
        if len(hash1) > len(hash2):
            hash2 = hash2.rjust(len(hash1), '0')
        else:
            hash1 = hash1.rjust(len(hash2), '0')
    
    assert len(hash1) == len(hash2)
    
    i = 0
    count = 0
 
    while(i < len(hash1)):
        if(hash1[i] != hash2[i]):
            count += 1
        i += 1
    return count


def get_similar_images(all_blocks, subject_block):

    for block in all_blocks:
        