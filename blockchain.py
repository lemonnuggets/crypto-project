import hashlib
import time
import dss

DIFFICULTY = 4


def verify(record, signature, public_key):
    """
    Verify the signature of a record.
    """
    return dss.verification(record, signature.r, signature.s, public_key)


class Signature:
    def __init__(self, message, private_key):
        self.r, self.s, _ = dss.signature(message, private_key)

    def get_componenents(self):
        return self.r, self.s

    def __str__(self):
        return f"{self.r},{self.s}"


class Record:
    def __init__(self, signatory_key, signature, data) -> None:
        self.signatory_key = signatory_key
        self.data = data
        self.signature = signature

    def __str__(self) -> str:
        return f"{self.signatory_key};{self.signature};{self.data}"

    def verify(self) -> bool:
        return verify(self.data, self.signature, self.signatory_key)


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.hash_block()
        self.mine_block(DIFFICULTY)

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(
            f"{str(self.index)}{str(self.timestamp)}{str(self.timestamp)}{str(self.data)}{str(self.previous_hash)}{str(self.nonce)}".encode(
                "utf-8"
            )
        )
        return sha.hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.hash_block()
            # print(self.hash, self.nonce)

    def __str__(self) -> str:
        return f"Block:\n\tIndex = {self.index},\n\tTimestamp = {self.timestamp},\n\tData = {self.data},\n\tPrevious Hash = {self.previous_hash},\n\tHash = {self.hash},\n\tNonce = {self.nonce}"


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        message = "Genesis Block"
        user = User("USER 0")
        record = Record(user.get_public_key(), user.sign(message), message)
        genesis_block = Block(0, time.time(), record, "0")
        self.chain.append(genesis_block)

    def add_block(self, data, signature, public_key):
        record = Record(public_key, signature, data)
        if record.verify():
            previous_hash = self.chain[-1].hash
            block = Block(len(self.chain), time.time(), record, previous_hash)
            self.chain.append(block)
            return {"status": "success", "block": block}
        else:
            return {"status": "failure", "reason": "invalid signature"}

    def __str__(self) -> str:
        print_str = ""
        print_str += "Blockchain: \n"
        for block in self.chain:
            print_str += str(block) + "\n"
        return print_str


class User:
    def __init__(self, name):
        self.name = name
        self.private_key, self.public_key = dss.userKeys()

    def sign(self, data):
        return Signature(data, self.private_key)

    def get_public_key(self):
        return self.public_key

    def __str__(self) -> str:
        return f"User {self.name}:\n\tPublic Key = {self.public_key},\n\tPrivate Key = {self.private_key}"


if __name__ == "__main__":
    blockchain = Blockchain()

    adam = User("Adam")
    message = "Hello, world!"
    signature = adam.sign(message)
    blockchain.add_block(message, signature, adam.get_public_key())

    preet = User("Preet")
    message = "Hello, world!"
    signature = preet.sign(message)
    blockchain.add_block(message, signature, preet.get_public_key())

    aditya = User("Aditya")
    message = "Hello, world!"
    signature = aditya.sign(message)
    blockchain.add_block(message, signature, aditya.get_public_key())

    ibrahim = User("Ibrahim")
    message = "Hello, world!"
    signature = ibrahim.sign(message)
    blockchain.add_block(message, signature, ibrahim.get_public_key())

    print(adam)
    print(preet)
    print(aditya)
    print(ibrahim)
    print(blockchain)
