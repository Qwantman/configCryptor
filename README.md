# ConfigCryptor
Fernet-encrypted config realization. Key'll be stored in .fernetKey file

Lib has just two simple methods:
- getValue(key)
- setValue(key, value)

To initialize main class use: 
```
import configcryptor

cnf = configcryptor.Config("conf.json")
```

You can add values by you own. If you add plaintext value, set "encrypted" to false. 
Lib'll encrypt and replace data on first start.

# Config.json example where dbPort was added unencrypted
```
{
  "dbHost": {
    "encrypted": true,
    "value": "<some encrypted data>"
  },
  "dbPort": { 
    "encrypted": false,
    "value": "12345"
  }
}
```
