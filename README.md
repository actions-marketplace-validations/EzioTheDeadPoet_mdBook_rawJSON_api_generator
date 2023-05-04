# mdBook Search GitHub Pages API generator

# Using this action

To use this action create or expand an existing workflow.yaml with the following implementations:

A dispatch workflow that can be triggered via the GitHub REST API:
Use case:

  - Push a new query to queries.json in the API branch (ideally using the GitHub REST API)
  - Trigger the workflow on the main branch (manually or ideally using the GitHub REST API)

```yaml
name: Prepare Queries
on:
    workflow_dispatch:
jobs:
    get-num-square:
      runs-on: ubuntu-latest
      name: Testing functionality
      steps:
        - name: Checkout
          uses: actions/checkout@v3
        - name: RUN PSEUDO-API Generator
          id: mdBook_site_to_JSON
          uses: ./
          with:
            github_token: ${{ secrets.GITHUB_TOKEN }}
            mbBook_url: https://rust-lang.github.io/mdBook/
            api_repo: ${{ github.repository }}
            api_branch: API

```

Update your queries once a new mdBook got deployed with GitHub pages:

  - Only works if you use this in the same repository as your mdBook
  - this is the last workflow that runs that alters the deployment branch

```yaml
name: Regenerate Cache
on:
  workflow_run:
    workflows: ["pages-build-deployment"] 
    types:
      - completed
  workflow_dispatch:

jobs:
    get-num-square:
      runs-on: ubuntu-latest
      name: Testing functionality
      steps:
        - name: Checkout
          uses: actions/checkout@v3
        - name: Run PSEUDO-API Generator
          id: mdBook_site_to_JSON
          uses: ./
          with:
            github_token: ${{ secrets.GITHUB_TOKEN }}
            mbBook_url: https://rust-lang.github.io/mdBook/
            api_repo: ${{ github.repository }}
            api_branch: API
            regenerate_cache: true

```
