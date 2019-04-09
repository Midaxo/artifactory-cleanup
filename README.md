# Artifactory Cleanup
A cleanup script for Artifactory that removes old (currently older than 4 months) artifacts from Artifactory plus a Jenkins pipeline for running the script periodically. This is needed because Artifactory Cloud Pro doesn't offer out-of-the-box solution for cleaning the old snapshots. Artifact is never removed in two cases:

- Its name begins with release-*
- It has Artifactory property "skipCleanup=true" set

Deleting artifact from Artifactory actually just puts it into trashcan. The trashcan must be emptied to remove the artifact permanently. Emptying the trash is done at the beginning of the script. This means that - since the script is run every day at midnight - there's a time window of 24h to restore an artifact that was accidentally deleted before it gets permanently removed during the next run.

AQL (Artifactory Query Language) and Artifactory REST API are used in the implementation.

## Requirements
Python 2.7

## Adding repositories
To enable cleaning for your new Artifactory repository, it must be added to the list of cleaned repositories in the script file.

## Skipping cleanup for certain artifacts
Add the property "skipCleanup=true" in the Artifactory UI to any artifact that you want to keep indefinitely.

## Authors
**Juha Luoto**

