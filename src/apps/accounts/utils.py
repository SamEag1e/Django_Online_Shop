from shared.messages import get_res_obj


# ---------------------------------------------------------------------
def phone_number_validate(phone_number):
    if not phone_number:
        return get_res_obj(False, "phone_not_given")

    if not (
        phone_number.startswith("0")
        and phone_number[1:].isdigit()
        and 10 <= len(phone_number) <= 15
    ):
        return get_res_obj(False, "phone_invalid")

    return get_res_obj(True, "phone_valid")
