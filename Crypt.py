from cryptography.fernet import Fernet

logger = Log.initialize('Crypt')

class Crypt:
    @classmethod
    def loadKeyFile(cls):
        logger.debug("Start loading the key file")
        returnCode = "OK"
        try:
            handle = open("keyfile","r")
            returnCode = handle.read().strip()
            handle.close()
        except Exception as err:
            logger.critical("Key File not found")
            returnCode = "KO"

        logger.debug("End loading the key file")
        return returnCode

    def decrypt(self, encodedString, key):
        logger.debug("Start password decryption")
        decodedString = ""
        cipher_suite = Fernet(key)
        try:
            decodedString = cipher_suite.decrypt(encodedString.encode('utf-8')).decode()
        except Exception as err:
            logger.error("Error while decrypting value")

        logger.debug("End password decryption")
        return decodedString
