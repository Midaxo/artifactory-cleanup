import os
import base64
import requests
import json
from datetime import date, timedelta

url = "https://midaxo.jfrog.io/midaxo"
username = os.environ['ARTIFACTORY_USERNAME']
password = os.environ['ARTIFACTORY_PASSWORD']
credentials = base64.b64encode(username + ":" + password)
headers = {'Authorization': 'Basic ' + credentials}
artifactAgeInDays = 120

cleanupRepos = [
    'Midaxo.Auth',
    'account-settings',
]

#    'account-settings',
#    'admin-console',
#    'apigateway',
#    'auth',
#    'exago',
#    'exago-api-loader',
#    'exago-integration-service',
#    'exago-web',
#    'frontend',
#    'platform',
#    'sharepoint'

def main():
    for repo in cleanupRepos:
        deleteOldArtifacts(repo)

def deleteOldArtifacts(repo):
    criteria = createSearchCriteria(repo = repo)
    results = findArtifacts(criteria)
    print 'Found %s removable artifacts for %s ' % (results['range']['total'], repo)
    for artifact in results['results']:
        deleteArtifact(artifact)

def findArtifacts(criteria):
    query = "items.find(%s)" % criteria
    r = requests.post(url = url + "/api/search/aql", headers = headers, data = query)
    return json.loads(r.content)

def createSearchCriteria(repo):
    criteria = {}
    # Only search the given Artifactory repository
    criteria['repo'] = repo
    # Get artifacts created within artifactAgeInDays
    criteria['created'] = {"$lt" : getDateDaysAgo(artifactAgeInDays)}
    # Only include artifacts that DO NOT have skipCleanup set to 'true'
    criteria['@skipCleanup'] = {"$ne": "true"}
    # Do not include release artifacts
    criteria['name'] = {"$nmatch":"release-*"}

    return json.dumps(criteria)

def getDateDaysAgo(daysAgo):
    d = date.today() - timedelta(days = daysAgo)
    return d.isoformat()

def deleteArtifact(art):
    full_url = "%s/%s/%s/%s" % (url, art['repo'], art['path'], art['name'])
    print "Deleting artifact: " + full_url
    #r = requests.delete(url = full_url, headers = headers)
    #print r.content

if __name__ == '__main__':
    main()
