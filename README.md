# Testing a template for a OCI container image

The purpose is a test sandbox and template for Python projects within an OCI container image.

## Features

* Dockerfile
  * Minimal: derived from Alpine
  * Adds user therefor commands don't run as root
  * Uses Python virtual environment to container requirements
  * Docker Buildx should allow setting UID/GID at build time
* Docker Compose file
  * Orchestrate container
  * Contains comments on how to override container "CMD" to allow exec of sh shell
  * Build using BuildX
    * `docker compose build`
    * `docker compose up -d`
    * `docker compose logs`
  * Secrets handling
* .dockerignore sample
* .githubignore sample
* src/python_demo
  * A quick python app to show the user running the Python script
* GitHub Actions
  * Dependabot
    * Update Dockerfile base OCI image
    * Update Python requirements.txt
  * OCI image build and publish to GitHub OCI image registry
  * GitHub OCI image registry cleanup of old images
