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

def main():
    deleteOldArtifactsFromAllRepos()

def deleteOldArtifactsFromAllRepos():
    for repo in getLocalRepos():
        deleteOldArtifacts(repo['key'])

def getLocalRepos():
    params = {'type': 'LOCAL'}
    r = requests.get(url = url + "/api/repositories", headers = headers, params = params)
    return json.loads(r.content)

def deleteOldArtifacts(repo):
    print "Finding removable artifacts for repository %s..." % repo
    criteria = createSearchCriteria(repo = repo, maxAgeInDays = 5)
    print criteria
    results = findArtifacts(criteria)
    print 'Found %s artifacts for %s ' % (results['range']['total'], repo)

def findArtifacts(criteria):
    query = "items.find(%s)" % criteria
    #query = 'items.find({"repo": "%s", "@skipCleanup": {"$ne": "true"}})' % repo
    r = requests.post(url = url + "/api/search/aql", headers = headers, data = query)
    return json.loads(r.content)

def createSearchCriteria(repo, maxAgeInDays):
    criteria = {}
    # Only search the given Artifactory repository
    criteria['repo'] = repo
    # Get artifacts created within maxAgeInDays
    criteria['created'] = {"$gt" : getIsoDate(maxAgeInDays)}
    # Skip any artifact that has the label skipCleanup set to 'true'
    criteria['@skipCleanup'] = {"$ne": "true"}
    return json.dumps(criteria)

def getIsoDate(daysAgo):
    d = date.today() - timedelta(days = daysAgo)
    return d.isoformat()

if __name__ == '__main__':
    main()
