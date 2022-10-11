from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, DetailView
from .models import Post, Comment
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from datetime import datetime

from django.http import JsonResponse

from accounts.models import User, Follow
from posts.models import PostLike, CommentLike, SubcommentLike, Save

# Create your views here.
class CreatePost(CreateView):
    model = Post
    fields = ('meme_file', 'description')
    template_name = "CreatePost.html"

    def get_success_url(self):
        return reverse_lazy("accounts:profile", kwargs={"slug": self.request.user.slug})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.memer = self.request.user
        obj.datetime_posted = datetime.now()
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

class PostAndCommentsView(TemplateView):
    template_name = "PostView.html"

    def post(self, request, pk):
        user = self.request.user.slug

        # Like/Unlike post on request.
        if request.POST.get("task") == "like":
            post_pk = request.POST.get("post_pk")
            current_post = Post.objects.get(pk=int(post_pk))
            user_model = User.objects.filter(slug=user) # .get() does not allow .update() on object
            list_user_interests = user_model[0].interests.split(",") # [0] because .filter() returns queryset
            if list_user_interests[0] == "":
                list_user_interests.pop(0) # removes initial empty string
            dict_user_interests = {}

            if len(list_user_interests) > 0:
                for i in range(0, len(list_user_interests), 2):
                    dict_user_interests[list_user_interests[i].lower()] = int(list_user_interests[i+1])

            current_post_description = current_post.description.split(",")
            order = ""

            # Unlike
            if PostLike.objects.filter(post=current_post, memer=self.request.user):
                liked_post = PostLike.objects.get(post=current_post, memer=self.request.user)
                liked_post.delete()
                order = "like"
            # Like
            else:
                PostLike.objects.create(post=current_post, memer=self.request.user)
                order = "unlike"

            update_post = Post.objects.filter(pk=post_pk)
            current_likes_amount = len(PostLike.objects.filter(post=current_post))
            update_post.update(likes_amount=current_likes_amount)

            updated_user_interests = ""
            for key in dict_user_interests.keys():
                updated_user_interests += "," + key + "," + str(dict_user_interests[key])
            updated_user_interests = updated_user_interests[1:]

            user_model.update(interests=updated_user_interests)

            return JsonResponse({
                "order": order,
                "likes_amount":  current_likes_amount
            }, status=200)

        # Like/Unlike comment on request
        elif request.POST.get("task") == "comment_like":
            comment = Comment.objects.get(pk=request.POST.get("comment_pk"))
            comment_model = Comment.objects.filter(pk=request.POST.get("comment_pk"))
            current_user = self.request.user

            # Unlike
            if CommentLike.objects.filter(comment=comment, memer=current_user):
                commentlike_obj = CommentLike.objects.get(comment=comment, memer=current_user)
                commentlike_obj.delete()
                order = "like"
            # Like
            else:
                CommentLike.objects.create(comment=comment, memer=current_user)
                order = "unlike"

            current_likes_amount = len(CommentLike.objects.filter(comment=comment))
            comment_model.update(likes_amount=current_likes_amount)

            return JsonResponse({
                "order": order,
                "likes_amount": current_likes_amount
            }, status=200)


        # Follow/Unfollow Post-User on request.
        elif request.POST.get("task") == "follow":
            post_user = current_post.memer
            current_user = self.request.user
            post_user_model = User.objects.filter(slug=current_post.memer.slug)
            current_user_model = User.objects.filter(slug=self.request.user.slug)

            # Unfollow
            if Follow.objects.filter(follower=current_user, following=post_user):
                followship = Follow.objects.get(follower=current_user, following=post_user)
                followship.delete()
                order = "follow"

            # Follow
            else:
                Follow.objects.create(follower=current_user, following=post_user)
                order = "unfollow"

            post_user_followers = len(Follow.objects.filter(following=post_user))
            current_user_following =  len(Follow.objects.filter(follower=current_user))

            post_user_model.update(followers_amount=post_user_followers)
            current_user_model.update(following_amount=current_user_following)

            return JsonResponse({
                "order": order,
                "post_user": current_post.memer.slug # To change all posts regarding following.
            }, status=200)

        else:
            comment_body = request.POST.get('comment_body')
            comment = Comment.objects.create(memer=self.request.user, body=comment_body, post=Post.objects.get(id=pk))

            return JsonResponse({
                "comment_body": comment.body, 
                "comment_memer": comment.memer.username,
                "comment_memer_slug": comment.memer.slug
            }, status=200)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = Post.objects.get(id=self.kwargs['pk']).memer
        context["current_user"] = self.request.user
        context["post"] = Post.objects.get(id=self.kwargs['pk'])
        context["comments"] = Comment.objects.filter(post=self.kwargs['pk'])

        # Makes a list of all the Users current user follows.
        following_queryset = Follow.objects.filter(follower=self.request.user)
        context["following"] = []
        for following in following_queryset:
            context["following"].append(following.following)
            
        # Makes a list of all the liked posts of user.
        likes_queryset = PostLike.objects.filter(memer=self.request.user)
        context["likes"] = []
        for like in likes_queryset:
            context["likes"].append(like.post)

        # Makes a list of all the saved posts of the current user.
        saves_queryset = Save.objects.filter(memer=self.request.user)
        context["saved_posts"] = []
        for save in saves_queryset:
            context["saved_posts"].append(save.post)
        
        # Makes a dictionary stating which comments the current user has liked.
        likes_by_comment = {}
        order = "Like"
        for comment in context["comments"]:
            comment_likes = CommentLike.objects.filter(comment=comment)
            for comment_like in comment_likes:
                if self.request.user == comment_like.memer:
                    order = "Unlike"
            likes_by_comment[comment] = order
            order = "Like"
        
        context["likes_by_comment"] = likes_by_comment

        return context
        
    def get_success_url(self, **kwargs):
        return reverse_lazy("posts:view_post", kwargs={"pk": self.kwargs['pk']})