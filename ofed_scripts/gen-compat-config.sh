#!/bin/bash
# Copyright 2013        Mellanox Technologies. All rights reserved.
# Copyright 2012        Luis R. Rodriguez <mcgrof@frijolero.org>
# Copyright 2012        Hauke Mehrtens <hauke@hauke-m.de>
#
# This generates a bunch of CONFIG_COMPAT_KERNEL_2_6_22
# CONFIG_COMPAT_KERNEL_3_0 .. etc for each kernel release you need an object
# for.
#
# Note: this is part of the compat.git project, not compat-drivers,
# send patches against compat.git.

if [[ ! -f ${KLIB_BUILD}/Makefile ]]; then
	exit
fi

KERNEL_VERSION=$(${MAKE} -C ${KLIB_BUILD} kernelversion | sed -n 's/^\([0-9]\)\..*/\1/p')

# 3.0 kernel stuff
COMPAT_LATEST_VERSION="11"
KERNEL_SUBLEVEL="-1"

function set_config {
	VAR=$1
	VALUE=$2

	eval "export $VAR=$VALUE"
	echo "export $VAR=$VALUE"
}
# Note that this script will export all variables explicitly,
# trying to export all with a blanket "export" statement at
# the top of the generated file causes the build to slow down
# by an order of magnitude.

if [[ ${KERNEL_VERSION} -eq "3" ]]; then
	KERNEL_SUBLEVEL=$(${MAKE} -C ${KLIB_BUILD} kernelversion | sed -n 's/^3\.\([0-9]\+\).*/\1/p')
else
	COMPAT_26LATEST_VERSION="39"
	KERNEL_26SUBLEVEL=$(${MAKE} -C ${KLIB_BUILD} kernelversion | sed -n 's/^2\.6\.\([0-9]\+\).*/\1/p')
	let KERNEL_26SUBLEVEL=${KERNEL_26SUBLEVEL}+1

	for i in $(seq ${KERNEL_26SUBLEVEL} ${COMPAT_26LATEST_VERSION}); do
		set_config CONFIG_COMPAT_KERNEL_2_6_${i} y
	done
fi

let KERNEL_SUBLEVEL=${KERNEL_SUBLEVEL}+1
for i in $(seq ${KERNEL_SUBLEVEL} ${COMPAT_LATEST_VERSION}); do
	set_config CONFIG_COMPAT_KERNEL_3_${i} y
done

# The purpose of these seem to be the inverse of the above other varibales.
# The RHEL checks seem to annotate the existance of RHEL minor versions.
RHEL_MAJOR=$(grep ^RHEL_MAJOR ${KLIB_BUILD}/Makefile | sed -n 's/.*= *\(.*\)/\1/p')
if [[ ! -z ${RHEL_MAJOR} ]]; then
	RHEL_MINOR=$(grep ^RHEL_MINOR ${KLIB_BUILD}/Makefile | sed -n 's/.*= *\(.*\)/\1/p')
	for i in $(seq 0 ${RHEL_MINOR}); do
		set_config CONFIG_COMPAT_RHEL_${RHEL_MAJOR}_${i} y
	done
fi

if [[ ${CONFIG_COMPAT_KERNEL_2_6_33} = "y" ]]; then
	if [[ ! ${CONFIG_COMPAT_RHEL_6_0} = "y" ]]; then
		set_config CONFIG_COMPAT_FIRMWARE_CLASS m
	fi
fi

if [[ ${CONFIG_COMPAT_KERNEL_2_6_36} = "y" ]]; then
	if [[ ! ${CONFIG_COMPAT_RHEL_6_1} = "y" ]]; then
		set_config CONFIG_COMPAT_KFIFO y
	fi
fi

if [[ ${CONFIG_COMPAT_KERNEL_3_2} = "y" ]]; then
	set_config CONFIG_COMPAT_USE_LRO y
fi

SLES_11_3_KERNEL=$(echo ${KVERSION} | sed -n 's/^\(3\.0\.76\+\)\-\(.*\)\-\(.*\)/\1-\2-\3/p')
if [[ ! -z ${SLES_11_3_KERNEL} ]]; then
	SLES_MAJOR="11"
	SLES_MINOR="3"
	set_config CONFIG_COMPAT_SLES_11_3 y
