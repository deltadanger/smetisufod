from django.contrib import admin
from mainsite.models import Job, ItemCategory, ItemType, Attribute, Item, AttributeValue, AttributeCondition, Recipe, UpdateHistory, InvalidItem


class StandardAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    # exclude = ("field_name")
    # fields = ("field_name")

class ItemAdmin(StandardAdmin):
    list_filter = ("type", "level", "attributes", "conditions")

class UpdateHistoryAdmin(StandardAdmin):
    filter_horizontal = ("updated_items", "updated_panos")

class InvalidItemAdmin(StandardAdmin):
    list_filter = ("origin", "flag_date")


admin.site.register(Item, ItemAdmin)
admin.site.register(Job, StandardAdmin)
admin.site.register(ItemCategory, StandardAdmin)
admin.site.register(ItemType, StandardAdmin)
admin.site.register(Attribute, StandardAdmin)
admin.site.register(AttributeValue, StandardAdmin)
admin.site.register(AttributeCondition, StandardAdmin)
admin.site.register(Recipe, StandardAdmin)
admin.site.register(UpdateHistory, UpdateHistoryAdmin)
admin.site.register(InvalidItem, StandardAdmin)
