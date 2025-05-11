from django.contrib import admin
from .models import (
    TelegramProfile,
    Level, UserProgress,
    TokenWallet, MiningCategory, MiningCard, UserMiningCard,
    Task, UserTask,
    MiniGame, UserMiniGameScore,
    Airdrop, UserAirdropEntry, Character, Skin, Purchase, UserCharater
)

@admin.register(UserCharater)
class UserCharaterAdmin(admin.ModelAdmin):
    list_display = ('character', 'level', 'engry')
    list_filter = ('character', 'level')


admin.site.register(TelegramProfile)
admin.site.register(Level)
admin.site.register(UserProgress)
admin.site.register(TokenWallet)
admin.site.register(MiningCategory)
admin.site.register(MiningCard)
admin.site.register(UserMiningCard)
admin.site.register(Task)
admin.site.register(UserTask)
admin.site.register(MiniGame)
admin.site.register(UserMiniGameScore)
admin.site.register(Airdrop)
admin.site.register(UserAirdropEntry)



@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Skin)
class SkinAdmin(admin.ModelAdmin):
    list_display = ('name', 'character', 'price', 'is_unlocked')
    list_filter = ('character', 'is_unlocked')
    search_fields = ('name',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('skin', 'purchase_date')
    list_filter = ('purchase_date',)