fi

SLES_11_2_KERNEL=$(echo ${KVERSION} | sed -n 's/^\(3\.0\.[0-9]\+\)\-\(.*\)\-\(.*\)/\1-\2-\3/p')
if [[ ! -z ${SLES_11_2_KERNEL} ]]; then
	SLES_MAJOR="11"
	SLES_MINOR="2"
	set_config CONFIG_COMPAT_SLES_11_2 y
fi

SLES_11_1_KERNEL=$(echo ${KVERSION} | sed -n 's/^\(2\.6\.32\.[0-9]\+\)\-\(.*\)\-\(.*\)/\1-\2-\3/p')
if [[ ! -z ${SLES_11_1_KERNEL} ]]; then
	SLES_MAJOR="11"
	SLES_MINOR="1"
	set_config CONFIG_COMPAT_SLES_11_1 y
fi

FC14_KERNEL=$(echo ${KVERSION} | grep fc14)
if [[ ! -z ${FC14_KERNEL} ]]; then
 # CONFIG_COMPAT_DISABLE_DCB should be set to 'y' as it used in drivers/net/ethernet/mellanox/mlx4/Makefile
	set_config CONFIG_COMPAT_DISABLE_DCB y
fi

FC16_KERNEL=$(echo ${KVERSION} | grep fc16)
if [[ ! -z ${FC16_KERNEL} ]]; then
	set_config CONFIG_COMPAT_EN_SYSFS y
fi

UBUNTU12=$(uname -a | grep Ubuntu | grep 3\.2)
if [[ ! -z ${UBUNTU12} ]]; then
	set_config CONFIG_COMPAT_EN_SYSFS y
	set_config CONFIG_COMPAT_ISER_ATTR_IS_VISIBLE y
fi

UEK_1_KERNEL=$(echo ${KVERSION} | grep uek | grep 2.6.32)
if [[ ! -z ${UEK_1_KERNEL} ]]; then
	set_config CONFIG_COMPAT_IS_BITMAP y
fi

UEK_2_KERNEL=$(echo ${KVERSION} | grep uek | grep 2.6.39)
if [[ ! -z ${UEK_2_KERNEL} ]]; then
	set_config CONFIG_COMPAT_DST_NEIGHBOUR y
	set_config CONFIG_COMPAT_NETDEV_FEATURES y
fi

if [[ ${CONFIG_COMPAT_KERNEL_2_6_38} = "y" ]]; then
	if [[ ! ${CONFIG_COMPAT_RHEL_6_3} = "y" ]]; then
		set_config CONFIG_COMPAT_NO_PRINTK_NEEDED y
	fi
fi

if [[ ${CONFIG_COMPAT_SLES_11_1} = "y" ]]; then
	set_config CONFIG_COMPAT_DISABLE_DCB y
	set_config CONFIG_COMPAT_UNDO_I6_PRINT_GIDS y
	set_config CONFIG_COMPAT_ISCSI_TRANSPORT_PARAM_MASK y
	set_config CONFIG_COMPAT_DISABLE_VA_FORMAT_PRINT y
	set_config CONFIG_COMPAT_DISABLE_REAL_NUM_TXQ y
fi

if [[ ${CONFIG_COMPAT_SLES_11_2} = "y" ]]; then
	set_config CONFIG_COMPAT_MIN_DUMP_ALLOC_ARG y
	set_config CONFIG_COMPAT_IS_NUM_TX_QUEUES y
	set_config CONFIG_COMPAT_NEW_TX_RING_SCHEME y
	set_config CONFIG_COMPAT_IS___SKB_TX_HASH y
	set_config CONFIG_COMPAT_ISER_ATTR_IS_VISIBLE y
	set_config CONFIG_COMPAT_ISCSI_ISER_GET_EP_PARAM y
	set_config CONFIG_COMPAT_IF_ISCSI_SCSI_REQ y
	set_config CONFIG_COMPAT_EN_SYSFS y
