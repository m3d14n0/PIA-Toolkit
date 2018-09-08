from django.core.exceptions import PermissionDenied

#superuser decorator
def superuser_only(function):
    """
    Limit view to superusers only.

    Usage:
    --------------------------------------------------------------------------
    @superuser_only
    def my_view(request):
        ...
    --------------------------------------------------------------------------

    or in urls:

    --------------------------------------------------------------------------
    urlpatterns = patterns('',
        (r'^foobar/(.*)', is_staff(my_view)),
    )
    --------------------------------------------------------------------------
    """

    def _inner(request, *args, **kwargs):
        if not request.user.is_admin:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner

def staff_only(function):
    """
    Limit view to staff users only.

    Usage:
    --------------------------------------------------------------------------
    @staff_only
    def my_view(request):
        ...
    --------------------------------------------------------------------------

    or in urls:

    --------------------------------------------------------------------------
    urlpatterns = patterns('',
        (r'^foobar/(.*)', is_staff(my_view)),
    )
    --------------------------------------------------------------------------
    """

    def _inner(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return function(request, *args, **kwargs)
    return _inner

def active_only(function):
    """
    Limit view to superusers only.

    Usage:
    --------------------------------------------------------------------------
    @superuser_only
    def my_view(request):
        ...
    --------------------------------------------------------------------------

    or in urls:

    --------------------------------------------------------------------------
    urlpatterns = patterns('',
        (r'^foobar/(.*)', is_staff(my_view)),
    )
    --------------------------------------------------------------------------
    """
    def _inner(request, *args, **kwargs):
        if not request.user.is_active:
            raise PermissionDenied
            return HttpResponseRedirect('login')
        return function(request, *args, **kwargs)
    return _inner