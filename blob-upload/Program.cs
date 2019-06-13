using System;
using System.IO;
using Microsoft.Azure.Storage;
using Microsoft.Azure.Storage.Blob;

namespace AzureBlobUpload
{
    public class Program
    {
        public static void Main(string[] args)
        {
            Upload(args[0], args[1], args[2]);
        }

        private static void Upload(string path, string containerName, string connectionString)
        {
            // Generate the file name and print it
            DateTime epoch = new DateTime(1970, 1, 1);
            DateTime now = DateTime.Now;
            TimeSpan span = now - epoch;
            string extension;
            if (path.LastIndexOf(".") == -1)
            {
                extension = "";
            }
            else
            {
                extension = path.Substring(path.LastIndexOf("."));
            }
            string name = ((ulong)span.TotalMilliseconds).ToString() + extension;
            Console.WriteLine(name);

            // Check whether the connection string can be parsed
            CloudStorageAccount storageAccount;
            if (CloudStorageAccount.TryParse(connectionString, out storageAccount))
            {
                // Create the blob storage client
                CloudBlobClient client = storageAccount.CreateCloudBlobClient();

                // Get the reference to the blob container
                CloudBlobContainer container = client.GetContainerReference(containerName);

                // Get the reference to the block blob from the container and upload the file
                container.GetBlockBlobReference(name).UploadFromFile(path);
            }
            else
            {
                // Let the user know that they need to provide a valid connection string
                Console.WriteLine("Failed to parse the connection string!");
            }
        }
    }
}
