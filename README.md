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

Here are the steps to execute the tests:

## 1.	Import the repository to your GitHub. 
```bash
https://github.com/charles138/csc-project.git
```

## 2.	Preparing the local environment.
```bash
####--------------------------------------------------------
### Create conda environment
####--------------------------------------------------------
conda activate base
conda create -n charming-aurora python=3.9  -y
conda activate charming-aurora

####--------------------------------------------------------
### Install databricks cli and dbx
####--------------------------------------------------------
python -m pip install --upgrade pip
pip install databricks-cli --upgrade
pip install dbx --upgrade
databricks --version
dbx --version

####--------------------------------------------------------
### Setup Databricks cli
####--------------------------------------------------------
databricks configure --profile charming-aurora --token
databricks --profile charming-aurora workspace ls /Repos
```

## 3.	Clone the repository to your local laptop.
```bash
git clone https://github.com/<your_name>/csc-project.git
cd csc-project
```

## 4.	Install GitHub Cli 
```bash
# For Mac
brew install gh
gh auth login
gh workflow lis
```

## 5.	Setup GitHub for the repository – create secrets
Note: Please enable 'Allow all actions and reusable workflows' if not enabled.
```bash
gh secret set DATABRICKS_HOST
gh secret set DATABRICKS_TOKEN
gh secret list
```

## 6.	Setup at Databricks
•	Create a lightweight interactive cluster and modify the conf/deployment.yml file to eliminate the waiting times during the testing. Please note that it’s not recommended for the production environments. For best practices, please refer to [Cluster Type](https://dbx.readthedocs.io/en/latest/concepts/cluster_types/). Note: Replace CharlesCluster11 to your cluster name.

•	Create two repository folders: Staging and Production.
```bash
####--------------------------------------------------------
### Production Repo
####--------------------------------------------------------
databricks repos create --url "https://github.com/<your name>/csc-project.git" --provider gitHub --path "/Repos/Production/csc-project" --profile charming-aurora

####--------------------------------------------------------
### Staging Repo
####--------------------------------------------------------
databricks repos create --url "https://github.com/<your name>/csc-project.git" --provider gitHub --path "/Repos/Staging/csc-project" --profile charming-aurora
```

## 7.	Run unit tests
```bash
pip install -e ".[local,test]"
pytest tests/unit --cov
```

## 8.	Run integration tests
```bash
dbx execute csc-project-sample-tests --task=main --cluster-name="CharlesCluster11"
dbx deploy csc-project-sample-tests
dbx launch csc-project-sample-tests --trace
```

## 9.	Run ETL task
```bash
dbx execute csc-project-sample-etl --task=main --cluster-name="CharlesCluster11"
dbx deploy csc-project-sample-etl 
dbx launch csc-project-sample-etl --trace
```

## 10.	Trigger the unit and integration tests (.github/workflows/onpush.yml)
Note: For the steps 10 ~ 12, please choose proper feathurexx and vxx.xx.xx. 
```bash
git checkout main
git pull origin main
git checkout -b feature05
# Append a line to tag.txt, such as “csc 2023-07-17 09:00 feature05”.
git status
git add .
git commit -m "csc 2023-07-17 09:00: feature05"
git push --set-upstream origin feature05
```

## 11.	Trigger the deployment of the main branch repository to the staging environment (.github/workflows/after_pull_request_merge.yml)
```bash
gh auth login
gh pr create --title "csc 2023-07-17 09:00: feature05" --body "csc 2023-07-17 09:00: feature05"
gh pr merge -m -d
```

## 12.	Trigger the deployment of workflow and repository to the production environment (.github/workflows/onrelease.yml)
```bash
git pull origin main
# Append a line to tag.txt, such as “csc 2023-07-17 09:10 v2.0.0”.
git status
git add .
git commit -m "csc 2023-07-17 09:10: v2.0.0"
git push origin main

git tag -a v2.0.0 -m "v2.0.0"
git push origin v2.0.0
```