fi

if [[ ${CONFIG_COMPAT_SLES_11_3} = "y" ]]; then
	set_config CONFIG_COMPAT_SCSI_TARGET_UNBLOCK y
fi

if (grep -q dst_set_neighbour ${KLIB_BUILD}/include/net/dst.h > /dev/null 2>&1 || grep -q dst_set_neighbour /lib/modules/${KVERSION}/source/include/net/dst.h > /dev/null 2>&1); then
	set_config CONFIG_COMPAT_DST_NEIGHBOUR y
fi

if (grep -q eth_hw_addr_random ${KLIB_BUILD}/include/linux/etherdevice.h > /dev/null 2>&1 || grep -q eth_hw_addr_random /lib/modules/${KVERSION}/source/include/linux/etherdevice.h > /dev/null 2>&1); then
	set_config CONFIG_COMPAT_ETH_HW_ADDR_RANDOM y
fi

if (grep -q dev_hw_addr_random ${KLIB_BUILD}/include/linux/etherdevice.h > /dev/null 2>&1 || grep -q dev_hw_addr_random /lib/modules/${KVERSION}/source/include/linux/etherdevice.h > /dev/null 2>&1); then
	set_config CONFIG_COMPAT_DEV_HW_ADDR_RANDOM y
fi

if (grep -q "typedef u64 netdev_features_t" ${KLIB_BUILD}/include/linux/netdevice.h > /dev/null 2>&1 || grep -q "typedef u64 netdev_features_t" /lib/modules/${KVERSION}/source/include/linux/netdevice.h > /dev/null 2>&1); then
	set_config CONFIG_COMPAT_NETDEV_FEATURES y
fi

if (grep -qw "WORK_BUSY_PENDING" ${KLIB_BUILD}/include/linux/workqueue.h > /dev/null 2>&1 || grep -qw "WORK_BUSY_PENDING" /lib/modules/${KVERSION}/source/include/linux/workqueue.h > /dev/null 2>&1); then
	set_config CONFIG_COMPAT_IS_WORK_BUSY y
fi

if (grep -qw ieee_getmaxrate ${KLIB_BUILD}/include/net/dcbnl.h > /dev/null 2>&1 || grep -qw ieee_getmaxrate /lib/modules/${KVERSION}/source/include/net/dcbnl.h > /dev/null 2>&1); then
	set_config CONFIG_COMPAT_IS_MAXRATE y
fi

if (grep -qw "netdev_extended" ${KLIB_BUILD}/include/linux/netdevice.h > /dev/null 2>&1 || grep -qw "netdev_extended" /lib/modules/${KVERSION}/source/include/linux/netdevice.h > /dev/null 2>&1); then
	set_config CONFIG_COMPAT_IS_NETDEV_EXTENDED y
fi

if [[ -f ${KLIB_BUILD}/include/linux/cpu_rmap.h || -f /lib/modules/${KVERSION}/source/include/linux/cpu_rmap.h ]]; then
	set_config CONFIG_COMPAT_IS_LINUX_CPU_RMAP y
fi

if (grep -w -A6 "struct ethtool_flow_ext" ${KLIB_BUILD}/include/{,uapi}/linux/ethtool.h 2> /dev/null | grep -wq "unsigned char   h_dest" > /dev/null 2>&1 || grep -q -A6 "struct ethtool_flow_ext" /lib/modules/${KVERSION}/source/include/{,uapi}/linux/ethtool.h 2> /dev/null | grep -wq "unsigned char   h_dest" > /dev/null 2>&1); then
	set_config CONFIG_COMPAT_ETHTOOL_FLOW_EXT_IS_H_DEST y
fi

if [[ ${CONFIG_COMPAT_RHEL_6_3} = "y" ]]; then
	set_config CONFIG_COMPAT_XPRT_ALLOC_4PARAMS y
	set_config CONFIG_COMPAT_XPRT_RESERVE_XPRT_CONG_2PARAMS y
	set_config CONFIG_COMPAT_FRAGS_SKB y
fi

