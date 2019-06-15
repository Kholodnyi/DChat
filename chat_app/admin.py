from django.contrib import admin

from chat_app.models import Message, ChatRoom  # Chat,


# @admin.register(Chat)
# class ChatAdmin(admin.ModelAdmin):
#     pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(ChatRoom)
class ChatRooAdmin(admin.ModelAdmin):
    pass
