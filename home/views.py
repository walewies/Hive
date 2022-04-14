from django.shortcuts import render
from django.views.generic import TemplateView
from posts.models import Post

from django.http import JsonResponse

# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

    def post(self, request):
        post_pk = request.POST.get("post_pk")
        user = self.request.user.slug
        current_post = Post.objects.get(pk=int(post_pk))
        current_likes_list = current_post.likes.split(",")

        if user in current_likes_list:
            current_likes_list.remove(user)
            current_likes_string = ""
            if len(current_likes_list) > 0:
                current_likes_string += current_likes_list[0]
                for i in range(1, len(current_likes_list)):
                    current_likes_string += ","
                    current_likes_string += current_likes_list[i]
            current_likes_amount = len(current_likes_list)
            Post.objects.filter(pk=int(post_pk)).update(likes=current_likes_string)
            Post.objects.filter(pk=int(post_pk)).update(likes_amount=current_likes_amount-1)
            return JsonResponse({
                "order": "like",
                "likes_amount":  current_likes_amount - 1 # -1 Accounts for empty string at index 0.
            }, status=200)
        else:
            current_likes_list.append(user)
            current_likes_string = ""
            current_likes_string += current_likes_list[0]
            for i in range(1, len(current_likes_list)):
                current_likes_string += ","
                current_likes_string += current_likes_list[i]
            current_likes_amount = len(current_likes_list)
            Post.objects.filter(pk=int(post_pk)).update(likes=current_likes_string)
            Post.objects.filter(pk=int(post_pk)).update(likes_amount=current_likes_amount-1)
            return JsonResponse({
                "order": "unlike",
                "element": request.POST.get("element"),
                "likes_amount":  current_likes_amount - 1 # -1 Accounts for empty string at index 0.
            }, status=200)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["posts"] = Post.objects.all()
        return context