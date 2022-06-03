# WSCBS_Assignment4b_Brane_Pipeline

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6612423.svg)](https://doi.org/10.5281/zenodo.6612423)

## Introduction

This course project is about using the Brane framework to implement a data processing pipeline. Our pipeline is built for the Kaggle challenges -- [Titanic – Machine Learning from Disaster](https://www.kaggle.com/c/titanic/overview). 

Note, in this project, we are not only focusing on the machine learning and data processing part, the other goal is to complete the process of this production pipeline through the framework of [Brane](https://github.com/epi-project/brane).

This is an assignment of Web Service and Cloud-Based Service course in UvA at period 5, 2021-2022.

## Structure

Our pipeline consists of four Brane packages: `setup` `getfeatures`, `trainandpredict` and `visualization`.

### The compute package
- [getfeatures](https://github.com/TISNN/brane-getfeatures)
- [trainandpredict](https://github.com/TISNN/brane-trainandpredict)

### The visualization package
- [visualization](https://github.com/TISNN/brane-visualization)

Among them, `setup` is the package used for data preparation. `getfeatures` and `trainandpredict` are packages used for computation, including data processing and model training functions. And, `visualization` package is used to generate corresponding figures based on the processed data.

## Getting-Started

We use submodule for each individual package of this repository. To clone the whole repository, run :
```shell
$ git clone --recurse-submodules https://github.com/TISNN/WSCBS_Assignment4b.git
```
For getting each submodule, please go to the package's git repository. All of the details of code documentation and setup instructions are listed in the `README.md` at each submodule.
- [init](https://github.com/TISNN/brane-setup)
- [getfeatures](https://github.com/TISNN/brane-getfeatures)
- [train_predict](https://github.com/TISNN/brane-trainandpredict)
- [visual](https://github.com/TISNN/brane-visualization)

## Running the pipeline
After the installation of Brane environment, use `makefile` to build all the brane package, it will take about 6 mins.

```shell
$ make
```

Also, users can directly import the package via `brane import` commands.
```shell
$ brane import TISNN/brane-getfeatures
$ brane import TISNN/brane-trainandpredict
$ brane import TISNN/brane-visualization
```

The complete pipeline implementing by BraneScript is in `pipeline.ipynb`.

## Testing
We created both python unit testing and automated testing by GitHub Actions and BraneScript.

### 1. pytest
Since we are writing each package separately, unit testing for the core functions is necessary to ensure they are executed correctly. To do so, we've built python scripts to test each of our functions individually. The pytest scripts are put in the `pytest.py` file, in each package.

### 2. Automated testing by Branescript
Another complete test is to consider the execution of the pipeline in Brane. For this testing, we created automated test workflow for each Brane package, using GitHub Actions service.

The steps for testing include:

1. Setup of Docker, Docker Compose, Docker Buildx.
2. Install Brane CLI (by copy `usr/local/bin/brane` file)
3. Build the Brane package
4. Run package by BraneScript.

The BraneScript is executed by the `brane run` command in the form of `test.txt`. We can determine whether it has successfully completed the task by examining the results of the execution.

After accomplishing this, we have actually built the complete CI/CD, which is part of the standard development workflow. Every time we use `git push` to update our code, Github Actions will automatically test it based on the workflow *(.github/workflow/cicd_test.yml)* we created. For each package in this project, it takes about 6 minutes to complete the branescript testing.

## Notes

### Run pipelines on cluster
At the beginning of the project, we have been trying to run brane directly on the cluster, but unfortunately due to kernel, RAM issues (or other problems), we were not able to successfully install the Brane environment on the cluster.

After installing Brane on another linux machine, we fetched the binary executable compiled `brane` file and uploaded it to `/usr/local/bin` of the cluster machine, so that we could finally run our packages on the cluster.

### DOI
We created DOIs for each package by archiving it on Zenodo.
