# Role-based access control for CI/CD

For more information see [this link](https://docs.microsoft.com/en-us/azure/role-based-access-control/overview).

To create a security principal for use with CI/CD run:

    az ad sp create-for-rbac --name cicdbot
