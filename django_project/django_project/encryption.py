import base64
import boto3
from django_project import settings
from cryptography.fernet import Fernet


NUM_BYTES_FOR_LEN = 4

def create_data_key(cmk_id, key_spec="AES_256"):
    """Generate a data key to use when encrypting and decrypting data"""

    # Create data key
    kms_client = boto3.client("kms",region_name = "us-west-1",aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = kms_client.generate_data_key(KeyId=cmk_id, KeySpec=key_spec)

    # Return the encrypted and plaintext data key
    return response["CiphertextBlob"], base64.b64encode(response["Plaintext"])

def create_cmk(description="My Customer Master Key"):
    """Creates a KMS Customer Master Key

    Description is used to differentiate between CMKs.
    """

    kms_client = boto3.client("kms",region_name = "us-west-1",aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = kms_client.create_key(Description=description)

    # Return the key ID and ARN
    return response["KeyMetadata"]["KeyId"], response["KeyMetadata"]["Arn"]
def retrieve_cmk(description):
    """Retrieve an existing KMS CMK based on its description"""
    # Retrieve a list of existing CMKs
    # If more than 100 keys exist, retrieve and process them in batches
    
    kms_client = boto3.client("kms",region_name = "us-west-1",aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = kms_client.list_keys()

    for cmk in response["Keys"]:
        key_info = kms_client.describe_key(KeyId=cmk["KeyArn"])
        if key_info["KeyMetadata"]["Description"] == description:
            return cmk["KeyId"], cmk["KeyArn"]

    # No matching CMK found
    return None, None

def encrypt_file(file, cmk_id):
    """Encrypt JSON data using an AWS KMS CMK"""

    filename = file.name
    # Replace with desired directory for now. Should be dynamic. 
    with open("C:/Users/rober_y/Desktop/{}".format(filename), "rb") as file:
      file_contents = file.read()

    data_key_encrypted, data_key_plaintext = create_data_key(cmk_id)
    if data_key_encrypted is None:
        return

    # Encrypt the data
    f = Fernet(data_key_plaintext)
    file_contents_encrypted = f.encrypt(file_contents)

    # Write the encrypted data key and encrypted file contents together
    with open(filename + '.encrypted', 'wb') as file_encrypted:
        file_encrypted.write(len(data_key_encrypted).to_bytes(NUM_BYTES_FOR_LEN,
                                                              byteorder='big'))
        file_encrypted.write(data_key_encrypted)
        file_encrypted.write(file_contents_encrypted)
        

def decrypt_data_key(data_key_encrypted):
    """Decrypt an encrypted data key"""

    # Decrypt the data key
    kms_client = boto3.client("kms",region_name = "us-west-1",aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
              aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    response = kms_client.decrypt(CiphertextBlob=data_key_encrypted)

    # Return plaintext base64-encoded binary data key
    return base64.b64encode((response["Plaintext"]))

def decrypt_file(filename):
    """Decrypt a file encrypted by encrypt_file()"""

    # Read the encrypted file into memory
    with open(filename + ".encrypted", "rb") as file:
      file_contents = file.read()

    # The first NUM_BYTES_FOR_LEN tells us the length of the encrypted data key
    # Bytes after that represent the encrypted file data
    data_key_encrypted_len = int.from_bytes(file_contents[:NUM_BYTES_FOR_LEN],
                                            byteorder="big") \
                             + NUM_BYTES_FOR_LEN
    data_key_encrypted = file_contents[NUM_BYTES_FOR_LEN:data_key_encrypted_len]

    # Decrypt the data key before using it
    data_key_plaintext = decrypt_data_key(data_key_encrypted)
    if data_key_plaintext is None:
        return False

    # Decrypt the rest of the file
    f = Fernet(data_key_plaintext)
    file_contents_decrypted = f.decrypt(file_contents[data_key_encrypted_len:])

    # Write the decrypted file contents
    with open(filename + '.decrypted', 'wb') as file_decrypted:
      file_decrypted.write(file_contents_decrypted)