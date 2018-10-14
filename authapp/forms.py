from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms.utils import ErrorList
from django.forms import ValidationError, HiddenInput, FileInput

from authapp.models import ShopUser


class ErrList(ErrorList):
    def __str__(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join([
            '<div class="alert alert-warning alert-dismissible fade show" role="alert">\
            %s\
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
            <span aria-hidden="true">&times;</span>\
            </button>\
            </div>' % err for err in self])


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(ShopUserLoginForm, self).__init__(error_class = ErrList, *args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegistrationForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super(ShopUserRegistrationForm, self).__init__(error_class = ErrList, *args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'avatar':
                continue
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        if self.cleaned_data['age'] < 18:
            raise ValidationError('Вы слишком молоды для этого.')
        return self.cleaned_data['age']


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super(ShopUserEditForm, self).__init__(error_class = ErrList, *args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'avatar':
                field.label = 'Изменить фото'
                field.widget = FileInput()
            elif field_name == 'password':
                self.fields.pop(field_name)
            else:
                field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        if self.cleaned_data['age'] < 18:
            raise ValidationError('Вы слишком молоды для этого.')
        return self.cleaned_data['age']