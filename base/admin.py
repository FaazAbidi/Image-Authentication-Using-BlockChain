from django.contrib import admin

# Register your models here.

from .models import Block, BlockChain

admin.site.register(Block)
admin.site.register(BlockChain)