# Switching Lambda Runtime with CloudFormation

This minimal example demonstrates switching the runtime of a Lambda function with help of CloudFormation templates.

The [v1.yml](./v1.yml) file contains a stack definition for a Lambda with Node.js as runtime.
The [v2.yml](./v2.yml) file contains a stack definition for a Lambda with Python as runtime.

Running the following two commands will first create a stack with the Node.js function and then modify it to Python:

```bash
aws cloudformation deploy --template-file v1.yml --stack-name EraseMe --capabilities CAPABILITY_NAMED_IAM --region eu-central-1
aws cloudformation deploy --template-file v2.yml --stack-name EraseMe --capabilities CAPABILITY_NAMED_IAM --region eu-central-1
```
