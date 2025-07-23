# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install lfric-apps
#
# You can edit this file again by typing:
#
#     spack edit lfric-apps
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class LfricApps(BundlePackage):
    """Dependencies of LFRic."""

    # FIXME: Add a proper url for your package's homepage here.
    # homepage = "https://www.example.com"
    # There is no URL since there is no code to download.

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers("github_user1", "github_user2")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    # license("UNKNOWN", checked_by="github_user1")

    version("1.2")
    version("2.0")
    version("2.1")
    version("2.2")

    # Dependencies
    depends_on("mpi")
    depends_on("hdf5+mpi")
    depends_on("netcdf-c+mpi")
    depends_on("netcdf-fortran")

    depends_on("yaxt")
    depends_on("py-jinja2")
    depends_on("xios@2252", when='@:2.0')
    depends_on("xios@2701", when='@2.1:')
    depends_on("py-psyclone@2.5.0", when='@:1.2')
    depends_on("py-psyclone@3.0.0", when='@2.0')
    depends_on("py-psyclone@3.1.0", when='@2.1:')
    depends_on("rose-picker")

    # depends_on("pfunit@3.2.9")

    # Set up environment paths
    def setup_run_environment(self, run_env):
        spec = self.spec

        # Compiler agnostic env vars
        run_env.set("FC", "ftn")
        run_env.set("LDMPI", "ftn")
        run_env.set("FPP", "cpp -traditional-cpp")
        run_env.set("LFRIC_TARGET_PLATFORM", "meto-xc40")
