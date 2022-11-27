import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import BlockForm, Block, BlockChain
from django.db.models import Q
from . services import hamming_distance, host_image, image_d_hash, proof_of_work, final_hash_generate

# Create your views here.

def home(request):
    
    all_blocks = Block.objects.all()
    block_count = len(all_blocks)
    
    context = {
        "images" : all_blocks,
        "image_count" : block_count
    }
    
    return render(request, 'home.html', context)


def authenticateImage(request):
  
    if request.method == 'POST':
        form = BlockForm(request.POST, request.FILES)
    
        if form.is_valid():    
            try:
                last_block_id = BlockChain.objects.all()[0].block_id.id
                last_block = Block.objects.get(id=last_block_id)
                last_block_hash = last_block.current_hash
                last_block_proof = last_block.proof
            except:
                last_block_hash = '0'
                last_block_proof = 1
            
        
            img_name = form.cleaned_data['image_name']
            img_desc = form.cleaned_data['image_description']
            img_url = form.files['image_url']            
            current_hashes = image_d_hash(img_url)
            current_proof = proof_of_work(last_block_proof)
            
            final_hash = final_hash_generate(str(last_block_hash), str(current_hashes['dhash']), str(current_proof))
            # hosting image
            image_url = host_image(img_url)
            
            new_block = Block(
                previous_hash = last_block_hash,
                current_hash = final_hash,
                proof = current_proof,
                image_name = img_name,
                image_description = img_desc,
                image_url = image_url,
                dhash = current_hashes['dhash'],
                average_hash = current_hashes['average_hash'],
                phash = current_hashes['phash'],
                whash = current_hashes['whash'],
                colorhash = current_hashes['colorhash']
            )
            
            new_block.save()
            
            # print(new_block.id)
            return redirect('results/'+str(new_block.id))
    else:
        form = BlockForm()
        
    return render(request, 'upload_image.html', {'form' : form})

def upload_success(request):
    return HttpResponse('successfully authenticated')


def image_page(request, pk):
    block = Block.objects.get(id=pk)
    context = {
        'block' : block 
    }
    
    return render(request, 'image_page.html', context)


def get_similar_results(request, pk):
    block = Block.objects.get(id=pk)
    d_hash = block.dhash
    
    all_images = Block.objects.all().filter(~Q(id=pk))
    final = []
            
    context = {
        'block' : block,
        'similar_blocks' : final,
    }
    
    return render(request, 'similar_image.html', context)