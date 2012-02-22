# $Id: Makefile 9120 2006-08-28 13:01:07Z vlad $

PHONY += all kernel install_kernel install clean clean_kernel
	
all:
.PHONY: $(PHONY)

.DELETE_ON_ERROR:

include ./configure.mk.kernel
include ./config.mk

DEPMOD  = /sbin/depmod
INSTALL_MOD_DIR ?= updates

ifeq ($(CONFIG_MEMTRACK),m)
        export KERNEL_MEMTRACK_CFLAGS = -include $(CWD)/drivers/infiniband/debug/mtrack.h
else
        export KERNEL_MEMTRACK_CFLAGS =
endif

export OPEN_ISCSI_MODULES = iscsi_tcp.ko libiscsi.ko scsi_transport_iscsi.ko

configure.mk.kernel:
	@echo Please run ./configure
	@exit 1

all: kernel

install: install_kernel
install_kernel: install_modules

autoconf_h=$(shell /bin/ls -1 $(KSRC)/include/*/autoconf.h | head -1)

V ?= 1

#########################
#	make kernel	#
#########################
#NB: The LINUXINCLUDE value comes from main kernel Makefile
#    with local directories prepended. This eventually affects
#    CPPFLAGS in the kernel Makefile
kernel:
	@echo "Building kernel modules"
	@echo "Kernel version: $(KVERSION)"
	@echo "Modules directory: $(INSTALL_MOD_PATH)/$(MODULES_DIR)"
	@echo "Kernel sources: $(KSRC)"
	env CWD=$(CWD) BACKPORT_INCLUDES=$(BACKPORT_INCLUDES) \
		$(MAKE) -C $(KSRC) SUBDIRS="$(CWD)" \
		V=$(V) $(WITH_MAKE_PARAMS) \
		CONFIG_MEMTRACK=$(CONFIG_MEMTRACK) \
		CONFIG_DEBUG_INFO=$(CONFIG_DEBUG_INFO) \
		CONFIG_INFINIBAND=$(CONFIG_INFINIBAND) \
		CONFIG_INFINIBAND_IPOIB=$(CONFIG_INFINIBAND_IPOIB) \
		CONFIG_INFINIBAND_IPOIB_CM=$(CONFIG_INFINIBAND_IPOIB_CM) \
		CONFIG_INFINIBAND_SDP=$(CONFIG_INFINIBAND_SDP) \
		CONFIG_INFINIBAND_SRP=$(CONFIG_INFINIBAND_SRP) \
		CONFIG_INFINIBAND_SRPT=$(CONFIG_INFINIBAND_SRPT) \
		CONFIG_INFINIBAND_USER_MAD=$(CONFIG_INFINIBAND_USER_MAD) \
		CONFIG_INFINIBAND_USER_ACCESS=$(CONFIG_INFINIBAND_USER_ACCESS) \
		CONFIG_INFINIBAND_USER_MEM=$(CONFIG_INFINIBAND_USER_MEM) \
		CONFIG_INFINIBAND_ADDR_TRANS=$(CONFIG_INFINIBAND_ADDR_TRANS) \
		CONFIG_INFINIBAND_MTHCA=$(CONFIG_INFINIBAND_MTHCA) \
		CONFIG_INFINIBAND_IPOIB_DEBUG=$(CONFIG_INFINIBAND_IPOIB_DEBUG) \
		CONFIG_INFINIBAND_ISER=$(CONFIG_INFINIBAND_ISER) \
		CONFIG_SCSI_ISCSI_ATTRS=$(CONFIG_SCSI_ISCSI_ATTRS) \
		CONFIG_ISCSI_TCP=$(CONFIG_ISCSI_TCP) \
		CONFIG_INFINIBAND_EHCA=$(CONFIG_INFINIBAND_EHCA) \
		CONFIG_INFINIBAND_EHCA_SCALING=$(CONFIG_INFINIBAND_EHCA_SCALING) \
		CONFIG_RDS=$(CONFIG_RDS) \
		CONFIG_RDS_RDMA=$(CONFIG_RDS_RDMA) \
		CONFIG_RDS_TCP=$(CONFIG_RDS_TCP) \
		CONFIG_RDS_DEBUG=$(CONFIG_RDS_DEBUG) \
		CONFIG_INFINIBAND_IPOIB_DEBUG_DATA=$(CONFIG_INFINIBAND_IPOIB_DEBUG_DATA) \
		CONFIG_INFINIBAND_SDP_SEND_ZCOPY=$(CONFIG_INFINIBAND_SDP_SEND_ZCOPY) \
		CONFIG_INFINIBAND_SDP_RECV_ZCOPY=$(CONFIG_INFINIBAND_SDP_RECV_ZCOPY) \
		CONFIG_INFINIBAND_SDP_DEBUG=$(CONFIG_INFINIBAND_SDP_DEBUG) \
		CONFIG_INFINIBAND_SDP_DEBUG_DATA=$(CONFIG_INFINIBAND_SDP_DEBUG_DATA) \
		CONFIG_INFINIBAND_IPATH=$(CONFIG_INFINIBAND_IPATH) \
		CONFIG_INFINIBAND_QIB=$(CONFIG_INFINIBAND_QIB) \
		CONFIG_INFINIBAND_MTHCA_DEBUG=$(CONFIG_INFINIBAND_MTHCA_DEBUG) \
		CONFIG_INFINIBAND_MADEYE=$(CONFIG_INFINIBAND_MADEYE) \
		CONFIG_INFINIBAND_QLGC_VNIC=$(CONFIG_INFINIBAND_QLGC_VNIC) \
		CONFIG_INFINIBAND_QLGC_VNIC_DEBUG=$(CONFIG_INFINIBAND_QLGC_VNIC_DEBUG) \
		CONFIG_INFINIBAND_QLGC_VNIC_STATS=$(CONFIG_INFINIBAND_QLGC_VNIC_STATS) \
		CONFIG_CHELSIO_T3=$(CONFIG_CHELSIO_T3) \
		CONFIG_INFINIBAND_CXGB3=$(CONFIG_INFINIBAND_CXGB3) \
		CONFIG_INFINIBAND_CXGB3_DEBUG=$(CONFIG_INFINIBAND_CXGB3_DEBUG) \
		CONFIG_CHELSIO_T4=$(CONFIG_CHELSIO_T4) \
		CONFIG_INFINIBAND_CXGB4=$(CONFIG_INFINIBAND_CXGB4) \
		CONFIG_INFINIBAND_NES=$(CONFIG_INFINIBAND_NES) \
		CONFIG_INFINIBAND_NES_DEBUG=$(CONFIG_INFINIBAND_NES_DEBUG) \
		CONFIG_MLX4_CORE=$(CONFIG_MLX4_CORE) \
		CONFIG_MLX4_EN=$(CONFIG_MLX4_EN) \
		CONFIG_MLX4_INFINIBAND=$(CONFIG_MLX4_INFINIBAND) \
		CONFIG_MLX4_ETHERNET=$(CONFIG_MLX4_ETHERNET) \
		CONFIG_MLX4_DEBUG=$(CONFIG_MLX4_DEBUG) \
		CONFIG_INFINIBAND_AMSO1100=$(CONFIG_INFINIBAND_AMSO1100) \
		CONFIG_SUNRPC_XPRT_RDMA=$(CONFIG_SUNRPC_XPRT_RDMA) \
		CONFIG_NFSD_RDMA=$(CONFIG_NFSD_RDMA) \
		LINUXINCLUDE=' \
		-D__OFED_BUILD__ \
		-include $(autoconf_h) \
		-include $(CWD)/include/linux/autoconf.h \
		$(BACKPORT_INCLUDES) \
		$(KERNEL_MEMTRACK_CFLAGS) \
		$(KERNEL_NFS_FS_CFLAGS) \
		$(OPENIB_KERNEL_EXTRA_CFLAGS) \
		-I$(CWD)/include \
		-I$(CWD)/drivers/infiniband/debug \
		-I/usr/local/include/scst \
		-I$(CWD)/drivers/infiniband/ulp/srpt \
		$$(if $$(CONFIG_XEN),-D__XEN_INTERFACE_VERSION__=$$(CONFIG_XEN_INTERFACE_VERSION)) \
		$$(if $$(CONFIG_XEN),-I$$(srctree)/arch/x86/include/mach-xen) \
		-I$$(srctree)/arch/$$(hdr-arch)/include \
		-Iinclude \
		$$(if $$(KBUILD_SRC),-Iinclude2 -I$$(srctree)/include) \
		-I$$(srctree)/arch/$$(SRCARCH)/include \
		' \
		modules


#########################
#	Install kernel	#
#########################
install_modules:
	@echo "Installing kernel modules"

	$(MAKE) -C $(KSRC) SUBDIRS="$(CWD)" \
		INSTALL_MOD_PATH=$(INSTALL_MOD_PATH) \
		INSTALL_MOD_DIR=$(INSTALL_MOD_DIR) \
		$(WITH_MAKE_PARAMS) modules_install;
	if [ ! -n "$(INSTALL_MOD_PATH)" ]; then $(DEPMOD) $(KVERSION);fi;

clean: clean_kernel

clean_kernel:
	$(MAKE) -C $(KSRC) SUBDIRS="$(CWD)" $(WITH_MAKE_PARAMS) clean

help:
	@echo
	@echo kernel: 		        build kernel modules
	@echo all: 		        build kernel modules
	@echo
	@echo install_kernel:	        install kernel modules under $(INSTALL_MOD_PATH)/$(MODULES_DIR)
	@echo install:	        	run install_kernel
	@echo
	@echo clean:	        	delete kernel modules binaries
	@echo clean_kernel:	        delete kernel modules binaries
	@echo
