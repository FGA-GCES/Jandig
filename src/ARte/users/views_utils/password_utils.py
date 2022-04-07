from ARte.users.services.encrypt_service import EncryptService
from ARte.users.views import build_message_and_send_to_user


def validate_username_or_email(recover_password_form, user_service):
    username_or_email = recover_password_form.cleaned_data.get('username_or_email')
    return user_service.check_if_username_or_email_exist(username_or_email), username_or_email

def build_global_vars(user_service, username_or_email):
    global_recovering_email = user_service.get_user_email(username_or_email)

    encrypt_service = EncryptService()
    global_verification_code = encrypt_service.generate_verification_code(global_recovering_email)

    build_message_and_send_to_user(global_recovering_email)

    return global_recovering_email, global_verification_code