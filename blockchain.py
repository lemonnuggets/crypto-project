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
        return f'{self.r},{self.s}'


class Record:
    def __init__(self, signatory_key, signature, data) -> None:
        self.signatory_key = signatory_key
        self.data = data
        self.signature = signature

    def __str__(self) -> str:
        return f"{self.signatory_key} {self.signature} {self.data}"

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
        sha.update(f'{str(self.index)}{str(self.timestamp)}{str(self.timestamp)}{str(self.data)}{str(self.previous_hash)}{str(self.nonce)}'.encode('utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.hash_block()
            # print(self.hash, self.nonce)

    def __str__(self) -> str:
        return f'Block:\n\tIndex = {self.index},\n\tTimestamp = {self.timestamp},\n\tData = {self.data},\n\tPrevious Hash = {self.previous_hash},\n\tHash = {self.hash},\n\tNonce = {self.nonce}'

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.chain.append(genesis_block)

    def add_block(self, record, signature, public_key):
        if verify(record, signature, public_key):
            previous_hash = self.chain[-1].hash
            block = Block(len(self.chain), time.time(), record, previous_hash)
            self.chain.append(block)
            return {'status': 'success', 'block': block}
        else:
            return {'status': 'failure', 'reason': 'invalid signature'}

    def __str__(self) -> str:
        print_str = ""
        print_str += "Blockchain: \n"
        for block in self.chain:
            print_str += str(block) + "\n"
        return print_str

if __name__ == "__main__":
    blockchain = Blockchain()
    print(blockchain)
    print("Adding blocks...")
    private_key, public_key = dss.userKeys()
    # signatory_private_key, signatory_public_key = dss.userKeys()
    message = "Hello, world!"
    signature = Signature(message, private_key)
    blockchain.add_block(message, signature, public_key)
    # blockchain.add_block("Record 1", "Signature 1", "Public Key 1")
    # blockchain.add_block("Record 2", "Signature 2", "Public Key 2")
    # blockchain.add_block("Record 3", "Signature 3", "Public Key 3")
    print(blockchain)