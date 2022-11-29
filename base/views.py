import os
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.http import HttpResponse
from . models import BlockForm, Block, BlockChain
from django.db.models import Q
from . services import get_similar_blocks, host_image, image_hashes, proof_of_work, final_hash_generate

# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def home(request):
    
    all_blocks = Block.objects.all().order_by('-timestamp')
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
            current_hashes = image_hashes(img_url)
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
            return redirect('similarity', pk = new_block.id)
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
    
    all_blocks = Block.objects.all().filter(~Q(id=pk))
    final = get_similar_blocks(all_blocks, block)
    
    context = {
        'block' : block,
        'similar_blocks' : final,
    }
    
    return render(request, 'similar_image.html', context)


def chain(request):
    
    all_blocks = all_blocks = Block.objects.all().order_by('-timestamp')
    
    context = {
        "all_blocks" : all_blocks
    }
    
    return render(request, 'chain.html', context)


def search(request): 
    # get id search
    print(request.GET)
    if request.method == 'GET':
        query = request.GET.get('q') if request.GET.get('q') != None else ''
        type = int(request.GET.get('type')) if request.GET.get('type') != None else -1

    
    

    
    # type 0 is keyword search
    if type == 0:
        all_blocks = Block.objects.all().filter(Q(image_name__icontains=query) | Q(image_description__icontains=query))
    # type 1 is dhash search
    elif type == 1:
        all_blocks = Block.objects.all().filter(Q(dhash__icontains=query))
    #type 2 is average_hash search
    elif type == 2:
        all_blocks = Block.objects.all().filter(Q(average_hash__icontains=query))
    # type 3 is phash search
    elif type == 3:
        all_blocks = Block.objects.all().filter(Q(phash__icontains=query))
    # type 4 is whash
    elif type == 4:
        all_blocks = Block.objects.all().filter(Q(whash__icontains=query))
    # type 5 is colorhash
    elif type == 5:
        all_blocks = Block.objects.all().filter(Q(whash__icontains=query))    
    else:
        all_blocks = []
        
    print(type, query)
    print(all_blocks)
    
    context = {
            "query" : query,
            "result_count" : len(all_blocks),
            "all_blocks" : all_blocks
        }
    
    return render(request, 'searchpage.html', context)
    