from django.contrib import admin
from .models import User, Auction, Bid, Comment, Category
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("auctions",)

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