if [[ ${CONFIG_COMPAT_RHEL_6_4} = "y" ]]; then
	set_config CONFIG_COMPAT_IS_PHYS_ID_STATE y
	set_config CONFIG_COMPAT_IS_PCI_PHYSFN y
	set_config CONFIG_COMPAT_IS_KSTRTOX y
	set_config CONFIG_COMPAT_IS_BITOP y
	set_config CONFIG_COMPAT_NETLINK_3_7 y
	set_config CONFIG_COMPAT_IS_IP_TOS2PRIO y
	set_config CONFIG_COMPAT_RCU y
	set_config CONFIG_COMPAT_HAS_NUM_CHANNELS y
	set_config CONFIG_COMPAT_ETHTOOL_OPS_EXT y
fi

if [[ ${RHEL_MAJOR} -eq "6" ]]; then
	set_config CONFIG_COMPAT_IS___SKB_TX_HASH y
	set_config CONFIG_COMPAT_IS_BITMAP y
	set_config CONFIG_COMPAT_DEFINE_NUM_LRO y
	set_config CONFIG_COMPAT_NDO_VF_MAC_VLAN y
	set_config CONFIG_COMPAT_EN_SYSFS y
	set_config CONFIG_COMPAT_LOOPBACK y
	set_config CONFIG_COMPAT_XPRTRDMA_NEEDED y

	if [[ ${RHEL_MINOR} -ne "1" ]]; then
		set_config CONFIG_COMPAT_ISER_ATTR_IS_VISIBLE y
		set_config CONFIG_COMPAT_ISCSI_ISER_GET_EP_PARAM y
		set_config CONFIG_COMPAT_IS_NUM_TX_QUEUES y
		set_config CONFIG_COMPAT_IS_PRIO_TC_MAP y
		set_config CONFIG_COMPAT_NEW_TX_RING_SCHEME y
		set_config CONFIG_COMPAT_NETIF_F_RXHASH y
	fi
fi

if (grep -q virtqueue_get_buf ${KLIB_BUILD}/include/linux/virtio.h > /dev/null 2>&1 || grep -q virtqueue_get_buf /lib/modules/${KVERSION}/source/include/linux/virtio.h > /dev/null 2>&1); then
	set_config CONFIG_COMPAT_VIRTQUEUE_GET_BUF y
fi

if (grep -q virtqueue_add_buf ${KLIB_BUILD}/include/linux/virtio.h > /dev/null 2>&1 || grep -q virtqueue_add_buf /lib/modules/${KVERSION}/source/include/linux/virtio.h > /dev/null 2>&1); then
	set_config CONFIG_COMPAT_VIRTQUEUE_ADD_BUF y
fi

if (grep -q virtqueue_kick ${KLIB_BUILD}/include/linux/virtio.h > /dev/null 2>&1 || grep -q virtqueue_kick /lib/modules/${KVERSION}/source/include/linux/virtio.h > /dev/null 2>&1); then
	set_config CONFIG_COMPAT_VIRTQUEUE_KICK y
fi

if (grep -q zc_request ${KLIB_BUILD}/include/net/9p/transport.h > /dev/null 2>&1 || grep -q zc_request /lib/modules/${KVERSION}/source/include/net/9p/transport.h > /dev/null 2>&1); then
        set_config CONFIG_COMPAT_ZC_REQUEST y
fi

if (grep -q gfp_t ${KLIB_BUILD}/tools/include/virtio/linux/virtio.h > /dev/null 2>&1 || grep -q gfp_t /lib/modules/${KVERSION}/source/include/linux/virtio.h > /dev/null 2>&1); then
        set_config CONFIG_COMPAT_GFP_T y
fi

if (grep -q virtqueue_add_buf_gfp ${KLIB_BUILD}/tools/include/virtio/linux/virtio.h > /dev/null 2>&1 || grep -q virtqueue_add_buf_gfp /lib/modules/${KVERSION}/source/include/linux/virtio.h > /dev/null 2>&1); then
        set_config CONFIG_COMPAT_VIRTQUEUE_ADD_BUF_GFP y
fi
