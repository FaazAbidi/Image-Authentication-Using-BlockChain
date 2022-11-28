import requests
import base64
import cv2 as cv
import numpy as np
import hashlib
import imagehash
from PIL import Image

from base.models import Block

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


def image_hashes(image_data):
        
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


def get_similar_blocks(all_blocks, subject_block):
    
    similar_blocks = [] 
    
    for block in all_blocks:
        
        average_hash_simm_percent = (1-(hamming_distance(block.average_hash, subject_block.average_hash) / len(subject_block.average_hash))) * 100
        dhash_simm_percent = (1-(hamming_distance(block.dhash, subject_block.dhash) / len(subject_block.dhash))) * 100
        phash_simm_percent = (1-(hamming_distance(block.phash, subject_block.phash) / len(subject_block.phash))) * 100
        whash_simm_percent = (1-(hamming_distance(block.whash, subject_block.whash) / len(subject_block.whash))) * 100
        colorhash_simm_percent = (1-(hamming_distance(block.colorhash, subject_block.colorhash) / len(subject_block.colorhash))) * 100
        
        cummulative = round(((average_hash_simm_percent+phash_simm_percent+dhash_simm_percent+whash_simm_percent+colorhash_simm_percent)/500)*100, 2)
        
        similarities_percent = {
            "average_hash" : round(average_hash_simm_percent, 2),
            "phash" : round(phash_simm_percent, 2),
            "dhash" : round(dhash_simm_percent, 2),
            "whash" : round(whash_simm_percent, 2),
            "colorhash" : round(colorhash_simm_percent, 2),
            'cummulative' : cummulative
        }
        
        similar_blocks.append((block, similarities_percent,))
        
    similar_blocks.sort(key=lambda x: x[1]["cummulative"], reverse=True)
    
    print(similar_blocks)
    return similar_blocks
        
        
        
        
