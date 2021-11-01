# Github Actions: Test

###### by Casper Frost

This repository will contain a myriad of trial and error on how to do actions in GitHub.

GitHub actions is the automation of software delivery workflows, as per GitHub documentation:

> Automate, customize, and execute your software development workflows right in your repository with GitHub Actions.
> You can discover, create, and share actions to perform any job you'd like, including CI/CD, and combine actions in a completely customized workflow.

To begin with, we will do some basic stuff, learn the terminology and slowly figure out how to use the features offered by GitHub actions to automate and optimize our CI/CD.

## Index

- [Prerequisites](#prerequisites)
  - [SSH and GitHub](#ssh-and-github)
- [GitHub Actions: workflows, expressions and examples](#github-actions-workflows-expressions-and-examples)
  - [Creating a workflow](#creating-a-workflow)
  - [A sample workflow](#a-sample-workflow)
  - [Expressions & contexts](#expressions--contexts)
  - [The if-key and job status check functions](#the-if-key-and-job-status-check-functions)
    - [The if-key](#the-if-key)
    - [The job status check functions](#the-job-status-check-functions)
- [GitHub events & activity types](#github-events--activity-types)
  - [Event triggers](#event-triggers)
  - [Triggering a workflow with a RESTful request with repository_dispatch](#user-content-triggering-a-workflow-with-a-restful-request-with-repository_dispatch)
- [Events, environment variables and encryption](#events-environment-varaibles-and-decryption)
  - [Encrypting environment variables](#encrypting-environment-variables)
  - [Using the GITHUB_TOKEN for authenticating](#user-content-using-the-github_token-for-authenticating)
  - [Encrypting and decrypting files](#encrypting-and-decrypting-files)

## Prerequisites

### SSH and GitHub

If you are planning to use SSH over HTTPS to clone repositories (and you are), you need to do some configuration in order to make this possible:

First, create and add an SSH key to your host, and add it to GitHub afterwards. There is a great guide on how to do that here:

Secondly, because we are behind a corporate proxy, we need to configure our ssh-agent to be able to make our ssh-tunnel through that.
Here is how to do that:

1. Go to your .ssh folder (typically in your home directory: /home/$USER/.ssh)
1. See if there is a config file with **ls -la**
   1. If there is, go to the next step
   1. If not, add it with **touch config**
1. Add this to the config file:

```bash
Host github.com
  HostName github.com
  User $GITHUB_ACTOR
  AddKeysToAgent yes
  PreferredAuthentications publickey
  ProxyCommand nc -X connect -x $ALMBRAND_PROXY %h %p
```

Where `GITHUB_ACTOR` is your login, and `ALMBRAND_PROXY` is the proxy URL.

Now your client should be able to pull repositories from GitHub with ssh.

## GitHub Actions: worflows, expressions and examples

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

### Expressions & contexts

In our workflows we will use expressions, which has the syntax `${{ EXPRESSION }}`. An expression evaluates the value of the objects
inside the curly brackets, and puts it as a value instead.

An expression can be:

- One value or object: `${{ object }}`
- A value in an object: `${{ object.value }}`
- A boolean or a string (and operators): `${{ true || 'abc' }}`

[GitHub provides some objects we can use in our workflows](https://docs.github.com/en/actions/learn-github-actions/contexts). However, expressions can also evaluate functions. Observe the snippet below:

```yaml
jobs:
  get-github-context:
    runs-on: ubuntu-latest
    steps:
      - name: Dump GitHub context
        env:
          GITHUB_CONTEXT: ${{ toJSON(github) }}
        run: echo "$GITHUB_CONTEXT"
```

In the `env` section, a `GITHUB_CONTEXT` variable is set to be the output of the function `toJSON(github)`.

- `github` is the object that github provides us, with all sorts of metadata
- `toJSON()` is the function that evaluates the object as a JSON object.
- The echo command will print out the entire `github` object in JSON format.

[You can find a list of the functions that you can use in GitHub here](https://docs.github.com/en/actions/learn-github-actions/expressions).

#### The if-key and job status check functions

Sometimes you want some jobs or steps in your workflow to run on certain conditions, like if a push event is triggered, or if a job fails to run.

#### The if-key

Say you want your workflow to do something on a pull request, and something else on a pull_request. You can use the if-key like so:

```yaml
name: The If-key

on: [push, pull_request]

jobs:
  push:
  runs-on: ubuntu-latest
  if: github.event_name == 'push'
  steps:
    - name: print push message
      run: echo "This will only print on a push event"
  pull_request:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  steps:
    - name: print pull_request message
      run: echo "This will only print on a pull_request event"

```

#### Job status check functions

You can use job status check functions like `failure()` or `always()`to control the flow of your steps:

```yaml
name: Job Status Check Functions

on: push

jobs:
  counter:
    runs-on: ubuntu-latest
    steps:
      - name: 1
        run: echo 1
      - name: 2
        run: echo 2
      - name: 3
        if: failure()
        run: echo 3
      - name: 4
        run: eccho 4
      - name: 5
        if: always()
        run: echo 5
```

If we observe the snippet above, the above workflow will print '1, 2, 3, 5", because:

- 1 will run
- 2 will run
- 3 will not run, because the `if: failure()` means it will only run if the job above fails
- 4 will fail because there is no such command as `eccho`
- 5 will run because `if: always()` means that the step will run no matter what

[You can find a list of the job status check functions here](https://docs.github.com/en/actions/learn-github-actions/expressions#job-status-check-functions)

## GitHub events & activity types

### Event triggers

GitHub actions can be triggered in many stages of the development process. The most common would be when a developer
pushes his code, but there are other events that can trigger one or more workflows.

A simple event trigger in a workflow will look like this:

```yaml
name: Simple event trigger

# The workflow in this case will be triggered when code is pushed, and is declared as an array.
on: [push, pull_request]
```

But what if you need something to be done when you make a pull request, assigns a pull request, closes it ect?
Some activities has several activity types, such as the pull request. It can be opened, closed, assigned, synchronized and so on.
GitHub lets us declare those activities as objects, where we can choose which types should trigger the workflow:

```yaml
name: More complex event trigger

# In this case, the activities are a set of objects, where the objects activity type can be selected from an array:
on:
  push:
  pull_request:
    types: [closed, assigned, opened, reopened]
```

On this page you can see all the activities that can trigger an event:
https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows

### Triggering a workflow with a RESTful request with **repository_dispatch**

We've seen two ways that a workflow can be triggered in GitHub:

- An array of events: [push, pull_request]
- A triggering on an event type:
  pull_request:
  types: [closed, assigned, opened]

The third way is with an event called **repository_dispatch**, and is triggered when a RESTful request is made to the repositorys API.
This workflow:

```yaml
name: Trigger On Repository Dispatch

on:
  repository_dispatch:
    types: [build]
```

will activate when a request, with the event type "**build**", is sent to the API.

The URL to your repository_dispatch API follows this structure:

```yaml
"https://api.github.com/repos/${{ GITHUB_USER }}/${{ GITHUB_REPO }}/dispatches"
```

And the following information is needed with the request:

```yaml
# Headers
"Accept": "application/vnd.github.everest-preview+json",
"Content-Type": "application/json",
"Authorization": "token ${{ GITHUB_PERSONAL_TOKEN }}"

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

Where `GITHUB_PERSONAL_TOKEN` is a token that you can create yourself for authentication.

## Environments, encryption and authentication

This section gives some insights as to how you can create and use environment variables in GitHub actions, and use those to authenticate jobs, decrypt files and other useful tools needed to make your workflows as standardized and flexible as possible.

### Encrypting environment variables

In your workflow files, you will encounter situations where we need to access some environment variables, that should not be uploaded to the repository.
This could be an API-key, an access token, a password ect.
For this, we can [enter environment variables in our repository](https://docs.github.com/en/actions/learn-github-actions/environment-variables)
To do this in your Repository, go to the repositorys **Settings** -> **Secrets** and add the environment variable.

To access this again, GitHub gives the secrets as objects, so it is accessible with the following: `${{ secrets.MY_VARIABLE }}`

### Using the GITHUB_TOKEN for authenticating

Sometimes you need authentication when using some GitHub action, like the below example:

```yaml
name: Pull Request Labeler
on:
  pull_request:
  jobs:
    labeler:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/labeler@v2
          with:
            repo-token: ${{ secrets.GITHUB_TOKEN }}
```

This workflow uses the 'labeler' action, and for the runner to be able to tag the pull requests, it needs to authenticate with the `GITHUB_TOKEN` secret.

### Encrypting and decrypting files

Because an environment variable in GitHub has a max memory limit, we could eventually find ourselves in a situation where we have a large datafile with secrets that we need to access in our workflow. Instead of entering them one by one in GitHub, we can encrypt it when we push it to GitHub, and decrypt it when we need it in our workflow.

For encrypting the file we need a tool, and here we will use [The GNU Privacy Guard (GPG)](https://gnupg.org)

On Mac/Linux, the syntax for encrypting a file with GPG is:
`gpg --symmetric --cipher-algo AES256 my_secret.json`

You will be prompted to enter a password for the encrypted file, and a **my_secret.json.gpg** file will be created.

```
NB: if you are connected to a host via SSH, you will not be promted a password with the above command.
To get around this, pass --pinentry-mode=loopback with the other arguments to be prompted a passphrase in
your terminal.
```

With the encrypted file in our repository, we can now decrypt it in a job in a workflow:

```yaml
name: Decrypt an encrypted file

on: [push]

jobs:
  decrypt:
    runs-on: ubuntu-latest
    steps:
      # Checks out the repository in the VM
      - uses: actions/checkout@v1
      - name: Decrypt file
        # This command will take the encryptet file 'secret.json.gpg' and decrypt it
        # using the passphrase given as a secret in the environment, and output it as
        # secret.json in the home directory.
        run: gpg --quiet --batch --yes --decrypt --passphrase="$PASSPHRASE"
          --output $HOME/secret.json secret.json.gpg
        env:
          # This gets the passphrase in your repository, and adds it as
          # an environment variable
          PASSPHRASE: ${{ secrets.PASSPHRASE }}
      - name: Print our file content
        run: cat $HOME/secret.json
```

You should now be able to see the contents of `secret.json` in the last step in the job.

### Links to examples

- [Creating a simple workflow](https://github.com/abcafr/github-actions-test/blob/main/.github/workflows/simple.yml)
- [Using an action in your workflow](https://github.com/abcafr/github-actions-test/blob/main/.github/workflows/actions.yml)
- [Making an API request to repository dispatch in Python(work in progress)](https://github.com/abcafr/github-actions-test/blob/main/api.py)
- [Using environment variables in your workflow](https://github.com/abcafr/github-actions-test/blob/main/.github/workflows/env.yml)
