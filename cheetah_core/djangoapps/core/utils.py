from django.db import models
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating
    ``created`` and ``modified`` fields.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractUserLoginTest(UserPassesTestMixin):
    """docstring for AbstractUserLoginTest."""

    login_url = reverse_lazy('account_login')
    text_404 = 'Does not exist'

    redirect_field_name = 'next'

    no_permission_url = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_not_logged()

        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_no_permission_url(self, url=None):
        if not url and not self.no_permission_url:
            raise NotImplementedError(
                '{0} no url passed to get_no_permission_url() method and no_permission_url attribute was set.'
                .format(self.__class__.__name__))
        
        return url if url else self.no_permission_url

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        if self.no_permission_url:
            return HttpResponseRedirect(self.get_no_permission_url())
        raise Http404(self.text_404)

    def handle_not_logged(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(),
                                 self.get_login_url(),
                                 self.get_redirect_field_name())


class LoginRequired(LoginRequiredMixin):

    login_url = reverse_lazy('account_login')
    redirect_field_name = 'next'
