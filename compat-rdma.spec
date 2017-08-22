#
# Copyright (c) 2012 Mellanox Technologies. All rights reserved.
#
# This Software is licensed under one of the following licenses:
#
# 1) under the terms of the "Common Public License 1.0" a copy of which is
#    available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/cpl.php.
#
# 2) under the terms of the "The BSD License" a copy of which is
#    available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/bsd-license.php.
#
# 3) under the terms of the "GNU General Public License (GPL) Version 2" a
#    copy of which is available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/gpl-license.php.
#
# Licensee has the right to choose one of the above licenses.
#
# Redistributions of source code must retain the above copyright
# notice and one of the license notices.
#
# Redistributions in binary form must reproduce both the above copyright
# notice, one of the license notices in the documentation
# and/or other materials provided with the distribution.
#
#

%{!?configure_options: %define configure_options %{nil}}

%{!?KVERSION: %define KVERSION %(uname -r)}
%define krelver %(echo -n %{KVERSION} | sed -e 's/-/_/g')

%global WITH_SYSTEMD %(if ( test -d "/lib/systemd/system" > /dev/null || test -d "%{_prefix}/lib/systemd/system" > /dev/null); then echo -n '1'; else echo -n '0'; fi)

# Select packages to build
# Kernel module packages to be included into compat-rdma

