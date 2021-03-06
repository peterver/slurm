# $Id$
#
# Note that this package is not relocatable

#
# build options      .rpmmacros options      change to default action
# ===============    ====================    ========================
# --with aix         %_with_aix         1    build aix RPM
# --with authd       %_with_authd       1    build auth-authd RPM
# --with auth_none   %_with_auth_none   1    build auth-none RPM
# --with blcr        %_with_blcr        1    require blcr support
# --with bluegene    %_with_bluegene    1    build bluegene RPM
# --with cray_xt     %_with_cray_xt     1    build for Cray XT system
# --with debug       %_with_debug       1    enable extra debugging within SLURM
# --with elan        %_with_elan        1    build switch-elan RPM
# --with lua         %_with_lua         1    build SLURM lua bindings (proctrack only for now)
# --without munge    %_without_munge    1    don't build auth-munge RPM
# --with mysql       %_with_mysql       1    require mysql support
# --with openssl     %_with_openssl     1    require openssl RPM to be installed
# --without pam      %_without_pam      1    don't require pam-devel RPM to be installed
# --with postgres    %_with_postgres    1    require postgresql support
# --without readline %_without_readline 1    don't require readline-devel RPM to be installed
# --with sgijob      %_with_sgijob      1    build proctrack-sgi-job RPM
# --with sun_const   %_with_sun_const   1    build for Sun Constellation system
# --with-srun2aprun  %_with_srun2aprun  1    build srun as aprun wrapper

#
#  Allow defining --with and --without build options or %_with and %without in .rpmmacors
#    slurm_with    builds option by default unless --without is specified
#    slurm_without builds option iff --with specified
#
%define slurm_with_opt() %{expand:%%{!?_without_%{1}:%%global slurm_with_%{1} 1}}
%define slurm_without_opt() %{expand:%%{?_with_%{1}:%%global slurm_with_%{1} 1}}
#
#  with helper macro to test for slurm_with_*
#
%define slurm_with() %{expand:%%{?slurm_with_%{1}:1}%%{!?slurm_with_%{1}:0}}

#  Options that are off by default (enable with --with <opt>)
%slurm_without_opt auth_none
%slurm_without_opt authd
%slurm_without_opt bluegene
%slurm_without_opt cray
%slurm_without_opt debug
%slurm_without_opt elan
%slurm_without_opt sun_const
%slurm_without_opt srun2aprun

# These options are only here to force there to be these on the build.
# If they are not set they will still be compiled if the packages exist.
%slurm_without_opt mysql
%slurm_without_opt postgres
%slurm_without_opt blcr
%slurm_without_opt openssl

# Build with munge by default on all platforms (disable using --without munge)
%slurm_with_opt munge

# Build with OpenSSL by default on all platforms (disable using --without openssl)
%slurm_with_opt openssl

# Use readline by default on all systems
%slurm_with_opt readline

# Build with PAM by default on linux
%ifos linux
%slurm_with_opt pam
%endif

# Define with_aix on AIX systems (for proctrack)
%ifos aix5.3
%slurm_with_opt aix
%endif

# Build with sgijob plugin and mysql (for slurmdbd) on CHAOS systems
%if %{?chaos}0
%slurm_with_opt mysql
%slurm_with_opt lua
%slurm_with_opt partial_attach
%else
%slurm_without_opt sgijob
%slurm_without_opt lua
%slurm_without_opt partial-attach
%endif

%if %{?chaos}0 && 0%{?chaos} < 5
%slurm_with_opt sgijob
%endif

Name:    see META file
Version: see META file
Release: see META file

Summary: Simple Linux Utility for Resource Management

License: GPL
Group: System Environment/Base
Source: %{name}-%{version}-%{release}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}
URL: https://computing.llnl.gov/linux/slurm/

Requires: slurm-plugins

%ifos linux
BuildRequires: python
%endif

%ifos solaris
Requires:	SUNWgnome-base-libs
BuildRequires:	SUNWgnome-base-libs

Requires:	SUNWopenssl
BuildRequires:	SUNWopenssl

BuildRequires:	SUNWaconf
BuildRequires:	SUNWgnu-automake-110
BuildRequires:	SUNWlibtool
BuildRequires:	SUNWgcc
BuildRequires:	SUNWgnome-common-devel
%endif

