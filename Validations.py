import re


class Validations:

    @staticmethod
    def validate_lat(lat):
        if -90 <= lat <= 90:
            return True
        raise ValueError("This is not a valid latitude")


    @staticmethod
    def validate_long(long):
        if -180 <= long <= 180:
            return True
        raise ValueError("This is not a valid longitude")

    @staticmethod
    def validate_email(email):
        valid = re.search("[^@]+@[^@]+\.[^@]+", email)
        if valid is None:
            raise ValueError("This is not a valid email address")
        return True
