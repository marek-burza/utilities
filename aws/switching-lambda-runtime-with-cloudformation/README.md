# Switching Lambda Runtime with CloudFormation

This minimal example demonstrates switching the runtime of a Lambda function with help of CloudFormation templates.

The [v1.yml](./v1.yml) file contains a stack definition for a Lambda with Node.js as runtime.
The [v2.yml](./v2.yml) file contains a stack definition for a Lambda with Python as runtime.

Running the following two commands will first create a stack with the Node.js function and then modify it to Python:

```bash
aws cloudformation deploy --template-file v1.yml --stack-name EraseMe --capabilities CAPABILITY_NAMED_IAM --region eu-central-1
aws cloudformation deploy --template-file v2.yml --stack-name EraseMe --capabilities CAPABILITY_NAMED_IAM --region eu-central-1
```

Moving onwards to a dockerized Python workload:

```bash
aws ecr create-repository --repository-name erasemerepo
aws ecr set-repository-policy --repository-name erasemerepo --policy-text file://ecr-policy.json
$(aws ecr get-login)
export REPO_URI=$(aws ecr describe-repositories | jq '.repositories[] | select(.repositoryName=="erasemerepo") | .repositoryUri' -r)
docker build -t ${REPO_URI}:latest .
docker push ${REPO_URI}:latest
# The old stack must be deleted before swithching to the dockerized one
# (deleting only the function is not enough)
aws cloudformation delete-stack --stack-name EraseMe
aws cloudformation deploy --template-file v3.yml --stack-name EraseMe --capabilities CAPABILITY_NAMED_IAM --region eu-central-1 --parameter-overrides RepoUriParameter=${REPO_URI}:latest
```

Materials:

* [AWS Documentation - Deploy Python Lambda functions with container images](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html)
* [AWS Documentation - Creating Lambda functions defined as container images](https://docs.aws.amazon.com/lambda/latest/dg/configuration-images.html)
