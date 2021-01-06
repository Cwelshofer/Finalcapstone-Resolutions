from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from rest_framework.decorators import action
from rest_framework.fields import NullBooleanField
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from rest_framework import status
from finalcapstoneapi.models import Subscription
from finalcapstoneapi.models import ResolutionUser
from datetime import date


class Subscriptions(ViewSet):

    def list(self, request):

        #localhost:8000/subscriptions?author_id=2

        followings = Subscription.objects.all()

        author_id = self.request.query_params.get('author_id', None)

        if author_id is not None and int(author_id) is not request.auth.user.id :
            followings = followings.filter(author_id=author_id, follower_id=request.auth.user.id)
            followings = followings[len(followings) - 1]
            serializer = SubscriptionSerializer(followings, many=False, context={'request': request})

        elif author_id is not None and int(author_id) is request.auth.user.id:
            followings = followings.filter(author_id=author_id)
            serializer = SubscriptionSerializer(followings, many=True, context={'request': request})

        else:
            serializer = SubscriptionSerializer(followings, many=True, context={'request': request})
        

            
        return Response(serializer.data)


    def create(self, request):
        new_subscription = Subscription()

        user = ResolutionUser.objects.get(user=request.auth.user)
        new_subscription.follower = user

        new_subscription.author = ResolutionUser.objects.get(pk=request.data["author_id"])
        new_subscription.created_on = date.today()

        new_subscription.save()

        serializer = SubscriptionSerializer(new_subscription, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get', 'put'], detail=True)
    def unsubscribe(self, request, pk=None):
        if request.method == 'PUT':

            #define author using pk retrieved from url
            author = ResolutionUser.objects.get(pk=pk)

            #get the subscription object where the author equals the userId (from front end)
            # where follow equals the logged in user
            # and where ended_on === null
            sub = Subscription.objects.get(author=author, follower=request.auth.user.id, ended_on=None)

            #change ended_on to today and save
            sub.ended_on = date.today()
            sub.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)





class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id', 'created_on', 'ended_on', 'author', 'follower')
        # depth = 1