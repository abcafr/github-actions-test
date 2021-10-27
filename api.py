# This API is used to learn the 'repository_dispatch' event trigger in a workflow.
# Use it to play around and make requests to your GitHub repository to
import requests

headers = {
    "Accept": "application/vnd.github.everest-preview+json",
    "Content-Type": "application/json"
}

data = {
    "event_type": "build"

}
r = requests.post(
    'https://github.com/abcafr/github-actions-test/actions/dispatches', data=data, headers=headers)
