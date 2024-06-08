from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import ValidationError


class UserPasswordMismatchError(ValidationError):
    status_code = 400
    default_code = '1001'
    default_detail = _('Password fields didnt match')


class UserIncorrectError(ValidationError):
    status_code = 400
    default_code = '1002'
    default_detail = _('Incorrect Credentials')


class UserOldPasswordError(ValidationError):
    status_code = 400
    default_code = '1003'
    default_detail = _('Old password is not correct')


class UserAvatarSizeError(ValidationError):
    status_code = 400
    default_code = '1004'
    default_detail = _('Maximum image size 2 MB')


class OrderUpdateError(ValidationError):
    status_code = 400
    default_code = '2001'
    default_detail = _('Not available')


class OrderPaymentError(ValidationError):
    status_code = 400
    default_code = '2002'
    default_detail = _('There was an error during payment')


class OrderAvailabilityError(ValidationError):
    status_code = 400
    default_code = '2003'
    default_detail = _('There is no required quantity of products')


class OrderProductNotFoundError(ValidationError):
    status_code = 400
    default_code = '2004'
    default_detail = _('This product was not found')


class BasketProductNotFoundError(ValidationError):
    status_code = 400
    default_code = '3001'
    default_detail = _('This product was not found')


class BasketAddProductError(ValidationError):
    status_code = 400
    default_code = '3002'
    default_detail = _('Error adding item to cart')


class BasketNotEnoughError(ValidationError):
    status_code = 400
    default_code = '3003'
    default_detail = _('There is no required quantity')


class BasketUpdatingProductError(ValidationError):
    status_code = 400
    default_code = '3004'
    default_detail = _('Error when updating a product in the cart')