%if %{?chaos}0
BuildRequires: gtk2-devel >= 2.7.1
BuildRequires: ncurses-devel
BuildRequires: pkgconfig
%endif

# not sure if this is always an actual rpm or not so leaving the requirement out
#%if %{slurm_with blcr}
#BuildRequires: blcr
#%endif

%if %{slurm_with readline}
BuildRequires: readline-devel
%endif

%if %{slurm_with openssl}
BuildRequires: openssl-devel >= 0.9.6 openssl >= 0.9.6
%endif

%if %{slurm_with mysql}
BuildRequires: mysql-devel >= 5.0.0
%endif

%if %{slurm_with postgres}
BuildRequires: postgresql-devel >= 8.0.0
%endif

%ifnos aix5.3
# FIXME: AIX can't seem to find this even though this is in existance there.
# We should probably figure out a better way of doing this, but for now we
# just won't look for it on AIX.
BuildRequires: perl(ExtUtils::MakeMaker)
%endif

%description
SLURM is an open source, fault-tolerant, and highly
scalable cluster management and job scheduling system for Linux clusters
containing up to 65,536 nodes. Components include machine status,
partition management, job management, scheduling and accounting modules.

#  Allow override of sysconfdir via _slurm_sysconfdir.
#  Note 'global' instead of 'define' needed here to work around apparent
#   bug in rpm macro scoping (or something...)
%{!?_slurm_sysconfdir: %global _slurm_sysconfdir /etc/slurm}
%define _sysconfdir %_slurm_sysconfdir

#
# Never allow rpm to strip binaries as this will break
#  parallel debugging capability
#
%define __os_install_post /usr/lib/rpm/brp-compress
%define debug_package %{nil}

#
# Should unpackaged files in a build root terminate a build?
#
# Note: The default value should be 0 for legacy compatibility.
# This was added due to a bug in Suse Linux. For a good reference, see
# http://slforums.typo3-factory.net/index.php?showtopic=11378
%define _unpackaged_files_terminate_build      0

# First we remove $prefix/local and then just prefix to make
# sure we get the correct installdir
%define _perlarch %(perl -e 'use Config; $T=$Config{installsitearch}; $P=$Config{installprefix}; $P1="$P/local"; $T =~ s/$P1//; $T =~ s/$P//; print $T;')

# AIX doesn't always give the correct install prefix here for mans 
%ifos aix5.3
%define _perlman3 %(perl -e 'use Config; $T=$Config{installsiteman3dir}; $P=$Config{siteprefix}; $P1="$P/local"; $T =~ s/$P1//; $T =~ s/$P//; $P="/usr/share"; $T =~ s/$P//; print $T;')
%else
%define _perlman3 %(perl -e 'use Config; $T=$Config{installsiteman3dir}; $P=$Config{siteprefix}; $P1="$P/local"; $T =~ s/$P1//; $T =~ s/$P//; print $T;')
%endif

%define _perlarchlib %(perl -e 'use Config; $T=$Config{installarchlib}; $P=$Config{installprefix}; $P1="$P/local"; $T =~ s/$P1//; $T =~ s/$P//; print $T;')

%define _perldir %{_prefix}%{_perlarch}
%define _perlman3dir %{_prefix}%{_perlman3}
%define _perlarchlibdir %{_prefix}%{_perlarchlib}
%define _php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php5)

%package perlapi
Summary: Perl API to SLURM.
Group: Development/System
Requires: slurm
%description perlapi
Perl API package for SLURM.  This package includes the perl API to provide a
helpful interface to SLURM through Perl.

%package devel
Summary: Development package for SLURM.
Group: Development/System
Requires: slurm
%description devel
Development package for SLURM.  This package includes the header files
and static libraries for the SLURM API.

%if %{slurm_with auth_none}
%package auth-none
Summary: SLURM auth NULL implementation (no authentication)
Group: System Environment/Base
Requires: slurm
%description auth-none
SLURM NULL authentication module
%endif

%if %{slurm_with authd}
%package auth-authd
Summary: SLURM auth implementation using Brent Chun's authd
Group: System Environment/Base
Requires: slurm authd
%description auth-authd
SLURM authentication module for Brent Chun's authd
%endif

