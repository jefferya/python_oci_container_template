# Testing a template for a OCI container image

The purpose is a test sandbox and template for Python projects within an OCI container image.

## Features

* Dockerfile
  * Minimal: derived from Alpine
  * Uses Python virtual environment and requirements file to control package versions
  * Adds user therefore commands don't run as root
  * OCI image and docker-compose example of setting UID/GID at build time
    * `env UID=9999 docker compose up -d`
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
    * Buildx bake to add labels and annotations to the image + SBOM/provenance to enhance OCI image scanning such as Trivy.
    * Cache to enhance build time
  * GitHub OCI image registry cleanup of old images
  * Run Python Lint and code tests via Nox

## Scripts

Host some sample python scripts used for various purposes

* [Pierre Ouvrard Archive Bindings Web Scraping](./src/2026-07-08_sarah_severson_pierre_ouvrard_archive.org.py)
