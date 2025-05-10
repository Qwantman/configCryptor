import os.path, json, cryptography.fernet

class Config:

    def __init__(self, configPath: bytes|str, key = None, autoFlush = True):

        # Default lib config
        self.__fernetSession = cryptography.fernet.Fernet
        self.__configPath = configPath
        self.__autoFlush = autoFlush
        self.__newKey = False
        self.__encryptedConfig = {}
        self.__decryptedConfig = {}

        if not os.path.exists(self.__configPath): open(self.__configPath, "w+").write("{}")

        # Key logic
        if key is None:
            if not os.path.exists('.fernetKey'): self.__fernetKey, self.__newKey = self.__fernetSession.generate_key(), True
            else: self.__fernetKey = open('.fernetKey', 'r').read().encode()
        else: self.__fernetKey = key.encode('uft-8') if type(self.__configPath) is str else key

        if self.__newKey: open('.fernetKey', "w+").write(self.__fernetKey.decode())

        # New fernet session
        self.__fernetSession = self.__fernetSession(self.__fernetKey)

        self.__loadConfig()

    def __fernetEncrypt(self, data: str|int) -> str:
        if type(data) is int: data = str(data)

        return self.__fernetSession.encrypt(data.encode()).decode()

    def __fernetDecrypt(self, data: str) -> str:

        return self.__fernetSession.decrypt(data.encode()).decode()

    def __fetchConfig(self):

        for _ in self.__encryptedConfig.keys():
            if self.__encryptedConfig[_]['encrypted']: continue

            value = self.__encryptedConfig[_]['value']
            self.__encryptedConfig[_]['value'] = self.__fernetEncrypt(value)
            self.__encryptedConfig[_]['encrypted'] = True

    def __loadConfig(self):

        if not os.path.exists(self.__configPath): raise FileExistsError('Config file not found')

        with open(self.__configPath, "r") as configFileHandle:
            self.__encryptedConfig = json.load(configFileHandle)
            self.__fetchConfig()
            configFileHandle.close()

        self.__writeConfig()

        for _ in self.__encryptedConfig.keys():
            self.__decryptedConfig[_] = self.__fernetDecrypt(self.__encryptedConfig[_]['value'])

    def __writeConfig(self):

        if not os.path.exists(self.__configPath): raise FileExistsError('Config file not found')

        with open(self.__configPath, "w+") as configFileHandler:
            json.dump(self.__encryptedConfig, configFileHandler, indent = 2)
            configFileHandler.close()


    def getValue(self, key): return self.__decryptedConfig.get(key)

    def setValue(self, key, value):

        self.__decryptedConfig[key] = value

        self.__encryptedConfig[key] = {
            "encrypted": True,
            "value": self.__fernetEncrypt(value)
        }

        if self.__autoFlush: self.__writeConfig()
