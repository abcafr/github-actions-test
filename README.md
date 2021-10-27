# Github Actions: Test

###### by Casper Frost

This repository will contain a myriad of trial and error on how to do actions in GitHub.

GitHub actions is the automation of software delivery workflows, as per GitHub documentation:

> Automate, customize, and execute your software development workflows right in your repository with GitHub Actions.
> You can discover, create, and share actions to perform any job you'd like, including CI/CD, and combine actions in a completely customized workflow.

To begin with, we will do some basic stuff, learn the terminology and slowly figure out how to use the features offered by GitHub actions to automate and optimize our CI/CD.

### Creating a workflow

1. To create a GitHub workflow, create the following path in your git repository: **.github/workflows/**.
1. Create a YML-file named after the workflows purpose, like 'actions.yml', and place it in the directory above, as such: **.github/workflows/actions.yml**.
1. Depending on the event-trigger, the workflow will now activate when you push code, make a pull-request ect.

### A sample workflow

A workflow is written in YAML, which is a deserialization-language like JSON. The basic structure of a workflow could look like this:

```yaml
# The name of our workflow
name: Hello-World

# The 'on' keyword determines which event(s) will trigger the workflow, for example on: [push, pull_request] ect.
on: [push]

# The jobs section holds all the jobs that the workflow will execute.
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

### GitHub events & activity types

GitHub actions can be triggered in many stages of the development process. The most common would be when a developer
pushes his code, but there are other events that can trigger one or more workflows.

A simple event trigger in a workflow will look like this:

```yaml
name: Simple event trigger

# The workflow in this case will be triggered when code is pushed, and is declared as an array.
on: [push]
```

But what if you need something to be done when you make a pull request, assigns a pull request, closes it ect?
Some activities has several activity types, such as the pull request. It can be opened, closed, assigned, synchronized and so on.
GitHub lets us declare those activities as objects, where we can choose which types should trigger the workflow:

```yaml
name: Complex event trigger

# In this case, the activities are a set of objects, where the objects activity type can be selected from an array:
on:
  push:
  pull_request:
    types: [closed, assigned, opened, reopened]
```

On this page you can see all the activities that can trigger an event:
https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows

## triggering a workflow with a RESTful request with _repository_dispatch_

We've seen two ways that a workflow can be triggered in GitHub:

- An array of events: [push, pull_request] ect.
- A triggering on an event type:
  pull_request:
  types: [closed, assigned, opened] ect.

The third way is with an event called _repository_dispatch_, and is triggered when a RESTful request is made to the repositorys API.
This code:

```yaml
name: Trigger On Repository Dispatch

on:
  repository_dispatch:
    types: [build]
```

Is activated when a request, with the payload _build_, is sent to the API.

The URL to your repository_dispatch API follows this structure:

```yaml
"https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}/dispatches"
```

And the following information is needed with the request:

```yaml
# Headers
"Accept": "application/vnd.github.everest-preview+json",
"Content-Type": "application/json",
"Authorization": "token ${GITHUB_TOKEN}"

# payload
data = {
  # Necessary
  "event_type": "build",
  # Optional
  "client_payload": {
    "env": "production"
  }

}

```

Where $GITHUB_TOKEN is a token that you can create yourself, if it is for a personal project, or you can request to get access to that token
if you are a part of that project.

### Links to examples

- [Creating a simple workflow](https://github.com/abcafr/github-actions-test/blob/main/.github/workflows/simple.yml)
- [Using an action in your workflow](https://github.com/abcafr/github-actions-test/blob/main/.github/workflows/actions.yml)
- [Making an API request to repository dispatch in Python(work in progress)](https://github.com/abcafr/github-actions-test/blob/main/api.py)
