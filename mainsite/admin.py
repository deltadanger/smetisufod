from django.contrib import admin
from mainsite.models import I18nString, Job, ItemCategory, ItemType, Attribute, Item, AttributeValue, AttributeCondition, Recipe


class StandardAdmin(admin.ModelAdmin):
    actions_on_bottom = True
    # exclude = ("field_name")
    # fields = ("field_name")

class I18nStringAdmin(StandardAdmin):
    fields = ("fr_fr",)

class ItemAdmin(StandardAdmin):
    list_filter = ("item_type", "level", "attributes", "craft", "has_valid_recipe", "conditions")




admin.site.register(I18nString, I18nStringAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Job, StandardAdmin)
admin.site.register(ItemCategory, StandardAdmin)
admin.site.register(ItemType, StandardAdmin)
admin.site.register(Attribute, StandardAdmin)
admin.site.register(AttributeValue, StandardAdmin)
admin.site.register(AttributeCondition, StandardAdmin)
admin.site.register(Recipe, StandardAdmin)
