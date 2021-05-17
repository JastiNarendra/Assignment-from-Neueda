from cryptography.fernet import Fernet
import logging
import os


class Decrypter:
    """
    This is a Deryption handler.
    It will load a symmetric key for each object and allow decryption based on the loaded key.
    """
    def __init__(self, path_to_key):
        """
        Constructor for Decrypter object
        :param path_to_key: Provide the path to the symmetric key
        """
        self.__decryption_keypath = path_to_key
        self.__load_decryption_key()
        self.__fernet_obj = Fernet(self.__decryption_key)

    def __load_decryption_key(self):
        """
        Loads symmetric key from provided path to the Decrypter object.
        :return: None
        """
        if os.path.isfile(self.__decryption_keypath):
            key = open(self.__decryption_keypath, "r")
            self.__decryption_key = str.encode(key.read().rstrip('\n'))
        else:
            logging.error("Decryption key is not available in {}.".format(self.__decryption_keypath))
            self.__decryption_key = Fernet.generate_key()
            logging.error("Autogenerated key {} will be used.".format(self.__decryption_key))

    def decrypt_file(self, file_to_decrypt, output_file):
        """
        Decrypts a given file using the loaded key.
        :param file_to_decrypt: File to decrypt.
        :param output_file: Path to decrypted file.
        :return: None
        """
        with open(file_to_decrypt, "rb") as fileobj:
            file_data = fileobj.read()
        decrypted_data = self.__fernet_obj.decrypt(file_data)
        with open(output_file, "wb") as fileobj:
            fileobj.write(decrypted_data)

    def decrypt(self, data_to_decrypt, output_file):
        """
        Decrypts a chunk of data and write to a file.
        :param data_to_decrypt: Chunk of data to decrypt.
        :param output_file: path to decrypted file.
        :return: None
        """
        decrypted_data = self.__fernet_obj.decrypt(data_to_decrypt)
        with open(output_file, "wb") as fileobj:
            fileobj.write(decrypted_data)
