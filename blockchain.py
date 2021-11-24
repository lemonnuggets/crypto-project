import hashlib
import time
import dss
import pickle
import os
import json

DIFFICULTY = 4
MAX_BLOCK_SIZE = 2
MAX_CHUNK_SIZE = 2


def verify(message, signature, public_key):
    """
    Verify the signature of a record.
    """
    # print("Verifying", message, json.dumps(message), signature, public_key)
    return dss.verification(message, signature.r, signature.s, public_key)


class Signature:
    def __init__(self, data, private_key):
        # print("Signing the data...")
        # print(json.dumps(data))
        # print(private_key)
        self.r, self.s, _ = dss.signature(data, private_key)
        # print("Signature is: ", self)

    def get_components(self):
        return self.r, self.s

    def __str__(self):
        return f"{self.r},{self.s}"


class Record:
    def __init__(self, signatory_key, signature, data) -> None:
        self.signatory_key = signatory_key
        self.data = data
        self.signature = signature

    def __str__(self) -> str:
        return f"{self.signatory_key};{self.signature};{json.dumps(self.data)}"

    def verify(self) -> bool:
        return verify(self.data, self.signature, self.signatory_key)


class User:
    def __init__(self, name, public_key=None, private_key=None):
        self.name = name
        if public_key is None or private_key is None:
            self.private_key, self.public_key = dss.userKeys()

    def sign(self, data):
        return Signature(data, self.private_key)

    def get_public_key(self):
        return self.public_key

    def __str__(self) -> str:
        return f"User {self.name}:\n\tPublic Key = {self.public_key},\n\tPrivate Key = {self.private_key}"


