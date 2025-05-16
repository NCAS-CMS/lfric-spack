# lfric-spack

The purpose of this repository is to install a spack environment on Archer2 to enable building and running of the Met. Office LFRic model.

## Installing lfric spack packages and dependencies

**Step 1** is to install the needed packages under a local user account, as the Archer2 login nodes do not have enough resources to build some of the packages the installation should be done using a batch job. There is an example batch job script included `archer2_install.job`. This job is setup to build all packages using the gcc compiler and can be modified as needed. Run the job

```
sbatch archer2_install.job
```

The installation of rose-picker will fail (and the packages which depend on it) as it needs to fetch the source code from the Met. Office Science Repository Service, for which a valid account is needed and a password needs to be provided. It is not possible to provide the password within a batch job so this package will need to be installed on the command line

```bash
spack install rose-picker %gcc@11
```

Next resubmit `archer2_install.job` to install the packages which depend on rose-picker.

**Step 2** is to install the packages under the LFRic shared account. First login to the `lfric` user account and copy file `sync_lfric_shared.sh` to the directory where your want the lfric spack packages to be installed. This script uses `rsync` to copy the lfric-spack github directory and it will also copy the Met. Office `simit-spack` repository. The script uses environment variables to specify the source and destination directories, change these as necessary and also change the same variables in script `update_lfric_shared.sh`. Run the script

```bash
./sync_lfric_shared.sh
```

The next step is to install the same packages as before, when installing previously a build cache was created and this can now be used to install the packages under the LFRic shared account. Installing using the build cache should be easier and quicker than before, a batch job is not necessary and no password should be needed. The install process should take less than 30 minutes. Run the script

```bash
./update_lfric_shared.sh
```

## Using lfric spack packages

To load the environment to build and run lfric apps version 2.1, run the following

```bash
module use /work/y07/shared/lfric/software/spack/lfric-spack/modules
module load PrgEnv-gnu
module load lfric-spack
spack load lfric-apps@2.1%gcc
```

There are also lfric apps versions 2.0 and 1.2 available. Alternatively there is also the lfric-meta package which is the same as the lfric-apps package except XIOS is not loaded.

Alternatively you can loaded the needed packages explicitly and set some environment variables needed by the LFRic build system.

```bash
module use /work/y07/shared/lfric/software/spack/lfric-spack/modules
module load PrgEnv-gnu
module load lfric-spack
spack load yaxt%gcc py-jinja2%gcc rose-picker%gcc xios@2701%gcc py-psyclone@3.1.0%gcc
export FC=ftn
export LDMPI=ftn
export FPP="cpp -traditional-cpp"
export LFRIC_TARGET_PLATFORM=meto-xc40
```