# This is named munge instead of auth-munge since there are 2 plugins in the
# package.  auth-munge and crypto-munge
%if %{slurm_with munge}
%package munge
Summary: SLURM authentication and crypto implementation using Munge
Group: System Environment/Base
Requires: slurm munge
BuildRequires: munge-devel munge-libs
Obsoletes: slurm-auth-munge
%description munge
SLURM authentication module for Chris Dunlap's Munge
%endif

%if %{slurm_with bluegene}
%package bluegene
Summary: SLURM interfaces to IBM Blue Gene system
Group: System Environment/Base
Requires: slurm
%description bluegene
SLURM plugin interfaces to IBM Blue Gene system
%endif

%if %{slurm_with elan}
%package switch-elan
Summary: SLURM switch plugin for Quadrics Elan3 or Elan4.
Group: System Environment/Base
Requires: slurm qsnetlibs
BuildRequires: qsnetlibs
%description switch-elan
SLURM switch plugin for Quadrics Elan3 or Elan4.
%endif

%package slurmdbd
Summary: SLURM database daemon
Group: System Environment/Base
Requires: slurm-plugins slurm-sql
%description slurmdbd
SLURM database daemon

%package sql
Summary: SLURM SQL support
Group: System Environment/Base
%description sql
SLURM sql support

%package plugins
Summary: SLURM plugins (loadable shared objects)
Group: System Environment/Base
%description plugins
SLURM plugins (loadable shared objects)

%package torque
Summary: Torque/PBS wrappers for transitition from Torque/PBS to SLURM.
Group: Development/System
Requires: slurm-perlapi
%description torque
Torque wrapper scripts used for helping migrate from Torque/PBS to SLURM.

%if %{slurm_with srun2aprun}
%package srun2aprun
Summary: SLURM srun command is a wrapper for Cray/ALPS aprun command.
Group: Development/System
Requires: slurm-perlapi
%description srun2aprun
SLURM srun command is a wrapper for Cray/ALPS aprun command.
%endif

%package sjobexit
Summary: SLURM job exit code management tools.
Group: Development/System
Requires: slurm-perlapi
%description sjobexit
SLURM job exit code management tools.

%package slurmdb-direct
Summary: Wrappers to write directly to the slurmdb.
Group: Development/System
Requires: slurm-perlapi
%description slurmdb-direct
Wrappers to write directly to the slurmdb.

%if %{slurm_with aix}
%package aix
Summary: SLURM interfaces to IBM AIX and Federation switch.
Group: System Environment/Base
Requires: slurm
BuildRequires: proctrack >= 3
Obsoletes: slurm-aix-federation
%description aix
SLURM plugins for IBM AIX and Federation switch.
%endif

