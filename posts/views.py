from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, DetailView
from .models import Post, Comment
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from datetime import datetime

from django.http import JsonResponse

from accounts.models import User, Follow
from posts.models import PostLike, CommentLike, SubcommentLike, Save, PostDislike

# Create your views here.
class CreatePost(CreateView):
    model = Post
    fields = ('meme_file', 'description')
    template_name = "CreatePost.html"

    def get_success_url(self):
        return reverse_lazy("accounts:profile", kwargs={"slug": self.request.user.slug})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.datetime_posted = datetime.now()
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

class PostAndCommentsView(TemplateView):
    template_name = "PostView.html"

    def post(self, request, pk):
        post_pk = pk
        user = self.request.user.slug
        current_post = Post.objects.get(pk=post_pk)

        # Like/Unlike post on request.
        if request.POST.get("task") == "like":
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
            if PostLike.objects.filter(post=current_post, user=self.request.user):
                liked_post = PostLike.objects.get(post=current_post, user=self.request.user)
                liked_post.delete()
                order = "like"
            # Like
            else:
                # Check if post has been disliked by user and deletes dislike
                if PostDislike.objects.filter(post=current_post, user=self.request.user):
                    disliked_post = PostDislike.objects.get(post=current_post, user=self.request.user)
                    disliked_post.delete()

                PostLike.objects.create(post=current_post, user=self.request.user)
                order = "unlike"

            update_post = Post.objects.filter(pk=post_pk)
            current_likes_amount = len(PostLike.objects.filter(post=current_post))
            current_dislikes_amount = len(PostDislike.objects.filter(post=current_post))
            update_post.update(likes_amount=current_likes_amount, dislikes_amount=current_dislikes_amount)

            updated_user_interests = ""
            for key in dict_user_interests.keys():
                updated_user_interests += "," + key + "," + str(dict_user_interests[key])
            updated_user_interests = updated_user_interests[1:]

            user_model.update(interests=updated_user_interests)

            return JsonResponse({
                "order": order,
                "likes_amount":  current_likes_amount,
                "dislikes_amount": current_dislikes_amount
            }, status=200)

        # Dislike/Undislike post on request.
        if request.POST.get("task") == "dislike":
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

            # Undislike
            if PostDislike.objects.filter(post=current_post, user=self.request.user):
                dislike_object = PostDislike.objects.get(post=current_post, user=self.request.user)
                dislike_object.delete()
                order = "dislike"
            # Dislike
            else:
                # Check if post has been liked by user and deletes like
                if PostLike.objects.filter(post=current_post, user=self.request.user):
                    like_object = PostLike.objects.get(post=current_post, user=self.request.user)
                    like_object.delete()
                
                PostDislike.objects.create(post=current_post, user=self.request.user)
                order = "undislike"

            update_post = Post.objects.filter(pk=post_pk)
            current_dislikes_amount = len(PostDislike.objects.filter(post=current_post))
            current_likes_amount = len(PostLike.objects.filter(post=current_post))
            update_post.update(dislikes_amount=current_dislikes_amount)

            updated_user_interests = ""
            for key in dict_user_interests.keys():
                updated_user_interests += "," + key + "," + str(dict_user_interests[key])
            updated_user_interests = updated_user_interests[1:]

            user_model.update(interests=updated_user_interests)

            return JsonResponse({
                "order": order,
                "dislikes_amount":  current_dislikes_amount,
                "likes_amount": current_likes_amount
            }, status=200)

        # Like/Unlike comment on request
        elif request.POST.get("task") == "comment_like":
            comment = Comment.objects.get(pk=request.POST.get("comment_pk"))
            comment_model = Comment.objects.filter(pk=request.POST.get("comment_pk"))
            current_user = self.request.user

            # Unlike
            if CommentLike.objects.filter(comment=comment, user=current_user):
                commentlike_obj = CommentLike.objects.get(comment=comment, user=current_user)
                commentlike_obj.delete()
                order = "like"
            # Like
            else:
                CommentLike.objects.create(comment=comment, user=current_user)
                order = "unlike"

            current_likes_amount = len(CommentLike.objects.filter(comment=comment))
            comment_model.update(likes_amount=current_likes_amount)

            return JsonResponse({
                "order": order,
                "likes_amount": current_likes_amount
            }, status=200)


        # Follow/Unfollow Post-User on request.
        elif request.POST.get("task") == "follow":
            post_user = current_post.user
            current_user = self.request.user
            post_user_model = User.objects.filter(slug=current_post.user.slug)
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
                "post_user": current_post.user.slug # To change all posts regarding following.
            }, status=200)

        # Creates a new comment
        elif request.POST.get("task") == "add_comment":
            comment_body = request.POST.get('comment_body')
            post = Post.objects.get(id=pk)
            comment = Comment.objects.create(user=self.request.user, body=comment_body, post=post)
            
            # Changes the amount of comments after a new one has been created
            post.comments_amount = len(Comment.objects.filter(post=post))
            post.save()

            return JsonResponse({
                "comment_body": comment.body, 
                "comment_user": comment.user.username,
                "comment_user_slug": comment.user.slug,
                "comment_pk": comment.pk,
                "comments_amount": post.comments_amount
            }, status=200)
        
        else:
            print("Failed to do anything in post view")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = Post.objects.get(id=self.kwargs['pk']).user
        context["current_user"] = self.request.user
        context["post"] = Post.objects.get(id=self.kwargs['pk'])
        context["comments"] = Comment.objects.filter(post=self.kwargs['pk'])

        # Avoids error when searching for followers, likes, etc. of unauthenticated user.
        if not self.request.user.is_authenticated:
            return context

        # Makes a list of all the Users current user follows.
        following_queryset = Follow.objects.filter(follower=self.request.user)
        context["following"] = []
        for following in following_queryset:
            context["following"].append(following.following)
            
        # Makes a list of all the liked posts of user.
        likes_queryset = PostLike.objects.filter(user=self.request.user)
        context["likes"] = []
        for like in likes_queryset:
            context["likes"].append(like.post)

        # Makes a list of all the disliked posts of user.
        dislikes_queryset = PostDislike.objects.filter(user=self.request.user)
        context["dislikes"] = []
        for dislike in dislikes_queryset:
            context["dislikes"].append(dislike.post)

        # Makes a list of all the saved posts of the current user.
        saves_queryset = Save.objects.filter(user=self.request.user)
        context["saved_posts"] = []
        for save in saves_queryset:
            context["saved_posts"].append(save.post)
        
        # Makes a dictionary stating which comments the current user has liked.
        likes_by_comment = {}
        order = "Like"
        for comment in context["comments"]:
            comment_likes = CommentLike.objects.filter(comment=comment)
            for comment_like in comment_likes:
                if self.request.user == comment_like.user:
                    order = "Unlike"
            likes_by_comment[comment] = order
            order = "Like"
        
        context["likes_by_comment"] = likes_by_comment

        return context
        
    def get_success_url(self, **kwargs):
        return reverse_lazy("posts:view_post", kwargs={"pk": self.kwargs['pk']})