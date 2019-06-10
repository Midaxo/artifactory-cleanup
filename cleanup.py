import os
import base64
import json
from datetime import date, timedelta
import requests

url = "https://midaxo.jfrog.io/midaxo"
username = os.environ['ARTIFACTORY_USERNAME']
password = os.environ['ARTIFACTORY_PASSWORD']
credentials = base64.b64encode(username.encode() + b":" + password.encode())
headers = {'Authorization': b'Basic ' + credentials}
artifactAgeInDays = 120

cleanupRepos = [
    'account-settings',
    'admin-console',
    'apigateway',
    'auth',
    'exago',
    'exago-api-loader',
    'exago-integration-service',
    'exago-web',
    'frontend',
    'platform',
    'sharepoint',
    'multibranch-pipeline-example'
]

cleanupDockerRepos = [
    'docker-local'
]


def main():
    # Clean all the repos found in the list
    for repo in cleanupRepos:
        deleteOldArtifacts(repo)
    for repo in cleanupDockerRepos:
        deleteOldArtifacts(repo)


def deleteOldArtifacts(repo):
    criteria = createSearchCriteria(repo=repo)
    results = findArtifacts(criteria)
    print('\n\n\n*** Found %s removable artifacts for %s ***' %
          (results['range']['total'], repo))
    for artifact in results['results']:
        deleteArtifact(artifact)


def findArtifacts(criteria):
    query = "items.find(%s)" % criteria
    r = requests.post(url=url + "/api/search/aql", headers=headers, data=query)
    return json.loads(r.content)


def createSearchCriteria(repo):
    criteria = {}
    # Only search the given Artifactory repository
    criteria['repo'] = repo
    # Get artifacts created within artifactAgeInDays
    criteria['created'] = {"$lt": getDateDaysAgo(artifactAgeInDays)}
    # Only include artifacts that DO NOT have skipCleanup set to 'true'
    criteria['@skipCleanup'] = {"$ne": "true"}
    # Do not include release artifacts
    if repo in cleanupDockerRepos:
        # manifest.json here is so we don't target individual layers
        # artifactory will clean orphaned layers up automatically
        criteria['name'] = {"$eq": "manifest.json"}
        criteria['@docker.manifest'] = {"$nmatch": "release-*"}
    if repo in cleanupRepos:
        criteria['name'] = {"$nmatch": "release-*"}
    return json.dumps(criteria)


def getDateDaysAgo(daysAgo):
    d = date.today() - timedelta(days=daysAgo)
    return d.isoformat()


def deleteArtifact(art):
    # If art['name] is manifest.json, this is a docker artifact
    artifact_name = art['name'] if art['name'] != 'manifest.json' else False
    # In case of a docker repository
    # URL should not include /manifest.json
    # or only the manifest will be deleted
    full_url = "%s/%s/%s/%s" % (url, art['repo'], art['path'],
                                (artifact_name if artifact_name else ''))
    print("Deleting artifact: %s" %
          (artifact_name if artifact_name else art['path']))
    r = requests.delete(url=full_url, headers=headers)


if __name__ == '__main__':
    main()