%if %{slurm_with sgijob}
%package proctrack-sgi-job
Summary: SLURM process tracking plugin for SGI job containers.
Group: System Environment/Base
Requires: slurm
BuildRequires: job
%description proctrack-sgi-job
SLURM process tracking plugin for SGI job containers.
(See http://oss.sgi.com/projects/pagg).
%endif

%if %{slurm_with lua}
%package lua
Summary: SLURM lua bindings
Group: System Environment/Base
Requires: slurm lua
BuildRequires: lua-devel
%description lua
SLURM lua bindings
Includes the SLURM proctrack/lua and job_submit/lua plugin
%endif

%package sjstat
Summary: Perl tool to print SLURM job state information.
Group: Development/System
Requires: slurm
%description sjstat
Perl tool to print SLURM job state information.

%if %{slurm_with pam}
%package pam_slurm
Summary: PAM module for restricting access to compute nodes via SLURM.
Group: System Environment/Base
Requires: slurm slurm-devel
BuildRequires: pam-devel
Obsoletes: pam_slurm
%description pam_slurm
This module restricts access to compute nodes in a cluster where the Simple
Linux Utility for Resource Managment (SLURM) is in use.  Access is granted
to root, any user with an SLURM-launched job currently running on the node,
or any user who has allocated resources on the node according to the SLURM
%endif

%if %{slurm_with blcr}
%package blcr
Summary: Allows SLURM to use Berkeley Lab Checkpoint/Restart
Group: System Environment/Base
Requires: slurm
%description blcr
Gives the ability for SLURM to use Berkeley Lab Checkpoint/Restart
%endif

#############################################################################

%prep
%setup -n %{name}-%{version}-%{release}

%build
%configure --program-prefix=%{?_program_prefix:%{_program_prefix}} \
	%{?slurm_with_cray_xt:--enable-cray-xt} \
	%{?slurm_with_debug:--enable-debug} \
	%{?slurm_with_partial_attach:--enable-partial-attach} \
	%{?slurm_with_sun_const:--enable-sun-const} \
	%{?with_db2_dir} \
	%{?with_pam_dir}	\
	%{?with_proctrack}	\
	%{?with_cpusetdir} \
	%{?with_apbasildir} \
	%{?with_xcpu} \
	%{?with_mysql_config} \
	%{?with_pg_config} \
	%{?with_ssl}		\
	%{?with_munge}      \
	%{?with_blcr}      \
	%{!?slurm_with_readline:--without-readline} \
	%{?with_cflags}

make %{?_smp_mflags}

%install
rm -rf "$RPM_BUILD_ROOT"
mkdir -p "$RPM_BUILD_ROOT"
DESTDIR="$RPM_BUILD_ROOT" make install
DESTDIR="$RPM_BUILD_ROOT" make install-contrib

%ifos aix5.3
   mv ${RPM_BUILD_ROOT}%{_bindir}/srun ${RPM_BUILD_ROOT}%{_sbindir}
%else
   if [ -d /etc/init.d ]; then
      install -D -m755 etc/init.d.slurm    $RPM_BUILD_ROOT/etc/init.d/slurm
      install -D -m755 etc/init.d.slurmdbd $RPM_BUILD_ROOT/etc/init.d/slurmdbd
   fi
%endif
install -D -m644 etc/slurm.conf.example ${RPM_BUILD_ROOT}%{_sysconfdir}/slurm.conf.example
install -D -m644 etc/cgroup.conf.example ${RPM_BUILD_ROOT}%{_sysconfdir}/cgroup.conf.example
install -D -m755 etc/cgroup.release_common.example ${RPM_BUILD_ROOT}%{_sysconfdir}/cgroup.release_common.example
install -D -m755 etc/cgroup.release_common.example ${RPM_BUILD_ROOT}%{_sysconfdir}/cgroup/release_freezer
install -D -m755 etc/cgroup.release_common.example ${RPM_BUILD_ROOT}%{_sysconfdir}/cgroup/release_cpuset
install -D -m755 etc/cgroup.release_common.example ${RPM_BUILD_ROOT}%{_sysconfdir}/cgroup/release_memory
install -D -m644 etc/slurmdbd.conf.example ${RPM_BUILD_ROOT}%{_sysconfdir}/slurmdbd.conf.example
install -D -m755 etc/slurm.epilog.clean ${RPM_BUILD_ROOT}%{_sysconfdir}/slurm.epilog.clean
install -D -m755 contribs/sjstat ${RPM_BUILD_ROOT}%{_bindir}/sjstat

# Delete unpackaged files:
rm -f $RPM_BUILD_ROOT/%{_libdir}/libpmi.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/libslurm.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/libslurmdb.a
rm -f $RPM_BUILD_ROOT/%{_libdir}/slurm/*.{a,la}
rm -f $RPM_BUILD_ROOT/%{_libdir}/security/*.{a,la}
%if %{?with_pam_dir}0
rm -f $RPM_BUILD_ROOT/%{with_pam_dir}/pam_slurm.{a,la}
%endif
rm -f $RPM_BUILD_ROOT/lib/security/pam_slurm.{a,la}
rm -f $RPM_BUILD_ROOT/lib32/security/pam_slurm.{a,la}
rm -f $RPM_BUILD_ROOT/lib64/security/pam_slurm.{a,la}
%if ! %{slurm_with auth_none}
rm -f $RPM_BUILD_ROOT/%{_libdir}/slurm/auth_none.so
%endif
%if ! %{slurm_with bluegene}
rm -f $RPM_BUILD_ROOT/%{_libdir}/slurm/job_submit_cnode.so
rm -f $RPM_BUILD_ROOT/%{_libdir}/slurm/libsched_if.so
rm -f $RPM_BUILD_ROOT/%{_libdir}/slurm/libsched_if64.so
rm -f $RPM_BUILD_ROOT/%{_mandir}/man5/bluegene*
rm -f $RPM_BUILD_ROOT/%{_sbindir}/sfree
rm -f $RPM_BUILD_ROOT/%{_sbindir}/slurm_epilog
rm -f $RPM_BUILD_ROOT/%{_sbindir}/slurm_prolog
%endif
%if ! %{slurm_with munge}
rm -f $RPM_BUILD_ROOT/%{_libdir}/slurm/auth_munge.so
rm -f $RPM_BUILD_ROOT/%{_libdir}/slurm/crypto_munge.so
%endif
rm -f $RPM_BUILD_ROOT/%{_perldir}/auto/Slurm/.packlist
rm -f $RPM_BUILD_ROOT/%{_perlarchlibdir}/perllocal.pod
rm -f $RPM_BUILD_ROOT/%{_perldir}/perllocal.pod
rm -f $RPM_BUILD_ROOT/%{_perldir}/auto/Slurmdb/.packlist

%if ! %{slurm_with blcr}
# remove these if they exist
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/srun_cr*
rm -f ${RPM_BUILD_ROOT}%{_bindir}/srun_cr
rm -f ${RPM_BUILD_ROOT}%{_libexecdir}/slurm/cr_*
%endif

# Build man pages that are generated directly by the tools
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/sjobexitmod.1
${RPM_BUILD_ROOT}%{_bindir}/sjobexitmod --roff > $RPM_BUILD_ROOT/%{_mandir}/man1/sjobexitmod.1

# Build conditional file list for main package
LIST=./slurm.files
touch $LIST
test -f $RPM_BUILD_ROOT/etc/init.d/slurm			&&
  echo /etc/init.d/slurm				>> $LIST
test -f $RPM_BUILD_ROOT/%{_bindir}/sview			&&
  echo %{_bindir}/sview					>> $LIST

%if %{slurm_with aix}
install -D -m644 etc/federation.conf.example ${RPM_BUILD_ROOT}%{_sysconfdir}/federation.conf.example
%endif

%if %{slurm_with bluegene}
rm -f ${RPM_BUILD_ROOT}%{_bindir}/srun
install -D -m644 etc/bluegene.conf.example ${RPM_BUILD_ROOT}%{_sysconfdir}/bluegene.conf.example
mkdir -p ${RPM_BUILD_ROOT}/etc/ld.so.conf.d
echo "%{_libdir}/slurm" > ${RPM_BUILD_ROOT}/etc/ld.so.conf.d/slurm.conf
chmod 644 ${RPM_BUILD_ROOT}/etc/ld.so.conf.d/slurm.conf

LIST=./bluegene.files
touch $LIST
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/libsched_if.so &&
   echo %{_libdir}/slurm/libsched_if.so >> $LIST
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/libsched_if64.so &&
   echo %{_libdir}/slurm/libsched_if64.so >> $LIST

%endif

LIST=./aix.files
touch $LIST
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/proctrack_aix.so      &&
  echo %{_libdir}/slurm/proctrack_aix.so               >> $LIST
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/switch_federation.so  &&
  echo %{_libdir}/slurm/switch_federation.so           >> $LIST

LIST=./slurmdbd.files
touch $LIST
test -f $RPM_BUILD_ROOT/etc/init.d/slurm                       &&
  echo /etc/init.d/slurmdbd                            >> $LIST

LIST=./sql.files
touch $LIST
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/accounting_storage_mysql.so &&
   echo %{_libdir}/slurm/accounting_storage_mysql.so >> $LIST
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/accounting_storage_pgsql.so &&
   echo %{_libdir}/slurm/accounting_storage_pgsql.so >> $LIST
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/jobcomp_mysql.so            &&
   echo %{_libdir}/slurm/jobcomp_mysql.so            >> $LIST
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/jobcomp_pgsql.so            &&
   echo %{_libdir}/slurm/jobcomp_pgsql.so            >> $LIST

LIST=./plugins.files
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/select_bluegene.so          &&
   echo %{_libdir}/slurm/select_bluegene.so          >> $LIST
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/crypto_openssl.so           &&
   echo %{_libdir}/slurm/crypto_openssl.so           >> $LIST
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/task_affinity.so            &&
   echo %{_libdir}/slurm/task_affinity.so            >> $LIST
test -f $RPM_BUILD_ROOT/%{_libdir}/slurm/task_cgroup.so              &&
   echo %{_libdir}/slurm/task_cgroup.so              >> $LIST

LIST=./pam.files
touch $LIST
%if %{?with_pam_dir}0
    test -f $RPM_BUILD_ROOT/%{with_pam_dir}/pam_slurm.so	&&
	echo %{with_pam_dir}/pam_slurm.so	>>$LIST
%else
    test -f $RPM_BUILD_ROOT/lib/security/pam_slurm.so		&&
	echo /lib/security/pam_slurm.so		>>$LIST
    test -f $RPM_BUILD_ROOT/lib32/security/pam_slurm.so		&&
	echo /lib32/security/pam_slurm.so	>>$LIST
    test -f $RPM_BUILD_ROOT/lib64/security/pam_slurm.so		&&
	echo /lib64/security/pam_slurm.so	>>$LIST
%endif
#############################################################################

%clean
rm -rf $RPM_BUILD_ROOT
#############################################################################

%files -f slurm.files
%defattr(-,root,root,0755)
%doc AUTHORS
%doc NEWS
%doc README.rst
%doc RELEASE_NOTES
%doc DISCLAIMER
%doc COPYING
%doc doc/html
%{_bindir}/sacct
%{_bindir}/sacctmgr
%{_bindir}/salloc
%{_bindir}/sattach
%{_bindir}/sbatch
%{_bindir}/sbcast
%{_bindir}/scancel
%{_bindir}/scontrol
%{_bindir}/sinfo
%{_bindir}/smap*
%{_bindir}/sprio
%{_bindir}/squeue
%{_bindir}/sreport
%if ! %{slurm_with srun2aprun}
%{_bindir}/srun
%endif
%{_bindir}/sshare
%{_bindir}/sstat
%{_bindir}/strigger
%{_sbindir}/slurmctld
%{_sbindir}/slurmd
%{_sbindir}/slurmstepd
%ifos aix5.3
%{_sbindir}/srun
%endif
%{_libdir}/*.so*
%{_libdir}/slurm/src/*
%{_mandir}/man1/*
%{_mandir}/man5/cgroup.*
%{_mandir}/man5/cray.*
%{_mandir}/man5/gres.*
%{_mandir}/man5/slurm.*
%{_mandir}/man5/topology.*
%{_mandir}/man5/wiki.*
%{_mandir}/man8/slurmctld.*
%{_mandir}/man8/slurmd.*
%{_mandir}/man8/slurmstepd*
%{_mandir}/man8/spank*
%dir %{_sysconfdir}
%dir %{_libdir}/slurm/src
%config %{_sysconfdir}/slurm.conf.example
%config %{_sysconfdir}/cgroup.conf.example
%config %{_sysconfdir}/cgroup.release_common.example
%config (noreplace) %{_sysconfdir}/cgroup/release_freezer
%config (noreplace) %{_sysconfdir}/cgroup/release_cpuset
%config (noreplace) %{_sysconfdir}/cgroup/release_memory
%config %{_sysconfdir}/slurm.epilog.clean
%exclude %{_mandir}/man1/sjobexit*
%if %{slurm_with blcr}
%exclude %{_mandir}/man1/srun_cr*
%exclude %{_bindir}/srun_cr
%endif
#############################################################################

%files devel
%defattr(-,root,root)
%dir %attr(0755,root,root) %{_prefix}/include/slurm
%{_prefix}/include/slurm/*
%{_libdir}/libpmi.la
%{_libdir}/libslurm.la
%{_libdir}/libslurmdb.la
%{_mandir}/man3/slurm_*
#%{_mandir}/man3/slurmdb_*
#############################################################################

%if %{slurm_with auth_none}
%files auth-none
%defattr(-,root,root)
%{_libdir}/slurm/auth_none.so
%endif
#############################################################################

%if %{slurm_with munge}
%files munge
%defattr(-,root,root)
%{_libdir}/slurm/auth_munge.so
%{_libdir}/slurm/crypto_munge.so
%endif
#############################################################################

%if %{slurm_with authd}
%defattr(-,root,root)
%files auth-authd
%{_libdir}/slurm/auth_authd.so
%endif
#############################################################################

%if %{slurm_with bluegene}
%files -f bluegene.files bluegene
%defattr(-,root,root)
%dir /etc/ld.so.conf.d
/etc/ld.so.conf.d/slurm.conf
%{_mandir}/man5/bluegene.*
%{_sbindir}/slurm_epilog
%{_sbindir}/slurm_prolog
%{_sbindir}/sfree
%{_libdir}/slurm/job_submit_cnode.so
%config %{_sysconfdir}/bluegene.conf.example
%endif
#############################################################################

%files perlapi
%defattr(-,root,root)
%{_perldir}/Slurm.pm
%{_perldir}/Slurm/Bitstr.pm
%{_perldir}/Slurm/Constant.pm
%{_perldir}/Slurm/Hostlist.pm
%{_perldir}/Slurm/Stepctx.pm
%{_perldir}/auto/Slurm/Slurm.so
%{_perldir}/auto/Slurm/Slurm.bs
%{_perldir}/Slurmdb.pm
%{_perldir}/auto/Slurmdb/Slurmdb.so
%{_perldir}/auto/Slurmdb/Slurmdb.bs
%{_perldir}/auto/Slurmdb/autosplit.ix
%{_perlman3dir}/Slurm*

#############################################################################

%if %{slurm_with elan}
%files switch-elan
%defattr(-,root,root)
%{_libdir}/slurm/switch_elan.so
%{_libdir}/slurm/proctrack_rms.so
%endif
#############################################################################

%files -f slurmdbd.files slurmdbd
%defattr(-,root,root)
%{_sbindir}/slurmdbd
%{_mandir}/man5/slurmdbd.*
%{_mandir}/man8/slurmdbd.*
%config %{_sysconfdir}/slurmdbd.conf.example
#############################################################################

%files -f sql.files sql
%defattr(-,root,root)
%dir %{_libdir}/slurm
#############################################################################

%files -f plugins.files plugins
%defattr(-,root,root)
%dir %{_libdir}/slurm
%{_libdir}/slurm/accounting_storage_filetxt.so
%{_libdir}/slurm/accounting_storage_none.so
%{_libdir}/slurm/accounting_storage_slurmdbd.so
%{_libdir}/slurm/checkpoint_none.so
%{_libdir}/slurm/checkpoint_ompi.so
%{_libdir}/slurm/gres_gpu.so
%{_libdir}/slurm/gres_nic.so
%{_libdir}/slurm/jobacct_gather_aix.so
%{_libdir}/slurm/jobacct_gather_linux.so
%{_libdir}/slurm/jobacct_gather_none.so
%{_libdir}/slurm/jobcomp_none.so
%{_libdir}/slurm/jobcomp_filetxt.so
%{_libdir}/slurm/jobcomp_script.so
%{_libdir}/slurm/job_submit_defaults.so
%{_libdir}/slurm/job_submit_logging.so
%{_libdir}/slurm/job_submit_partition.so
%{_libdir}/slurm/mpi_lam.so
%{_libdir}/slurm/mpi_mpich1_p4.so
%{_libdir}/slurm/mpi_mpich1_shmem.so
%{_libdir}/slurm/mpi_mpichgm.so
%{_libdir}/slurm/mpi_mpichmx.so
%{_libdir}/slurm/mpi_mvapich.so
%{_libdir}/slurm/mpi_none.so
%{_libdir}/slurm/mpi_openmpi.so
%{_libdir}/slurm/preempt_none.so
%{_libdir}/slurm/preempt_partition_prio.so
%{_libdir}/slurm/preempt_qos.so
%{_libdir}/slurm/priority_basic.so
%{_libdir}/slurm/priority_multifactor.so
%{_libdir}/slurm/proctrack_cgroup.so
%{_libdir}/slurm/proctrack_pgid.so
%{_libdir}/slurm/proctrack_linuxproc.so
%{_libdir}/slurm/sched_backfill.so
%{_libdir}/slurm/sched_builtin.so
%{_libdir}/slurm/sched_hold.so
%{_libdir}/slurm/sched_wiki.so
%{_libdir}/slurm/sched_wiki2.so
%{_libdir}/slurm/select_cray.so
%{_libdir}/slurm/select_cons_res.so
%{_libdir}/slurm/select_linear.so
%{_libdir}/slurm/switch_none.so
%{_libdir}/slurm/task_none.so
%{_libdir}/slurm/topology_3d_torus.so
%{_libdir}/slurm/topology_node_rank.so
%{_libdir}/slurm/topology_none.so
%{_libdir}/slurm/topology_tree.so
#############################################################################

%files torque
%defattr(-,root,root)
%{_bindir}/pbsnodes
%{_bindir}/qdel
%{_bindir}/qhold
%{_bindir}/qrls
%{_bindir}/qstat
%{_bindir}/qsub
%{_bindir}/mpiexec
#############################################################################

%if %{slurm_with srun2aprun}
%files srun2aprun

%defattr(-,root,root)
%{_bindir}/srun
%endif
#############################################################################

%files sjobexit
%defattr(-,root,root)
%{_bindir}/sjobexitmod
%{_mandir}/man1/sjobexit*
#############################################################################

%files slurmdb-direct
%defattr(-,root,root)
%config (noreplace) %{_perldir}/config.slurmdb.pl
%{_sbindir}/moab_2_slurmdb
#############################################################################

%if %{slurm_with aix}
%files -f aix.files aix
%defattr(-,root,root)
%{_libdir}/slurm/checkpoint_aix.so
%config %{_sysconfdir}/federation.conf.example
%endif
#############################################################################

%if %{slurm_with sgijob}
%files proctrack-sgi-job
%defattr(-,root,root)
%{_libdir}/slurm/proctrack_sgi_job.so
%endif
#############################################################################

%if %{slurm_with lua}
%files lua
%defattr(-,root,root)
%doc contribs/lua/proctrack.lua
%{_libdir}/slurm/job_submit_lua.so
%{_libdir}/slurm/proctrack_lua.so
%endif
#############################################################################

%files sjstat
%defattr(-,root,root)
%{_bindir}/sjstat
#############################################################################

%if %{slurm_with pam}
%files -f pam.files pam_slurm
%defattr(-,root,root)
%endif
#############################################################################

%if %{slurm_with blcr}
%files blcr
%defattr(-,root,root)
%{_bindir}/srun_cr
%{_libexecdir}/slurm/cr_*
%{_libdir}/slurm/checkpoint_blcr.so
%{_mandir}/man1/srun_cr*
%endif
#############################################################################

%pre
#if [ -x /etc/init.d/slurm ]; then
#    if /etc/init.d/slurm status | grep -q running; then
#        /etc/init.d/slurm stop
#    fi
#fi
#if [ -x /etc/init.d/slurmdbd ]; then
#    if /etc/init.d/slurmdbd status | grep -q running; then
#        /etc/init.d/slurmdbd stop
#    fi
#fi

%post
if [ -x /sbin/ldconfig ]; then
    /sbin/ldconfig %{_libdir}
    if [ $1 = 1 ]; then
	[ -x /sbin/chkconfig ] && /sbin/chkconfig --add slurm
    fi
fi
if [ ! -f %{_sysconfdir}/slurm.conf ]; then
    echo "You need to build and install a slurm.conf file"
    echo "Edit %{_sysconfdir}/slurm.conf.example and copy it to slurm.conf or"
    echo "Build a new one using http://www.llnl.gov/linux/slurm/configurator.html"
fi

%post slurmdbd
if [ ! -f %{_sysconfdir}/slurmdbd.conf ]; then
    echo "You need to build and install a slurmdbd.conf file"
    echo "Edit %{_sysconfdir}/slurmdbd.conf.example and copy it to slurmdbd.conf"
fi

%if %{slurm_with bluegene}
%post bluegene
if [ -x /sbin/ldconfig ]; then
    /sbin/ldconfig %{_libdir}/slurm
fi
if [ ! -f %{_sysconfdir}/bluegene.conf ]; then
    echo "You need to build and install a bluegene.conf file"
    echo "Edit %{_sysconfdir}/bluegene.conf.example and copy it to bluegene.conf"
fi
%endif

%preun
if [ "$1" = 0 ]; then
    if [ -x /etc/init.d/slurm ]; then
	[ -x /sbin/chkconfig ] && /sbin/chkconfig --del slurm
	if /etc/init.d/slurm status | grep -q running; then
	    /etc/init.d/slurm stop
	fi
    fi
fi

%preun slurmdbd
if [ "$1" = 0 ]; then
    if [ -x /etc/init.d/slurmdbd ]; then
	[ -x /sbin/chkconfig ] && /sbin/chkconfig --del slurmdbd
	if /etc/init.d/slurmdbd status | grep -q running; then
	    /etc/init.d/slurmdbd stop
	fi
    fi
fi

%postun
if [ "$1" = 0 ]; then
    if [ -x /sbin/ldconfig ]; then
	/sbin/ldconfig %{_libdir}
    fi
fi
#############################################################################


%changelog
* Tue Feb 14 2006 Morris Jette <jette1@llnl.gov>
- See the NEWS file for update details
