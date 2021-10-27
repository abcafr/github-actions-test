# This API is used to learn the 'repository_dispatch' event trigger in a workflow.
# Use it to play around and make requests to your GitHub repository to
import requests
import json

headers = {
    "Accept": "application/vnd.github.everest-preview+json",
    "Content-Type": "application/json",
    "Authorization": "token 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"
}

data = {
    "event_type": "build"
}

r = requests.post(
    'https://api.github.com/repos/abcafr/github-actions-test/dispatches', data=data, headers=headers)

print(r.status_code)
print(json.dumps(r.json()))
