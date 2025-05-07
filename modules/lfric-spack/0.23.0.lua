help("Name:     LFRic build environment\n"
     .. "Version:  " .. myModuleVersion() .. "\n"
     .. "\n" 
     .. [[
This module activates a spack environment suitable for loading software used to build LFRic.
]])

-- get lfric-spack base directory
local moddir,modname = splitFileName(myFileName())
local pkgBase = pathJoin(moddir,"..","..")

-- set simit-spack repository directory as an environment variable
setenv("SPACK_SIMIT_SPACK_REPOS",  pathJoin(pkgBase,"..","simit-spack","repos"))
-- set lfric-spack install,repository and environment directories as environment variables
setenv("SPACK_LFRIC_SPACK_INSTALL",  pathJoin(pkgBase,"install"))
setenv("SPACK_LFRIC_SPACK_REPOS",  pathJoin(pkgBase,"repos"))
setenv("SPACK_LFRIC_SPACK_ENVS",  pathJoin(pkgBase,"envs"))

-- load Archer2 spack module
prepend_path("MODULEPATH", "/mnt/lustre/a2fs-work4/work/y07/shared/archer2-lmod/others/dev")
depends_on("spack/"..myModuleVersion())

-- activate/deactivate LFRic spack environment on module load/unload
execute{cmd="spack env activate ${SPACK_LFRIC_SPACK_ENVS}", modeA={"load"}}
execute{cmd="spack env deactivate", modeA={"unload"}}
