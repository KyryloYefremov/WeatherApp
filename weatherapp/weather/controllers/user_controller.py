

class UserController:

    def __init__(self, user_file_path):
        self.__user_file_path = user_file_path

    def sign_in(self, form_email, password):
        try:
            with open(self.__user_file_path, 'r') as file:
                for line in file:
                    credentials = line.rstrip().split(',')
                    email, pwd = credentials[0], credentials[1]
                    if email == form_email and pwd == password:
                        return True
        except Exception:
            return False
        return False

    def sign_up(self, email, password, card_number, cvv, expiration_date):
        """
        Register a new user.
        :param email: Email address.
        :param password: Password.
        :param card_number: Credit card number 16 digits.
        :param cvv: CVV code 3 digits.
        :param expiration_date: Expiration date MM/YY.
        :return: True if the user was registered successfully, False otherwise.
        """

        # Check if the user is already registered
        if self.sign_in(email, password):
            return False

        try:
            # Validate input
            if len(card_number) != 16 or len(cvv) != 3 or len(expiration_date) != 5:
                return False
            with open(self.__user_file_path, 'a') as file:
                file.write(f"{email},{password},{card_number},{cvv},{expiration_date}\n")
            return True
        except Exception as e:
            print(e)
            return False
