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
1. Depending on the event-trigger, the workflow will now activate when you push code, make a pull-request ect.

### Using actions in your workflows

A workflow is written in YAML, which is a deserialization-language like JSON. The basic structure of a workflow could look like this:

```yaml
# The name of our workflow
name: Hello-World

# The 'on' keyword determines which event(s) will trigger the workflow, for example on: [push, pull_request] ect.
on: [push]

# The jobs section holds all the jobs that the workflow will do.
jobs:
  # The name of the job
  run-shell-command:
    # Choose the VM the workflow will run on
    runs-on: ubuntu-latest
    # The steps that the workflow will go through
    steps:
      - name: echo a string
        run: echo "Hello World"
      - name: multiline script
        # The pipe '|' character lets us do several lines of scripting in one 'run'
        run: |
          node -v
          npm -v
```

### Links to examples

- [Creating a simple workflow](https://github.com/abcafr/github-actions-test/blob/main/.github/workflows/simple.yml)
- [Using an action in your workflow](https://github.com/abcafr/github-actions-test/blob/main/.github/workflows/actions.yml)
