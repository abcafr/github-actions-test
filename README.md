# Github Actions: Test

###### by Casper Frost

This repository will contain a myriad of trial and error on how to do actions in GitHub.

GitHub actions is the automation of software delivery workflows, as per GitHub documentation:

> Automate, customize, and execute your software development workflows right in your repository with GitHub Actions.
> You can discover, create, and share actions to perform any job you'd like, including CI/CD, and combine actions in a completely customized workflow.

To begin with, we will do some basic stuff, learn the terminology and slowly figure out how to use the features offered by GitHub actions to automate and optimize our CI/CD.

### Creating a workflow

1. To create a GitHub workflow, create the following path in your git repository: **.github/workflows/**.
1. Create a YML-file named after the workflows purpose, like 'provision_env.yml', and place it in the directory above, as such: **.github/workflows/provision_env.yml**.
