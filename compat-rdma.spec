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

# %{!?MEMTRACK: %define MEMTRACK 0}
%define MEMTRACK %(if ( echo %{configure_options} | grep "with-memtrack" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define MADEYE %(if ( echo %{configure_options} | grep "with-madeye-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)

%{!?KVERSION: %define KVERSION %(uname -r)}
%define krelver %(echo -n %{KVERSION} | sed -e 's/-/_/g')

%{!?build_kernel_ib: %define build_kernel_ib 0}
%{!?build_kernel_ib_devel: %define build_kernel_ib_devel 0}

# Set default to use scif.h and scif symvers from MPSS installation
# Use the release-3.x paths
%{!?scif_h: %define scif_h %(echo -n '/usr/src/kernels/%{KVERSION}/include/modules/scif.h')}
%{!?scif_symvers: %define scif_symvers %(echo -n '/lib/modules/%{KVERSION}/scif.symvers')}

# Select packages to build
%{!?modprobe_update: %define modprobe_update %(if ( echo %{configure_options} | grep "without-modprobe" > /dev/null ); then echo -n '0'; else echo -n '1'; fi)}

# Kernel module packages to be included into compat-rdma
%define build_mthca %(if ( echo %{configure_options} | grep "with-mthca-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_qib %(if ( echo %{configure_options} | grep "with-qib-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_ipath %(if ( echo %{configure_options} | grep "with-ipath_inf-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_ehca %(if ( echo %{configure_options} | grep "with-ehca-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_ipoib %(if ( echo %{configure_options} | grep "with-ipoib-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%define build_sdp %(if ( echo %{configure_options} | grep "with-sdp-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
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

%{!?LIB_MOD_DIR: %define LIB_MOD_DIR /lib/modules/%{KVERSION}/updates}

%{!?RDMA_CONF_DIR: %define RDMA_CONF_DIR /etc/infiniband}
%{!?MLXNET_CONF_DIR: %define MLXNET_CONF_DIR /etc/mlxethernet}

%{!?K_SRC: %define K_SRC /lib/modules/%{KVERSION}/build}

%{!?KERNEL_SOURCES: %define KERNEL_SOURCES /lib/modules/%{KVERSION}/source}

# Do not include srp.h if it exist in the kernel
%define include_srp_h %(if [ -e %{KERNEL_SOURCES}/include/scsi/srp.h ]; then echo -n 0; else echo -n 1; fi )
%define include_rdma %(if [ -d %{KERNEL_SOURCES}/include/rdma ]; then echo -n 1; else echo -n 0; fi )

%define include_udev_rules %(eval `grep udev_rules /etc/udev/udev.conf | grep -v '^#'` ; if test -d $udev_rules; then echo -n 1; else echo -n 0; fi)

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
License: GPL/BSD
Url: http://openfabrics.org/
Group: System Environment/Base
Source: %{_name}-%{_version}.tgz
BuildRoot: %{?build_root:%{build_root}}%{!?build_root:/var/tmp/OFED}
Vendor: OpenFabrics
Requires: coreutils
Requires: kernel
Requires: pciutils
Requires: grep
Requires: perl
Requires: procps
Requires: module-init-tools
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

%if %{build_kernel_ib_devel}
# Save clean sources for compat-rdma-devel
mkdir -p $RPM_BUILD_DIR/src
cp -a $RPM_BUILD_DIR/%{_name}-%{_version} $RPM_BUILD_DIR/src/
%endif

./configure --prefix=%{_prefix} --kernel-version %{KVERSION} --kernel-sources %{K_SRC} --modules-dir %{LIB_MOD_DIR} %{configure_options}

%if %{build_kernel_ib_devel}
# Copy InfniBand include files after applying backport patches (if required)
mkdir -p $RPM_BUILD_DIR/src/%{_name}
cp -a $RPM_BUILD_DIR/%{_name}-%{_version}/include/ $RPM_BUILD_DIR/src/%{_name}
cp -a $RPM_BUILD_DIR/%{_name}-%{_version}/configure.mk.kernel $RPM_BUILD_DIR/src/%{_name}
cp -a $RPM_BUILD_DIR/%{_name}-%{_version}/config.mk  $RPM_BUILD_DIR/src/%{_name}
sed -i -e "s@\${CWD}@%{_prefix}/src/%{_name}@g" $RPM_BUILD_DIR/src/%{_name}/config.mk
%endif


%if %{build_kernel_ib}
%if %{build_ibp_server} || %{build_ibscif} || %{build_qib}
test ! -d ./include/modules && mkdir ./include/modules
test -f %{scif_h} && cp %{scif_h} ./include/modules
test -f %{scif_symvers} && cat %{scif_symvers} >> ./Module.symvers
%endif
%if %{build_srpt}
if [ -f /usr/local/include/scst/Module.symvers ]; then
	cat /usr/local/include/scst/Module.symvers >> ./Module.symvers
fi
%endif
export INSTALL_MOD_DIR=updates
make kernel
%endif

%install
%if %{build_kernel_ib_devel}
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/src
cp -a $RPM_BUILD_DIR/src/%{_name}-%{_version} $RPM_BUILD_ROOT/%{_prefix}/src
cp -a $RPM_BUILD_DIR/src/%{_name} $RPM_BUILD_ROOT/%{_prefix}/src
rm -rf $RPM_BUILD_DIR/src

# Support external modules include dir for backward compatibility
cd $RPM_BUILD_ROOT/%{_prefix}/src/
ln -s %{_name} openib
cd -
%endif

%if %{build_kernel_ib}
make install_kernel MODULES_DIR=%{LIB_MOD_DIR} INSTALL_MOD_PATH=$RPM_BUILD_ROOT INSTALL_MOD_DIR=updates KERNELRELEASE=%{KVERSION}
cp -a compat.config $RPM_BUILD_ROOT/%{_prefix}/src/%{_name}
cp -a include/linux/compat_autoconf.h $RPM_BUILD_ROOT/%{_prefix}/src/%{_name}/include/linux
%endif

%if %{build_kernel_ib_devel}
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
%endif
	
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

# Copy infiniband configuration
install -d $RPM_BUILD_ROOT/%{RDMA_CONF_DIR}
install -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/openib.conf $RPM_BUILD_ROOT/%{RDMA_CONF_DIR}

%if %{build_ibp_server} || %{build_ibscif}
# install overlay files and config
install -D -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/ofed.conf $RPM_BUILD_ROOT/etc/mpss/conf.d/ofed.conf
install -D -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/ofed.filelist $RPM_BUILD_ROOT/opt/intel/mic/ofed/ofed.filelist
%endif

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
install -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/truescale.cmds $RPM_BUILD_ROOT/%{RDMA_CONF_DIR}
%endif

%if %{build_ipoib}
%if %{modprobe_update}
install -d $RPM_BUILD_ROOT/etc/modprobe.d
install -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/ib_ipoib.conf $RPM_BUILD_ROOT/etc/modprobe.d
%endif
%if %{build_ibp_server} || %{build_ibscif}
install -d $RPM_BUILD_ROOT/etc/sysconfig/mic
install -D -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/ipoib.conf $RPM_BUILD_ROOT/etc/mpss/ipoib.conf
install -D -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/docs/lustre-phi.txt $RPM_BUILD_ROOT/usr/share/doc/%{_name}-%{_version}/lustre-phi.txt
%endif
%endif

%if %{build_sdp}
%if %{modprobe_update}
install -d $RPM_BUILD_ROOT/etc/modprobe.d
install -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/ib_sdp.conf $RPM_BUILD_ROOT/etc/modprobe.d
%endif
%endif

%if %{include_udev_rules}
install -d $RPM_BUILD_ROOT/etc/udev/rules.d
install -m 0644 $RPM_BUILD_DIR/%{_name}-%{_version}/ofed_scripts/90-ib.rules $RPM_BUILD_ROOT/etc/udev/rules.d
case "$(udevinfo -V 2> /dev/null | awk '{print $NF}' 2> /dev/null)" in
0[1-4]*)
sed -i -e 's/KERNEL==/KERNEL=/g'  $RPM_BUILD_ROOT/etc/udev/rules.d/90-ib.rules
;;
esac
%endif
	
%clean
#Remove installed driver after rpm build finished
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{_name}-%{_version}

%pre

%pre -n compat-rdma-devel

%post
if [ $1 -ge 1 ]; then # 1 : This package is being installed or reinstalled
count_ib_ports()
{
    local cnt=0
    local tmp_cnt=0
    
    tmp_cnt=$(/sbin/lspci -n | grep "15b3:" | wc -l | tr -d '[:space:]') # Mellanox HCAs
    cnt=$[ $cnt + 2*${tmp_cnt} ]
    
    tmp_cnt=$(/sbin/lspci -n | grep -E "1fc1:|1077:7220" | wc -l | tr -d '[:space:]') # QLogic SDR and DDR HCA
    cnt=$[ $cnt + ${tmp_cnt} ]
    
    tmp_cnt=$(/sbin/lspci -n | grep -E "1077:7322" | wc -l | tr -d '[:space:]') # QLogic QDR HCA
    cnt=$[ $cnt + 2*${tmp_cnt} ]
    return $cnt
}

count_ib_ports
ports_num=$?

# Set default number of ports to 2 if no HCAs found
if [ $ports_num -eq 0 ]; then
    ports_num=2
fi    
#############################################################################################################
#                                       Modules configuration                                               #
#############################################################################################################

%if ! %{include_udev_rules}
    if [ -e /etc/udev/udev.rules ]; then
        perl -ni -e 'if (/\# Infiniband devices \#$/) { $filter = 1 }' -e 'if (!$filter) { print }' -e 'if (/\# End Infiniband devices \#$/){ $filter = 0 }' /etc/udev/udev.rules
        cat >> /etc/udev/udev.rules << EOF
# Infiniband devices #
KERNEL="umad*", NAME="infiniband/%k"
KERNEL="issm*", NAME="infiniband/%k"
KERNEL="ucm*", NAME="infiniband/%k", MODE="0666"
KERNEL="uverbs*", NAME="infiniband/%k", MODE="0666"
KERNEL="uat", NAME="infiniband/%k", MODE="0666"
KERNEL="ucma", NAME="infiniband/%k", MODE="0666"
KERNEL="rdma_cm", NAME="infiniband/%k", MODE="0666"
# End Infiniband devices #
EOF
    fi
%endif

%if %{modprobe_update}
%if %{build_ipoib}
for (( i=0 ; i < $ports_num ; i++ ))
do
cat >> /etc/modprobe.d/ib_ipoib.conf << EOF
alias ib${i} ib_ipoib
EOF
done
%endif
%endif

    /sbin/depmod %{KVERSION}

#############################################################################################################


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

        if ! ( /sbin/chkconfig --del openibd > /dev/null 2>&1 ); then
                true
        fi
        if ! ( /sbin/chkconfig --add openibd > /dev/null 2>&1 ); then
                true
        fi

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
# Required-Stop: $local_fs
# Default-Start:  2 3 5
# Default-Stop: 0 1 4 6
# Description:    Activates/Deactivates InfiniBand Driver to \
#                 start at boot time.
### END INIT INFO
@;
                 } else {
                     print;
                 }" /etc/init.d/openibd

        if ! ( /sbin/insserv openibd > /dev/null 2>&1 ); then
                true
        fi
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
# Required-Stop: $local_fs
# Default-Start:  2 3 4 5
# Default-Stop: 0 1 6
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

%if %{build_kernel_ib}
    echo >> %{RDMA_CONF_DIR}/openib.conf
    echo "# Load UCM module" >> %{RDMA_CONF_DIR}/openib.conf
    echo "UCM_LOAD=no" >> %{RDMA_CONF_DIR}/openib.conf
    echo >> %{RDMA_CONF_DIR}/openib.conf
    echo "# Load RDMA_CM module" >> %{RDMA_CONF_DIR}/openib.conf
    echo "RDMA_CM_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
    echo >> %{RDMA_CONF_DIR}/openib.conf
    echo "# Load RDMA_UCM module" >> %{RDMA_CONF_DIR}/openib.conf
    echo "RDMA_UCM_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
    echo >> %{RDMA_CONF_DIR}/openib.conf
    echo "# Increase ib_mad thread priority" >> %{RDMA_CONF_DIR}/openib.conf
    echo "RENICE_IB_MAD=no" >> %{RDMA_CONF_DIR}/openib.conf
    echo >> %{RDMA_CONF_DIR}/openib.conf
    echo "# Run sysctl performance tuning script" >> %{RDMA_CONF_DIR}/openib.conf
    echo "RUN_SYSCTL=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_mthca}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load MTHCA" >> %{RDMA_CONF_DIR}/openib.conf
       echo "MTHCA_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_qib}
       echo >> %{RDMA_CONF_DIR}/openib.conf
       echo "# Load QIB" >> %{RDMA_CONF_DIR}/openib.conf
       echo "QIB_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
       echo "# QIB QME BP VER" >> %{RDMA_CONF_DIR}/openib.conf
       echo "QIB_QME_BPVER=1" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_ipath}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load IPATH" >> %{RDMA_CONF_DIR}/openib.conf
       echo "IPATH_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_ehca}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load eHCA" >> %{RDMA_CONF_DIR}/openib.conf
       echo "EHCA_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_mlx4}
       echo >> %{RDMA_CONF_DIR}/openib.conf
       echo "# Load MLX4 modules" >> %{RDMA_CONF_DIR}/openib.conf
       echo "MLX4_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_mlx5}
       echo >> %{RDMA_CONF_DIR}/openib.conf
       echo "# Load MLX5 modules" >> %{RDMA_CONF_DIR}/openib.conf
       echo "MLX5_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_mlx4_en}
       echo >> %{RDMA_CONF_DIR}/openib.conf
       echo "# Load MLX4_EN module" >> %{RDMA_CONF_DIR}/openib.conf
       echo "MLX4_EN_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_cxgb3}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load CXGB3 modules" >> %{RDMA_CONF_DIR}/openib.conf
       echo "CXGB3_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_cxgb4}
       echo >> %{RDMA_CONF_DIR}/openib.conf
       echo "# Load CXGB4 modules" >> %{RDMA_CONF_DIR}/openib.conf
       echo "CXGB4_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_nes}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load NES modules" >> %{RDMA_CONF_DIR}/openib.conf
       echo "NES_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_ipoib}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load IPoIB" >> %{RDMA_CONF_DIR}/openib.conf
       echo "IPOIB_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Enable IPoIB Connected Mode" >> %{RDMA_CONF_DIR}/openib.conf
       echo "SET_IPOIB_CM=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_sdp}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load SDP module" >> %{RDMA_CONF_DIR}/openib.conf
       echo "SDP_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_srp}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load SRP module" >> %{RDMA_CONF_DIR}/openib.conf
       echo "SRP_LOAD=no" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_srpt}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load SRP Target module" >> %{RDMA_CONF_DIR}/openib.conf
       echo "SRPT_LOAD=no" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_iser}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load ISER module" >> %{RDMA_CONF_DIR}/openib.conf
       echo "ISER_LOAD=no" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_rds}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load RDS module" >> %{RDMA_CONF_DIR}/openib.conf
       echo "RDS_LOAD=no" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_qlgc_vnic}
       echo >> %{RDMA_CONF_DIR}/openib.conf
       echo "# Load QLogic VNIC module" >> %{RDMA_CONF_DIR}/openib.conf
       echo "QLGC_VNIC_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

%if %{build_ocrdma}
       echo >> %{RDMA_CONF_DIR}/openib.conf                                                
       echo "# Load OCRDMA modules" >> %{RDMA_CONF_DIR}/openib.conf
       echo "OCRDMA_LOAD=yes" >> %{RDMA_CONF_DIR}/openib.conf
%endif

fi # 1 : closed
# END of post

%post -n compat-rdma-devel

%preun
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
          if [[ -f /etc/redhat-release || -f /etc/rocks-release ]]; then        
                if ! ( /sbin/chkconfig --del openibd  > /dev/null 2>&1 ); then
                        true
                fi
		if [ -x /etc/init.d/ofed-mic ]; then
                    if ! ( /sbin/chkconfig --del ofed-mic  > /dev/null 2>&1 ); then
                        true
                    fi
		fi
          fi
          if [ -f /etc/SuSE-release ]; then
                if ! ( /sbin/insserv -r openibd > /dev/null 2>&1 ); then
                        true
                fi
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

# Clean udev.rules
%if ! %{include_udev_rules}
    if [ -e /etc/udev/udev.rules ]; then
        perl -ni -e 'if (/\# Infiniband devices \#$/) { $filter = 1 }' -e 'if (!$filter) { print }' -e 'if (/\# End Infiniband devices \#$/){ $filter = 0 }' /etc/udev/udev.rules
    fi
%endif

# Clean sysctl.conf
if [ -f /etc/sysctl.conf ]; then
perl -ni -e 'if (/\#\# OFED Network tuning parameters \#\#$/) { $filter = 1 }' -e 'if (!$filter) { print }' -e 'if (/\#\# END of OFED parameters \#\#$/){ $filter = 0 }' /etc/sysctl.conf
fi

fi

%postun -n compat-rdma-devel

%files
%defattr(-,root,root,-)
%dir %{RDMA_CONF_DIR}
%config(noreplace) %{RDMA_CONF_DIR}/openib.conf
%if %{build_ibp_server} || %{build_ibscif}
%config %{_sysconfdir}/init.d/ofed-mic
%config %{_sysconfdir}/mpss/conf.d/ofed.conf
%dir /opt/intel/mic/ofed
/opt/intel/mic/ofed/*
%endif
%{RDMA_CONF_DIR}/info
/etc/init.d/openibd
/sbin/sysctl_perf_tuning
%if %{include_udev_rules}
/etc/udev/rules.d/90-ib.rules
%endif
%{LIB_MOD_DIR}
%if %{build_qib}
%config(noreplace) %{RDMA_CONF_DIR}/truescale.cmds
%endif
%if %{build_ibp_server} || %{build_ibscif}
%if %{modprobe_update}
%config(noreplace) %{_sysconfdir}/modprobe.d/ibscif.conf
%endif
%endif
%if %{build_ipoib}
%if %{modprobe_update}
/etc/modprobe.d/ib_ipoib.conf
%endif
%if %{build_ibp_server} || %{build_ibscif}
%config(noreplace) %{_sysconfdir}/mpss/ipoib.conf
/usr/share/doc/%{_name}-%{_version}/lustre-phi.txt
%endif
%endif
%if %{build_sdp}
%if %{modprobe_update}
/etc/modprobe.d/ib_sdp.conf
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
