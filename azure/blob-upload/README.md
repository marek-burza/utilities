# Usage of the scripts

There are two scripts `container.create.sh` and `container.destroy.sh`. The first one creates Azure resources the second destroys them.
Both scripts require one parameter which specifies the prefix to be used in resource names.

    ./container.create.sh example
    ./container.destroy.sh example

The first script will print a connection string for the storage account.

    ...
    {
      "connectionString": "DefaultEndpointsProtocol=https;EndpointSuffix=core.windows.net;AccountName=examplestorageaccount;AccountKey=cY1aa1/GIBW5jlIJ7oaKxC9CrXuYInuaosUM7r+mC6tp+Pms2O52RW8KE4l+Wj3xQb9WBkUjgTk1t8f0NKI69g=="
    }


# Usage of the application

To use the application to upload a file into Azure Blob Storage run:

    docker run --rm --name azure-upload-blob -v [FILE PATH ON HOST]:[FILE PATH IN CONTAINER] -it azure-blob-upload [FILE PATH IN CONTAINER] [AZURE STORAGE CONTAINER NAME] [AZURE STORAGE ACCOUNT CONECTION STRING]

The application will print one line with the name of the blob, for example:

    1439256846789.jpg

The file can be then accessed under a following URL schema:

    https://[AZURE STORAGE ACCOUNT NAME].blob.core.windows.net/[AZURE STORAGE CONTAINER NAME]/[BLOB NAME]

Assuming the example listed earlier, it would be:

    https://examplestorageaccount.blob.core.windows.net/examplecontainer/1439256846789.jpg
