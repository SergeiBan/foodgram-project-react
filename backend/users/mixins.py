from rest_framework import mixins, viewsets


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class CreateDeleteViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    pass


class IsSubscribed():
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if (
            user.is_authenticated and user != obj
                and hasattr(user, 'authors')):
            return user.authors.filter(author=obj).exists()
        return False
