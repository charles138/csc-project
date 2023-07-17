# csc-project

The webpage for the [dbx Python quickstart](https://dbx.readthedocs.io/en/latest/guides/python/python_quickstart/) provides clear explanations and demonstrations for the following tasks:
1) Setting up the local environment to run dbx.
2) Running local unit tests.
3) Deploying workflows to Databricks.
4) Launching workflows on the Databricks platform.

In this repository, I followed the quickstart steps to set up the environment, run tests, and deploy the workflows. Additionally, I made some changes to demonstrate the deployment to the staging and production repositories of Databricks. There are various approaches to setting up development, staging, and production environments. I chose to use feature, main, and tag/release branches for the development, staging, and production environments, respectively. Here are the specific changes I made:
1) In the file tasks/sample_etl_task.py, I avoided using pandas 2.0 to resolve the error "AttributeError: 'DataFrame' object has no attribute 'iteritems'" in pandas 2.0.1.
2) In the file .github/workflows/onpush.yml, I have restricted the Push trigger to branches that begin with "feature*". This YAML file is responsible for executing the unit and integration tests.
3) In the file .github/workflows/after_pull_request_merge.yml, I added the deployment of the main branch to the staging repositories of Databricks after a Pull Request is merged.
4) In the file .github/workflows/onrelease.yml, I included the deployment of the tag/release branch to the production repositories of Databricks after tagging the code.

In addition to the prerequisites mentioned in the quickstart guide, it is recommended to have [GitHub CLI](https://cli.github.com/) installed in your local environment.


====================================================================================================================================
This is a sample project for Databricks, generated via cookiecutter.

While using this project, you need Python 3.X and `pip` or `conda` for package management.

## Local environment setup

1. Instantiate a local Python environment via a tool of your choice. This example is based on `conda`, but you can use any environment management tool:
```bash
conda create -n csc_project python=3.9
conda activate csc_project
```

2. If you don't have JDK installed on your local machine, install it (in this example we use `conda`-based installation):
```bash
conda install -c conda-forge openjdk=11.0.15
```

3. Install project locally (this will also install dev requirements):
```bash
pip install -e ".[local,test]"
```

## Running unit tests

For unit testing, please use `pytest`:
```
pytest tests/unit --cov
```

Please check the directory `tests/unit` for more details on how to use unit tests.
In the `tests/unit/conftest.py` you'll also find useful testing primitives, such as local Spark instance with Delta support, local MLflow and DBUtils fixture.

## Running integration tests

There are two options for running integration tests:

- On an all-purpose cluster via `dbx execute`
- On a job cluster via `dbx launch`

For quicker startup of the job clusters we recommend using instance pools ([AWS](https://docs.databricks.com/clusters/instance-pools/index.html), [Azure](https://docs.microsoft.com/en-us/azure/databricks/clusters/instance-pools/), [GCP](https://docs.gcp.databricks.com/clusters/instance-pools/index.html)).

For an integration test on all-purpose cluster, use the following command:
```
dbx execute <workflow-name> --cluster-name=<name of all-purpose cluster>
```

To execute a task inside multitask job, use the following command:
```
dbx execute <workflow-name> \
    --cluster-name=<name of all-purpose cluster> \
    --job=<name of the job to test> \
    --task=<task-key-from-job-definition>
```

For a test on a job cluster, deploy the job assets and then launch a run from them:
```
dbx deploy <workflow-name> --assets-only
dbx launch <workflow-name>  --from-assets --trace
```


## Interactive execution and development on Databricks clusters

1. `dbx` expects that cluster for interactive execution supports `%pip` and `%conda` magic [commands](https://docs.databricks.com/libraries/notebooks-python-libraries.html).
2. Please configure your workflow (and tasks inside it) in `conf/deployment.yml` file.
3. To execute the code interactively, provide either `--cluster-id` or `--cluster-name`.
```bash
dbx execute <workflow-name> \
    --cluster-name="<some-cluster-name>"
```

Multiple users also can use the same cluster for development. Libraries will be isolated per each user execution context.

## Working with notebooks and Repos

To start working with your notebooks from a Repos, do the following steps:

1. Add your git provider token to your user settings in Databricks
2. Add your repository to Repos. This could be done via UI, or via CLI command below:
```bash
databricks repos create --url <your repo URL> --provider <your-provider>
```
This command will create your personal repository under `/Repos/<username>/csc_project`.
3. Use `git_source` in your job definition as described [here](https://dbx.readthedocs.io/en/latest/guides/python/devops/notebook/?h=git_source#using-git_source-to-specify-the-remote-source)

## CI/CD pipeline settings

Please set the following secrets or environment variables for your CI provider:
- `DATABRICKS_HOST`
- `DATABRICKS_TOKEN`

## Testing and releasing via CI pipeline

- To trigger the CI pipeline, simply push your code to the repository. If CI provider is correctly set, it shall trigger the general testing pipeline
- To trigger the release pipeline, get the current version from the `csc_project/__init__.py` file and tag the current code version:
```
git tag -a v<your-project-version> -m "Release tag for version <your-project-version>"
git push origin --tags
```
