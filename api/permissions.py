from rest_framework.permissions import IsAuthenticated


class IsSeller(IsAuthenticated):
    def has_permission(self, request, view):
        return super(IsSeller, self).has_permission(request, view) and request.user.role.name == 'seller'


class IsBuyer(IsAuthenticated):
    def has_permission(self, request, view):
        return super(IsBuyer, self).has_permission(request, view) and request.user.role.name == 'buyer'
