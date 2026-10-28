# Jenkins release candidate and production integration boundary

The original root `Jenkinsfile` is an **existing deployment pipeline** and has not been overwritten. The reviewed candidate in `pipelines/Jenkinsfile.reviewed` is an alternative that requires Jenkins administrator review, credential setup and a deliberate job configuration change before it can deploy.

## Separation of duties

All builds run tests and build a container candidate. Only the `main` branch with `PUBLISH_TO_DEV=true` publishes a commit-tagged image or changes GitOps. The GitOps update fails on ambiguous image matches, refuses mutable tags, and stops on competing remote updates. Credentials are sourced from Jenkins Credentials and never embedded in the Git URL. To achieve full immutable delivery, resolve the published image digest and record digest-pinned promotion as a later controlled step.

## Transition and rollback

Before enabling the candidate: configure a dedicated least-privilege token permitted to update only the GitOps repository, set masked credentials, verify protected branch approval and Docker runner isolation. Confirm the GitOps repository's active Argo CD controller and its current commit. Run dry-run verification against a temporary branch. Roll back by reverting the reviewed GitOps commit, not by editing live pods or force-pushing protected history.

## Required acceptance criteria

A passing GitHub Actions check demonstrates source-level tests, not that Jenkins was configured or used. Before calling this a live production pipeline, collect Jenkins run URLs, image digest evidence, Argo synchronization proof, smoke tests, release approval IDs and rollback verification.