%define build_mthca %(if ( echo %{configure_options} | grep "with-mthca-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_qib %(if ( echo %{configure_options} | grep "with-qib-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_ipath %(if ( echo %{configure_options} | grep "with-ipath_inf-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_ehca %(if ( echo %{configure_options} | grep "with-ehca-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_ipoib %(if ( echo %{configure_options} | grep "with-ipoib-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_srp %(if ( echo %{configure_options} | grep "with-srp-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_srpt %(if ( echo %{configure_options} | grep "with-srp-target-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_iser %(if ( echo %{configure_options} | grep "with-iser-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_oiscsi %(if ( echo %{configure_options} | grep "with-iscsi-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_rds %(if ( echo %{configure_options} | grep "with-rds-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_cxgb3 %(if ( echo %{configure_options} | grep "with-cxgb3-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_cxgb4 %(if ( echo %{configure_options} | grep "with-cxgb4-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_nes %(if ( echo %{configure_options} | grep "with-nes-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_mlx4 %(if ( echo %{configure_options} | grep "with-mlx4-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_mlx5 %(if ( echo %{configure_options} | grep "with-mlx5-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_mlx4_en %(if ( echo %{configure_options} | grep "with-mlx4_en-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_qlgc_vnic %(if ( echo %{configure_options} | grep "with-qlgc_vnic-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_nfsrdma %(if ( echo %{configure_options} | grep "with-nfsrdma-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_ocrdma %(if ( echo %{configure_options} | grep "with-ocrdma-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_ibp_server %(if ( echo %{configure_options} | grep "with-ibp-server-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_ibscif %(if ( echo %{configure_options} | grep "with-ibscif-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_vmw_pvrdma %(if ( echo %{configure_options} | grep "with-vmw_pvrdma-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_qedr %(if ( echo %{configure_options} | grep "with-qedr-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_bnxt_re %(if ( echo %{configure_options} | grep "with-bnxt_re-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_compat_rdma_firmware %(if ( echo %{configure_options} | grep "with-firmware" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)

%{!?LIB_MOD_DIR: %define LIB_MOD_DIR /lib/modules/%{KVERSION}/updates}

%{!?RDMA_CONF_DIR: %define RDMA_CONF_DIR /etc/infiniband}
%{!?MLXNET_CONF_DIR: %define MLXNET_CONF_DIR /etc/mlxethernet}

%{!?K_SRC: %define K_SRC /lib/modules/%{KVERSION}/source}
%{!?K_SRC_OBJ: %define K_SRC_OBJ /lib/modules/%{KVERSION}/build}

%{!?KERNEL_SOURCES: %define KERNEL_SOURCES /lib/modules/%{KVERSION}/source}

# Disable debugging
%define debug_package %{nil}
%define __check_files %{nil}

# Disable brp-lib64-linux
%ifarch x86_64 ia64
%define __arch_install_post %{nil}
%endif

%{!?_name: %define _name compat-rdma}
%{!?_version: %define _version @VERSION@}
%{!?_release: %define _release @RELEASE@}

Name: %{_name}
Version: %{_version}
Release: %{_release}
License: GPLv2
Url: http://openfabrics.org/
Group: System Environment/Base
Source: %{_name}-%{_version}.tgz
Vendor: OpenFabrics
Requires: coreutils
Requires: kernel
Requires: pciutils
Requires: grep
Requires: perl
Requires: procps
Requires: module-init-tools
Requires: lsof
%if %{build_ibscif}
BuildRequires: /lib/modules/%{KVERSION}/scif.symvers
%endif
Summary: Infiniband Driver and ULPs kernel modules
%description
InfiniBand "verbs", Access Layer  and ULPs

%package -n compat-rdma-devel
Requires: coreutils
Requires: kernel
Requires: pciutils
Requires: compat-rdma
Version: %{_version}
Release: %{_release}
Summary: Infiniband Driver and ULPs kernel modules sources
Group: System Environment/Libraries
%description -n compat-rdma-devel
Core, HW and ULPs kernel modules sources

%prep
%setup -n %{_name}-%{_version}

%build
rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/%{_name}-%{_version}

# Save clean sources for compat-rdma-devel
mkdir -p $RPM_BUILD_DIR/src
cp -a $RPM_BUILD_DIR/%{_name}-%{_version} $RPM_BUILD_DIR/src/

./configure --prefix=%{_prefix} --kernel-version %{KVERSION} --with-linux %{K_SRC} --with-linux-obj %{K_SRC_OBJ} --modules-dir %{LIB_MOD_DIR} %{configure_options}

# Copy InfniBand include files after applying backport patches (if required)
mkdir -p $RPM_BUILD_DIR/src/%{_name}
cp -a $RPM_BUILD_DIR/%{_name}-%{_version}/include/ $RPM_BUILD_DIR/src/%{_name}
cp -a $RPM_BUILD_DIR/%{_name}-%{_version}/config*  $RPM_BUILD_DIR/src/%{_name}
cp -a $RPM_BUILD_DIR/%{_name}-%{_version}/compat*  $RPM_BUILD_DIR/src/%{_name}
cp -a $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts*  $RPM_BUILD_DIR/src/%{_name}
sed -i -e "s@\${CWD}@%{_prefix}/src/%{_name}@g" $RPM_BUILD_DIR/src/%{_name}/config.mk

%if %{build_ibp_server} || %{build_ibscif} || %{build_qib}
  %{!?scif_symvers: %define scif_symvers %(echo -n '/lib/modules/%{KVERSION}/scif.symvers')}
  test -f %{scif_symvers} && cat %{scif_symvers} >> ./Module.symvers
%endif

%if %{build_srpt}
if [ -f /usr/local/include/scst/Module.symvers ]; then
	cat /usr/local/include/scst/Module.symvers >> ./Module.symvers
fi
%endif
export INSTALL_MOD_DIR=updates
make %{?_smp_mflags} kernel

%install
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/src
cp -a $RPM_BUILD_DIR/src/%{_name}-%{_version} $RPM_BUILD_ROOT/%{_prefix}/src
cp -a $RPM_BUILD_DIR/src/%{_name} $RPM_BUILD_ROOT/%{_prefix}/src
rm -rf $RPM_BUILD_DIR/src

# Support external modules include dir for backward compatibility
cd $RPM_BUILD_ROOT/%{_prefix}/src/
ln -s %{_name} openib
cd -

make install_kernel MODULES_DIR=%{LIB_MOD_DIR} INSTALL_MOD_PATH=$RPM_BUILD_ROOT INSTALL_MOD_DIR=updates KERNELRELEASE=%{KVERSION}
cp -a compat.config $RPM_BUILD_ROOT/%{_prefix}/src/%{_name}
cp -a include/linux/compat_autoconf.h $RPM_BUILD_ROOT/%{_prefix}/src/%{_name}/include/linux

modsyms=`find $RPM_BUILD_DIR/%{_name}-%{_version} -name Module.symvers -o -name Modules.symvers`
if [ -n "$modsyms" ]; then
	for modsym in $modsyms
	do
	        cat $modsym >> $RPM_BUILD_ROOT/%{_prefix}/src/%{_name}/Module.symvers
	done
else
	./ofed_scripts/create_Module.symvers.sh
	cp ./Module.symvers $RPM_BUILD_ROOT/%{_prefix}/src/%{_name}/Module.symvers
fi
	
INFO=${RPM_BUILD_ROOT}%{RDMA_CONF_DIR}/info
/bin/rm -f ${INFO}
mkdir -p ${RPM_BUILD_ROOT}%{RDMA_CONF_DIR}
touch ${INFO}

cat >> ${INFO} << EOFINFO
#!/bin/bash

echo prefix=%{_prefix}
echo Kernel=%{KVERSION}
echo
echo "Configure options: %{configure_options}"
echo
EOFINFO

chmod +x ${INFO} > /dev/null 2>&1

%if "%{WITH_SYSTEMD}" == "1"
install -d $RPM_BUILD_ROOT/%{_prefix}/lib/systemd/system
install -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/openibd.service $RPM_BUILD_ROOT/%{_prefix}/lib/systemd/system
%endif

# Copy infiniband configuration
install -d $RPM_BUILD_ROOT/%{RDMA_CONF_DIR}
install -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/openib.conf $RPM_BUILD_ROOT/%{RDMA_CONF_DIR}
cat $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/openib.conf.tmp >> $RPM_BUILD_ROOT/%{RDMA_CONF_DIR}/openib.conf

# Install openib service script
install -d $RPM_BUILD_ROOT/etc/init.d
install -m 0755 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/openibd $RPM_BUILD_ROOT/etc/init.d

%if %{build_ibp_server} || %{build_ibscif}
# Also install ofed-mic script in init.d
install -m 0755 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/ofed-mic $RPM_BUILD_ROOT/etc/init.d
%endif

install -d $RPM_BUILD_ROOT/sbin
install -m 0755 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/sysctl_perf_tuning $RPM_BUILD_ROOT/sbin

%if %{build_mlx4} || %{build_mlx5}
install -d $RPM_BUILD_ROOT/%{_bindir}
install -m 0755 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/ibdev2netdev $RPM_BUILD_ROOT/%{_bindir}
%endif

%if %{build_mlx4_en}
install -d $RPM_BUILD_ROOT/sbin
install -m 0755 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/connectx_port_config $RPM_BUILD_ROOT/sbin
touch $RPM_BUILD_ROOT/%{RDMA_CONF_DIR}/connectx.conf
%endif

%if %{build_ibp_server} || %{build_ibscif}
install -d $RPM_BUILD_ROOT/etc/modprobe.d
install -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/ibscif.conf $RPM_BUILD_ROOT/etc/modprobe.d/
install -d $RPM_BUILD_ROOT/usr/sbin
install -m 0755 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/ibscif-opt $RPM_BUILD_ROOT/usr/sbin
%endif

%if %{build_qib}
install -m 0755 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/truescale.cmds $RPM_BUILD_ROOT/%{RDMA_CONF_DIR}
%endif

%if %{build_ipoib}
install -d $RPM_BUILD_ROOT/etc/modprobe.d
install -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/ib_ipoib.conf $RPM_BUILD_ROOT/etc/modprobe.d
%if %{build_ibp_server} || %{build_ibscif}
install -d $RPM_BUILD_ROOT/etc/sysconfig/mic
install -D -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/ipoib.conf $RPM_BUILD_ROOT/etc/mpss/ipoib.conf
install -D -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/docs/lustre-phi.txt $RPM_BUILD_ROOT/usr/share/doc/%{_name}-%{_version}/lustre-phi.txt
%endif
%endif

%if %{build_compat_rdma_firmware}
%if %{build_qedr}
install -D -m 0755 $RPM_BUILD_DIR/%{_name}-%{_version}/linux-firmware/qed/* /lib/firmware/qed/
%endif
%endif

install -d $RPM_BUILD_ROOT/etc/udev/rules.d
install -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/90-ib.rules $RPM_BUILD_ROOT/etc/udev/rules.d

%clean
rm -rf %{buildroot}

%pre

%pre -n compat-rdma-devel

%post
if [ $1 -ge 1 ]; then # 1 : This package is being installed or reinstalled
    /sbin/depmod %{KVERSION}

if [[ -f /etc/redhat-release || -f /etc/rocks-release ]]; then        
perl -i -ne 'if (m@^#!/bin/bash@) {
        print q@#!/bin/bash
#
# Bring up/down openib
#
# chkconfig: 2345 05 95
# description: Activates/Deactivates InfiniBand Driver to \
#              start at boot time.
#
### BEGIN INIT INFO
# Provides:       openibd
### END INIT INFO
@;
                 } else {
                     print;
                 }' /etc/init.d/openibd

        /sbin/chkconfig openibd off >/dev/null 2>&1 || true
        /usr/bin/systemctl disable openibd >/dev/null  2>&1 || true
        /sbin/chkconfig --del openibd >/dev/null 2>&1 || true

        /sbin/chkconfig --add openibd >/dev/null 2>&1 || true
        /sbin/chkconfig openibd on >/dev/null 2>&1 || true
        /usr/bin/systemctl enable openibd >/dev/null  2>&1 || true

        if [ -x /etc/init.d/ofed-mic ]; then
            if ! ( /sbin/chkconfig --del ofed-mic > /dev/null 2>&1 ); then
                    true
            fi
            if ! ( /sbin/chkconfig --add ofed-mic && /sbin/chkconfig ofed-mic off > /dev/null 2>&1 ); then
                    true
            fi
        fi
fi

if [ -f /etc/SuSE-release ]; then
    local_fs='$local_fs'
    openiscsi=''
    %if %{build_oiscsi}
        openiscsi='open-iscsi'
    %endif
        perl -i -ne "if (m@^#!/bin/bash@) {
        print q@#!/bin/bash
### BEGIN INIT INFO
# Provides:       openibd
# Required-Start: $local_fs
# Required-Stop: opensmd $openiscsi
# Default-Start:  2 3 5
# Default-Stop: 0 1 2 6
# Description:    Activates/Deactivates InfiniBand Driver to \
#                 start at boot time.
### END INIT INFO
@;
                 } else {
                     print;
                 }" /etc/init.d/openibd

        /sbin/chkconfig openibd off >/dev/null  2>&1 || true
        /usr/bin/systemctl disable openibd >/dev/null  2>&1 || true
        /sbin/insserv -r openibd >/dev/null 2>&1 || true

        /sbin/insserv openibd >/dev/null 2>&1 || true
        /sbin/chkconfig openibd on >/dev/null 2>&1 || true
        /usr/bin/systemctl enable openibd >/dev/null  2>&1 || true
fi

if [ -f /etc/debian_version ]; then
    local_fs='$local_fs'
    openiscsi=''
    %if %{build_oiscsi}
        openiscsi='open-iscsi'
    %endif
        perl -i -ne "if (m@^#!/bin/bash@) {
        print q@#!/bin/bash
### BEGIN INIT INFO
# Provides:       openibd
# Required-Start: $local_fs
# Required-Stop: opensmd $openiscsi
# Default-Start:  2 3 5
# Default-Stop: 0 1 2 6
# Description:    Activates/Deactivates InfiniBand Driver to \
#                 start at boot time.
### END INIT INFO
@;
                 } else {
                     print;
                 }" /etc/init.d/openibd

        if ! ( /usr/sbin/update-rc.d openibd defaults > /dev/null 2>&1 ); then
                true
        fi
fi

%if "%{WITH_SYSTEMD}" == "1"
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

fi # 1 : closed
# END of post

%post -n compat-rdma-devel

%preun
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
          if [[ -f /etc/redhat-release || -f /etc/rocks-release ]]; then        
                /sbin/chkconfig openibd off >/dev/null 2>&1 || true
                /usr/bin/systemctl disable openibd >/dev/null  2>&1 || true
                /sbin/chkconfig --del openibd  >/dev/null 2>&1 || true
		if [ -x /etc/init.d/ofed-mic ]; then
                    if ! ( /sbin/chkconfig --del ofed-mic  > /dev/null 2>&1 ); then
                        true
                    fi
		fi
          fi
          if [ -f /etc/SuSE-release ]; then
                /sbin/chkconfig openibd off >/dev/null 2>&1 || true
                /usr/bin/systemctl disable openibd >/dev/null  2>&1 || true
                /sbin/insserv -r openibd >/dev/null 2>&1 || true
		if [ -x /etc/init.d/ofed-mic ]; then
                    if ! ( /sbin/insserv -r ofed-mic > /dev/null 2>&1 ); then
                        true
                    fi
                fi
          fi
          if [ -f /etc/debian_version ]; then
                if ! ( /usr/sbin/update-rc.d openibd remove > /dev/null 2>&1 ); then
                        true
                fi
          fi
fi

%postun
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
        # Clean /etc/modprobe.d/ofed.conf   
        # Remove previous configuration if exist
        /sbin/depmod %{KVERSION}
%if "%{WITH_SYSTEMD}" == "1"
/usr/bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif
fi

%postun -n compat-rdma-devel

%files
%defattr(-,root,root,-)
%dir %{RDMA_CONF_DIR}
%config(noreplace) %{RDMA_CONF_DIR}/openib.conf
%if %{build_ibp_server} || %{build_ibscif}
%config %{_sysconfdir}/init.d/ofed-mic
%endif
%{RDMA_CONF_DIR}/info
/etc/init.d/openibd
%if "%{WITH_SYSTEMD}" == "1"
%{_prefix}/lib/systemd/system/openibd.service
%endif
/sbin/sysctl_perf_tuning
/etc/udev/rules.d/90-ib.rules
%{LIB_MOD_DIR}
%if %{build_qib}
%config(noreplace) %{RDMA_CONF_DIR}/truescale.cmds
%endif
%if %{build_ibp_server} || %{build_ibscif}
%config(noreplace) %{_sysconfdir}/modprobe.d/ibscif.conf
%endif
%if %{build_ipoib}
/etc/modprobe.d/ib_ipoib.conf
%if %{build_ibp_server} || %{build_ibscif}
%config(noreplace) %{_sysconfdir}/mpss/ipoib.conf
/usr/share/doc/%{_name}-%{_version}/lustre-phi.txt
%endif
%endif
%if %{build_mlx4} || %{build_mlx5}
%{_bindir}/ibdev2netdev
%endif
%if %{build_mlx4_en}
/sbin/connectx_port_config
%config(noreplace) %{RDMA_CONF_DIR}/connectx.conf
%endif

%files -n compat-rdma-devel
%defattr(-,root,root,-)
%dir %{_prefix}/src
%{_prefix}/src/%{_name}-%{_version}
%{_prefix}/src/%{_name}
%{_prefix}/src/openib

%changelog
* Thu Feb 16 2012 Vladimir Sokolovsky <vlad@mellanox.com>
- Created spec file for compat-rdma
