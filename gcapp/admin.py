from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(GiftCard)
# admin.site.register(UserBuy)
admin.site.register(UserSellImage)
    

class UserSellorBuyAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_action', 'giftCardType', 'gift_card_name', 'amount', 'date')

    def get_action(self, obj):
        if obj.trans_type == "Bought":
            return "Paid"
        else:
            return "Sold"
    get_action.short_description = 'Action'

admin.site.register(UserSellorBuy, UserSellorBuyAdmin)
    