class Block:
    def __init__(self, index, timestamp, previous_hash, records=[]):
        self.index = index
        self.timestamp = timestamp
        self.records = records
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.hash_block()
        self.mine_block(DIFFICULTY)

    def add_record(self, record):
        if not record.verify():
            return {
                "status": "error",
                "message": "Record is not valid",
                "error_code": "1",
            }
        elif len(self.records) >= MAX_BLOCK_SIZE:
            return {"status": "error", "message": "Block is full", "error_code": "2"}
        else:
            self.records.append(record)
            self.hash = self.hash_block()
            return {"status": "success", "message": "Record added", "error_code": "0"}

    def record_to_string(self):
        result = ""
        for record in self.records:
            result += str(record)
        return result

    def hash_block(self):
        # print(str(self.index))
        # print(str(self.timestamp))
        # print(str(self.previous_hash))
        # print(str(self.nonce))
        # print(self.record_to_string())
        sha = hashlib.sha256()
        sha.update(
            f"{str(self.index)}{str(self.timestamp)}{str(self.timestamp)}{self.record_to_string()}{str(self.previous_hash)}{str(self.nonce)}".encode(
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
        return "Block:\n\tIndex = {0},\n\tTimestamp = {1},\n\tRecords: {2},\n\tPrevious Hash = {3},\n\tHash = {4},\n\tNonce = {5}".format(
            self.index,
            self.timestamp,
            self.record_to_string(),
            self.previous_hash,
            self.hash,
            self.nonce,
        )


class Blockchain:
    def __init__(self, prev_hash=None):
        self.chain = []
        if prev_hash is None:
            self.create_genesis_block()
        self.initial_hash = prev_hash

    def create_genesis_block(self):
        message = "Genesis Block"
        user = User("USER 0")
        record = Record(user.get_public_key(), user.sign(message), message)
        genesis_block = Block(0, time.time(), "0", [record])
        self.chain.append(genesis_block)

    def add_record(self, data, signature, public_key):
        record = Record(public_key, signature, data)
        if len(self.chain) == 0:
            prev_hash = self.initial_hash
        else:
            prev_hash = self.chain[-1].hash
            current_block = self.chain[-1]

        if len(self.chain) == 0 or len(current_block.records) >= MAX_BLOCK_SIZE:
            current_block = Block(len(self.chain), time.time(), prev_hash)
            self.chain.append(current_block)

        response = current_block.add_record(record)
        return response

    def __str__(self) -> str:
        print_str = ""
        print_str += "Blockchain: \n"
        for block in self.chain:
            print_str += str(block) + "\n"
        return print_str


class BlockchainDB:
    def __init__(self, dir_path) -> None:
        self.chunk_no = 0
        self.users = set()
        self.dir_path = dir_path
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        self.load_last_chunk()

    def get_chunk_path(self, chunk_no):
        return self.dir_path + "/" + str(chunk_no) + ".pickle"

    def load_last_chunk(self):
        self.chunk_no = len(os.listdir(self.dir_path))
        while (
            not os.path.exists(self.get_chunk_path(self.chunk_no))
            and self.chunk_no >= 0
        ):
            self.chunk_no -= 1
        if self.chunk_no < 0:
            self.chunk_no = 0
            self.blockchain = Blockchain()
            return
        print(f"loading chunk {self.chunk_no}")
        self.blockchain = pickle.load(open(self.get_chunk_path(self.chunk_no), "rb"))
        print(self.blockchain)

    def save_last_chunk(self):
        pickle.dump(self.blockchain, open(self.get_chunk_path(self.chunk_no), "wb"))

    def start_next_chunk(self):
        self.save_last_chunk()
        self.chunk_no += 1
        self.users.clear()
        self.blockchain = Blockchain(self.blockchain.chain[-1].hash)

    def add_to_blockchain(self, record):
        if len(self.blockchain.chain) >= MAX_CHUNK_SIZE:
            self.start_next_chunk()
        return self.blockchain.add_record(
            record.data, record.signature, record.signatory_key
        )

    def add_record(self, signature, public_key, data):
        possible_actions = ("create user", "delete user", "diagnose")
        if len(self.blockchain.chain) >= MAX_CHUNK_SIZE:
            self.start_next_chunk()
        if "action" not in data:
            return {
                "status": "error",
                "message": "No action specified",
                "error_code": "7",
            }
        action = data["action"]
        if action not in possible_actions:
            return {
                "status": "error",
                "message": "Action is not valid",
                "error_code": "3",
            }
        if action == "create user":
            if "name" not in data:
                return {
                    "status": "error",
                    "message": "Name is not provided",
                    "error_code": "4",
                }
            if "public key" not in data:
                return {
                    "status": "error",
                    "message": "Public key is not provided",
                    "error_code": "5",
                }
        if action == "delete user":
            if "public key" not in data:
                return {
                    "status": "error",
                    "message": "Public key is not provided",
                    "error_code": "5",
                }
        if action == "diagnose":
            if "public key" not in data:
                return {
                    "status": "error",
                    "message": "Public key is not provided",
                    "error_code": "5",
                }
            if "diagnosis" not in data:
                return {
                    "status": "error",
                    "message": "Diagnosis is not provided",
                    "error_code": "6",
                }
        record = Record(public_key, signature, json.dumps(data))
        # print(record)
        response = self.add_to_blockchain(record)
        if response["status"] == "error":
            return response
        self.save_last_chunk()
        return response


if __name__ == "__main__":
    # blockchain = Blockchain()

    # adam = User("Adam")
    # message = "Hello, world!"
    # signature = adam.sign(message)
    # blockchain.add_record(message, signature, adam.get_public_key())

    # preet = User("Preet")
    # message = "Hello, world!"
    # signature = preet.sign(message)
    # blockchain.add_block(message, signature, preet.get_public_key())

    # aditya = User("Aditya")
    # message = "Hello, world!"
    # signature = aditya.sign(message)
    # blockchain.add_block(message, signature, aditya.get_public_key())

    # ibrahim = User("Ibrahim")
    # message = "Hello, world!"
    # signature = ibrahim.sign(message)
    # blockchain.add_block(message, signature, ibrahim.get_public_key())

    # print(adam)
    # print(preet)
    # print(aditya)
    # print(ibrahim)
    # print(blockchain)
    # user = User("USER 0")
    # print(user)
    # message = "Hello, world!"
    # print(verify(message, user.sign(message), user.get_public_key()))
    db = BlockchainDB("blockchain")
    adam = User("Adam")
    data = {
        "name": adam.name,
        "public key": adam.get_public_key(),
        "designation": "doctor",
        "action": "create user",
    }
    response = db.add_record(adam.sign(json.dumps(data)), adam.get_public_key(), data)
    print(adam)
    print(data)
    print(response)

    preet = User("Preet")
    data = {
        "name": preet.name,
        "public key": preet.get_public_key(),
        "designation": "patient",
        "action": "create user",
    }
    response = db.add_record(adam.sign(json.dumps(data)), adam.get_public_key(), data)
    print(preet)
    print(data)
    print(response)

    data = {
        "public key": preet.get_public_key(),
        "action": "diagnose",
        "diagnosis": "cold",
    }
    response = db.add_record(adam.sign(json.dumps(data)), adam.get_public_key(), data)
    print(data)
    print(response)
