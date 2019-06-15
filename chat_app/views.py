from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_list_or_404
from django.views import View
from django.contrib.auth import authenticate, logout
from django.db.models import Q


from chat_app.models import Message, ChatRoom  # Chat,

import random
import string


def id_generator(l):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(l))


class IndexView(View):
    def get(self, request, page):
        if self.request.user.is_authenticated:
            users = list(User.objects.all())
            chatroom1 = list(ChatRoom.objects.filter(user1=self.request.user))
            chatroom2 = list(ChatRoom.objects.filter(user2=self.request.user))

            users1, users2, users3 = [], [], []

            for user in users:
                skip = False
                if user == self.request.user:
                    continue
                for chatroom in chatroom1:
                    if user == chatroom.user2:
                        users1.append(user)
                        skip = True
                        break
                for chatroom in chatroom2:
                    if user == chatroom.user1:
                        users2.append(user)
                        skip = True
                        break
                if not skip:
                    users3.append(user)

            return render(request, 'index.html', {'users': users,
                                                  'chatroom1': chatroom1,
                                                  'chatroom2': chatroom2,
                                                  'users1': users1,
                                                  'users2': users2,
                                                  'users3': users3})
        else:
            return render(request, 'index.html')


class SignUpView(View):
    def get(self, request):
        return render(request,
                      'registration.html')

    def post(self, request):
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(username=request.POST['name'],
                                            email=request.POST['email'],
                                            password=request.POST['password1'])
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration.html', {'error': 'Passwords are not equal'})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(username=request.POST['name'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'username or password incorrect'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'index.html')


class ChatView(View):
    def get(self, request, pk):
        user_sender = self.request.user
        if len(str(pk)) == 10:
            chatroom = list(ChatRoom.objects.filter(chat_id=pk))
            messages = list(Message.objects.filter(chatroom=chatroom[0].id))
            return render(request, 'chat.html', {'chatroom': chatroom[0],
                                                 'messages': messages,
                                                 'user_sender': user_sender})
        else:
            chatroom = list(ChatRoom.objects.filter(user1=self.request.user, user2=User.objects.get(pk=pk)))
            if chatroom:
                messages = list(Message.objects.filter(chatroom=chatroom[0].id))
                return render(request, 'chat.html', {'chatroom': chatroom[0],
                                                     'messages': messages,
                                                     'user_sender': user_sender})

            chatroom = list(ChatRoom.objects.filter(user1=User.objects.get(pk=pk), user2=self.request.user))
            if chatroom:
                messages = list(Message.objects.filter(chatroom=chatroom[0].id))
                return render(request, 'chat.html', {'chatroom': chatroom[0],
                                                     'messages': messages,
                                                     'user_sender': user_sender})

            chatroom = ChatRoom.objects.create(chat_id=id_generator(10),
                                               user1=self.request.user,
                                               user2=User.objects.get(pk=pk))
            # user_sender.chat = chatroom
            # User.objects.get(pk=pk).chat = chatroom
            return render(request, 'chat.html', {'chatroom': chatroom, 'messages': None, 'user_sender': user_sender})

    def post(self, request, pk):
        user_sender = self.request.user
        if len(str(pk)) == 10:
            chatroom = list(ChatRoom.objects.filter(chat_id=pk))
        else:
            chatroom = list(ChatRoom.objects.filter(user1=User.objects.get(pk=pk), user2=user_sender))
            if chatroom:
                pass
            else:
                chatroom = list(ChatRoom.objects.filter(user1=user_sender, user2=User.objects.get(pk=pk)))

        message = Message.objects.create(user_sender=user_sender, text=request.POST['text'], chatroom=chatroom[0])
        # message.chatroom.set(chatroom)
        messages = list(Message.objects.filter(chatroom=chatroom[0].id))
        return render(request, 'chat.html', {'chatroom': chatroom, 'messages': messages, 'user_sender': user_sender})
