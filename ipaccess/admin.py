
from django.contrib import admin


from .models import BlockIPAddress


@admin.register(BlockIPAddress)
class BlockIPAdmin(admin.ModelAdmin):
	list_display = ( '__str__', 'reason_for_block','is_enabled')