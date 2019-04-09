# Artifactory Cleanup
A cleanup script for Artifactory that removes old (currently older than 4 months) artifacts from Artifactory plus a Jenkins pipeline for running the script periodically. This is needed because Artifactory Cloud Pro doesn't offer out-of-the-box solution for cleaning the old snapshots. AQL (Artifactory Query Language) and Artifactory REST API are used in the implementation.

## Requirements
Python 2.7

## Adding repositories
To enable cleaning for your new Artifactory repository, it must be added to the list of cleaned repositories in the script file.

## Skipping cleanup for certain artifacts
Add the property "skipCleanup=true" in the Artifactory UI to any artifact that you want to keep indefinitely.

## Authors
* **Juha Luoto**

