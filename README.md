# mdBook Indexer

# Using this action

To use this action create or expand an existing workflow.yaml
```yaml
name: Test Action
on:
    page_build: # recommended so the task always runs when the website got redeployed (Only works if this is used on the same repository as the mdBook github pages deployment)
    push:
        branches: [main]
    pull_request:
        branches: [main]
    workflow_dispatch:

jobs:
    get-num-square:
      runs-on: ubuntu-latest
      name: Testing functionality
      steps:
        - name: Checkout
          uses: actions/checkout@v2
        - name: Index mdBook 
          id: mdBook_site_to_JSON
          uses: EzioTheDeadPoet/actions-mdBook-indexer@v2
          with:
            github_token: ${{ secrets.GITHUB_TOKEN }} # Mandatory for the action to write to the desired output branch
            mdBook_url: https://wiki.wabbajack.org/ # URL to the hosted mdBook
            output_branch: index_json # Output Branch
            output_file: example_output.json # Desired output name (optional with default: mdBook_index.json)
```
