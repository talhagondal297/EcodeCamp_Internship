from django.contrib import admin
from .models import QuesModel

class QuesModelAdmin(admin.ModelAdmin):
    # Fields to be displayed in the admin form
    fields = ('question', 'op1', 'op2', 'op3', 'op4', 'ans')
    
    # Fields to be displayed in the list view
    list_display = ('question',)
    
    # Optional: Add a search box to filter the list view by specific fields
    search_fields = ('question', 'op1', 'op2', 'op3', 'op4')
    
    # Optional: Add filters to the right side of the list view
    list_filter = ('question',)  # Can be used to filter questions by their answers
    
    # Optional: Specify the default ordering of items in the list view
    ordering = ('-id',)  # Orders by `id` in descending order

admin.site.register(QuesModel, QuesModelAdmin)
