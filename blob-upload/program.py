import sys
import time

from azure.storage.blob import BlobServiceClient


def upload(path, container_name, connection_string):
    # Generate the file name and print it
    if '.' in path:
        extension = path.split('.')[-1]
        extension = f'.{extension}'
    else:
        extension = ''
    name = f'{int(time.time() * 1000)}{extension}'
    print(name)
    # Instantiate a new BlobServiceClient using a connection string
    client = BlobServiceClient.from_connection_string(connection_string)
    # Instantiate a new ContainerClient
    container_client = client.get_container_client(container_name)
    # Instantiate a new BlobClient
    blob_client = container_client.get_blob_client(name)
    # Upload content to block blob
    with open(path, 'rb') as handle:
        blob_client.upload_blob(handle, blob_type='BlockBlob')


if __name__ == '__main__':
    upload(sys.argv[1], sys.argv[2], sys.argv[3])
