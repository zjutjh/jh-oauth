# from Cryptodome.Cipher import AES
# from Cryptodome import Random
from Crypto.Cipher import AES
from Crypto import Random
from binascii import b2a_hex, a2b_hex


class Aes:

    def __init__(self, key: str):
        """
        初始化AES加密器
        :param key: 加密的私钥，该密钥在整个类内是不可变的
        """
        # byteArray 加密的密钥
        self.key = key.encode('utf-8')
        # 加密的模式
        self.mode = AES.MODE_CBC

    def encrypt(self, text: str):
        """
        使用AES算法对数据进行加密
        :param text: 待加密的字符串
        :return: 加密后的字符串，自带公钥
        """
        raw_data: bytes = text.encode('utf-8')
        per_len: int = AES.block_size  # int 每次加密数据的长度
        count: int = len(raw_data)
        if count % per_len != 0:
            add: int = per_len - (count % per_len)
        else:
            add: int = 0
        raw_data = raw_data + (b'0' * add)  # 将数据补齐
        iv: bytes = Random.new().read(AES.block_size)  # 随机生成一个公钥
        cipher: AES = AES.new(self.key, self.mode, iv)  # AES数据加密器

        s_data: bytes = cipher.encrypt(raw_data)
        return b2a_hex(iv + s_data).decode('ascii')

    def decrypt(self, text):
        """
        使用AES解密算法进行解密
        :param text: 待解密的字符串
        :return: 解密后的字符串
        """
        s_data: bytes = a2b_hex(text.encode('ascii'))  # 解密后的数据，前n位为公钥
        per_len: int = AES.block_size
        cipher: AES = AES.new(self.key, self.mode, s_data[:per_len])
        data: bytes = cipher.decrypt(s_data[per_len:])
        data = data.strip(b'0')
        raw_text: str = data.decode('utf-8')
        return raw_text
