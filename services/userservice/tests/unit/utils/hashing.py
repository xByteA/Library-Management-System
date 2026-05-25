from src.utils.cryptography.bcryptAdapter import BcryptAdapter
text= "test-hashing-adapter"
def test_hash(text):

    b= BcryptAdapter()
    hashed= b.hash(text)
    return hashed!= text
print(test_hash())


def test_verify(text):
    b= BcryptAdapter()
    hashed= b.hash(text)
    verify= b.verify(hashed)
    return verify