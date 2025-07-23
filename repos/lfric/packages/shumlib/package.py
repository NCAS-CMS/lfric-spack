# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
from spack.package import MakefilePackage


class Shumlib(MakefilePackage):

    """Shared UM Library.

    Shumlib is the collective name for a set of libraries which are
    used by the UM; the UK Met Office's Unified Model, that may be of
    use to external tools or applications where identical
    functionality is desired. The hope of the project is to enable
    developers to quickly and easily access parts of the UM code that
    are commonly duplicated elsewhere, at the same time benefiting
    from any improvements or optimisations that might be made in
    support of the UM itself.
    """

    homepage = "https://code.metoffice.gov.uk"
    url = "https://github.com/metomi/shumlib/archive/refs/tags/um13.9.tar.gz"

    # shumlib does not currently build in parallel
    parallel = False

    version(
        "13.9",
        sha256="3f577ad55ffd20c79aba92c1a5698df79722b698ab8ee0548a80043ed169cbc8",
    )
    version(
        "13.0",
        sha256="50f43a2f8980e8fbeafd053376612503bcb17c34948297f19b2c95ce0642b340",
    )

    variant("openmp", default=False, description="enable OpenMP support")

    def patch(self):

        """Patch GCC<12 work around ieee_arithmetic module problem.

        With GCC<12 versions the following does not compile
          USE, INTRINSIC :: ieee_arithmetic, ONLY: OPERATOR(==)
        changing to
          USE, INTRINSIC :: ieee_arithmetic, ONLY: OPERATOR(.eq.)
        fixes it.
        """

        if self.spec.satisfies("%gcc@:11"):
            # Only patch for GCC 11 and below
            filter_file(
                r"OPERATOR\(==\)",
                "OPERATOR(.eq.)",
                "shum_number_tools/src/f_shum_is_inf.F90",
            )

        return

    def edit(self, spec, prefix):

        """Minor setup edits."""

        # Create a copy of the makefile
        if self.spec.satisfies("%cce"):
            source = "make/meto-ex1a-crayftn12.0.1+-craycc.mk"
        elif self.spec.satisfies("%gcc"):
            source = "make/meto-ex1a-gfortran-gcc.mk"
        self.dest = "make/spack.mk"
        shutil.copy(source, self.dest)

        # FIXME: set a better identifier
        makefile = FileFilter(self.dest)
        makefile.filter(r"^\s*PLATFORM\s*=.*", "PLATFORM=spack-fortran-cc")

    def build(self, *args, **kwargs):

        super().build(*args, **kwargs)

    def install(self, spec, prefix):

        mkdir(prefix.lib)
        install_tree("build/spack-fortran-cc/lib", prefix.lib)
        mkdir(prefix.include)
        install_tree("build/spack-fortran-cc/include", prefix.include)

    @property
    def build_targets(self):

        current = os.getcwd()

        args = ["-f", self.dest, f"DIR_ROOT={current}", f"LIBDIR_ROOT={current}/build"]

        if "+openmp" in self.spec:
            # args.append("SHUM_USE_C_OPENMP_VIA_THREAD_UTILS=true")
            env["SHUM_USE_C_OPENMP_VIA_THREAD_UTILS"] = "true"

            # Build openmp version
            env["SHUM_OPENMP"] = "true"
        else:
            # Build non-openmp version
            env["SHUM_OPENMP"] = "false"

        return args

    def setup_run_environment(self, env):
        """Setup custom variables in the generated module file"""

        env.prepend_path("FFLAGS", "-I" + self.spec.prefix.include, " ")
        env.prepend_path("CPPFLAGS", "-I" + self.spec.prefix.include, " ")
        env.prepend_path("LDFLAGS", "-L" + self.spec.prefix.lib + " -Wl,-rpath=" + self.spec.prefix.lib, " ")
