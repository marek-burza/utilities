# Kubernetes: AKS with Authenticated App Service Ingress

Scripts in this repository implement a template for provisioning a password protected App Service which proxies (via VNet Integration) to a pod running on Azure Kubernetes Service serving static frontend (without anonymous cluster access) kept on a Files Share (and volume mounted using key kept in Kubernetes secrets vault).

![Architecture](architecture.png)

After running the create script the app will be available at:

    https://[PREFIX]app.azurewebsites.net/index.html


# Extras

## Sources & Materials

* [Network concepts for applications in Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/concepts-network)
* [Create an ingress controller in Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/ingress-basic)
* [Integrate your app with an Azure Virtual Network](https://docs.microsoft.com/en-us/azure/app-service/web-sites-integrate-with-vnet)
* [Tutorial: integrate Functions with an Azure virtual network](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-vnet)
