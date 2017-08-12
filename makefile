PHONY += all kernel install_kernel install clean clean_kernel
	
all:
.PHONY: $(PHONY)

.DELETE_ON_ERROR:

include ./configure.mk.kernel

export COMPAT_CONFIG=$(CWD)/compat.config
export COMPAT_AUTOCONF=$(CWD)/include/linux/compat_autoconf.h
export KLIB_BUILD
export KVERSION
export MAKE

-include $(COMPAT_CONFIG)

export CREL=$(shell cat $(CWD)/compat_version)
export CREL_PRE:=.compat_autoconf_
export CREL_CHECK:=$(CREL_PRE)$(CREL)
CFLAGS += \
	-DCOMPAT_BASE="\"$(shell cat compat_base)\"" \
	-DCOMPAT_BASE_TREE="\"$(shell cat compat_base_tree)\"" \
	-DCOMPAT_BASE_TREE_VERSION="\"$(shell cat compat_base_tree_version)\"" \
	-DCOMPAT_PROJECT="\"Compat-rdma\"" \
	-DCOMPAT_VERSION="\"$(shell cat compat_version)\"" \

DEPMOD  = /sbin/depmod
INSTALL_MOD_DIR ?= updates

ifeq ($(CONFIG_MEMTRACK),m)
        export KERNEL_MEMTRACK_CFLAGS = -include $(CWD)/drivers/infiniband/debug/mtrack.h
else
        export KERNEL_MEMTRACK_CFLAGS =
endif

export OPEN_ISCSI_MODULES = iscsi_tcp.ko libiscsi.ko scsi_transport_iscsi.ko

$(COMPAT_AUTOCONF): $(COMPAT_CONFIG)
	+@$(CWD)/ofed_scripts/gen-compat-autoconf.sh $(COMPAT_CONFIG) > $(COMPAT_AUTOCONF)

$(COMPAT_CONFIG):
	+@$(CWD)/ofed_scripts/gen-compat-config.sh > $(COMPAT_CONFIG)

configure.mk.kernel:
	@echo Please run ./configure
	@exit 1

all: kernel

install: install_kernel
install_kernel: install_modules

autoconf_h=$(shell /bin/ls -1 $(KSRC_OBJ)/include/*/autoconf.h 2> /dev/null | head -1)
kconfig_h=$(shell /bin/ls -1 $(KSRC)/include/*/kconfig.h 2> /dev/null | head -1)

ifneq ($(kconfig_h),)
KCONFIG_H = -include $(kconfig_h)
endif

V ?= 0

#########################
#	make kernel	#
#########################
#NB: The LINUXINCLUDE value comes from main kernel Makefile
#    with local directories prepended. This eventually affects
#    CPPFLAGS in the kernel Makefile
kernel: $(COMPAT_CONFIG) $(COMPAT_AUTOCONF)
	@echo "Building kernel modules"
	@echo "Kernel version: $(KVERSION)"
	@echo "Modules directory: $(INSTALL_MOD_PATH)/$(MODULES_DIR)"
	@echo "Kernel sources: $(KSRC_OBJ)"
	env CWD=$(CWD) BACKPORT_INCLUDES=$(BACKPORT_INCLUDES) \
		$(MAKE) -C $(KSRC_OBJ) SUBDIRS="$(CWD)" \
		V=$(V) KBUILD_NOCMDDEP=1 $(WITH_MAKE_PARAMS) \
		CONFIG_MEMTRACK=$(CONFIG_MEMTRACK) \
		CONFIG_DEBUG_INFO=$(CONFIG_DEBUG_INFO) \
		CONFIG_INFINIBAND=$(CONFIG_INFINIBAND) \
		CONFIG_INFINIBAND_IPOIB=$(CONFIG_INFINIBAND_IPOIB) \
		CONFIG_INFINIBAND_IPOIB_CM=$(CONFIG_INFINIBAND_IPOIB_CM) \
		CONFIG_INFINIBAND_SRP=$(CONFIG_INFINIBAND_SRP) \
		CONFIG_INFINIBAND_SRPT=$(CONFIG_INFINIBAND_SRPT) \
		CONFIG_SCSI_SRP_ATTRS=$(CONFIG_SCSI_SRP_ATTRS) \
		CONFIG_INFINIBAND_USER_MAD=$(CONFIG_INFINIBAND_USER_MAD) \
		CONFIG_INFINIBAND_USER_ACCESS=$(CONFIG_INFINIBAND_USER_ACCESS) \
		CONFIG_INFINIBAND_USER_MEM=$(CONFIG_INFINIBAND_USER_MEM) \
		CONFIG_INFINIBAND_ADDR_TRANS=$(CONFIG_INFINIBAND_ADDR_TRANS) \
		CONFIG_INFINIBAND_ADDR_TRANS_CONFIGFS=$(CONFIG_INFINIBAND_ADDR_TRANS_CONFIGFS) \
		CONFIG_INFINIBAND_MTHCA=$(CONFIG_INFINIBAND_MTHCA) \
		CONFIG_INFINIBAND_IPOIB_DEBUG=$(CONFIG_INFINIBAND_IPOIB_DEBUG) \
		CONFIG_INFINIBAND_ISERT=$(CONFIG_INFINIBAND_ISERT) \
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
		CONFIG_INFINIBAND_RDMAVT=$(CONFIG_INFINIBAND_RDMAVT) \
		CONFIG_INFINIBAND_RXE=$(CONFIG_INFINIBAND_RXE) \
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
		CONFIG_SCSI_CXGB3_ISCSI=$(CONFIG_SCSI_CXGB3_ISCSI) \
		CONFIG_SCSI_CXGB4_ISCSI=$(CONFIG_SCSI_CXGB4_ISCSI) \
		CONFIG_INFINIBAND_I40IW=$(CONFIG_INFINIBAND_I40IW) \
		CONFIG_I40E=$(CONFIG_I40E) \
		CONFIG_INFINIBAND_NES=$(CONFIG_INFINIBAND_NES) \
		CONFIG_INFINIBAND_NES_DEBUG=$(CONFIG_INFINIBAND_NES_DEBUG) \
		CONFIG_MLX4_CORE=$(CONFIG_MLX4_CORE) \
		CONFIG_MLX5_CORE=$(CONFIG_MLX5_CORE) \
		CONFIG_MLX5_CORE_EN=$(CONFIG_MLX5_CORE_EN) \
		CONFIG_MLX5_CORE_EN_DCB=$(CONFIG_MLX5_CORE_EN_DCB) \
		CONFIG_MLX4_EN=$(CONFIG_MLX4_EN) \
		CONFIG_MLX4_EN_DCB=$(CONFIG_MLX4_EN_DCB) \
		CONFIG_MLX4_INFINIBAND=$(CONFIG_MLX4_INFINIBAND) \
		CONFIG_MLX5_INFINIBAND=$(CONFIG_MLX5_INFINIBAND) \
		CONFIG_MLX4_ETHERNET=$(CONFIG_MLX4_ETHERNET) \
		CONFIG_MLX4_DEBUG=$(CONFIG_MLX4_DEBUG) \
		CONFIG_MLX5_DEBUG=$(CONFIG_MLX5_DEBUG) \
		CONFIG_IBP_SERVER=$(CONFIG_IBP_SERVER) \
		CONFIG_IBP_DEBUG=$(CONFIG_IBP_DEBUG) \
		CONFIG_INFINIBAND_SCIF=$(CONFIG_INFINIBAND_SCIF) \
		CONFIG_INFINIBAND_AMSO1100=$(CONFIG_INFINIBAND_AMSO1100) \
		CONFIG_SUNRPC_XPRT_RDMA=$(CONFIG_SUNRPC_XPRT_RDMA) \
		CONFIG_SUNRPC_XPRT_RDMA_CLIENT=$(CONFIG_SUNRPC_XPRT_RDMA_CLIENT) \
		CONFIG_SUNRPC_XPRT_RDMA_SERVER=$(CONFIG_SUNRPC_XPRT_RDMA_SERVER) \
		CONFIG_INFINIBAND_OCRDMA=$(CONFIG_INFINIBAND_OCRDMA) \
		CONFIG_BE2NET=$(CONFIG_BE2NET) \
		CONFIG_INFINIBAND_ISERT=$(CONFIG_INFINIBAND_ISERT) \
		CONFIG_INFINIBAND_USNIC=$(CONFIG_INFINIBAND_USNIC) \
		CONFIG_INFINIBAND_HFI1=$(CONFIG_INFINIBAND_HFI1) \
		CONFIG_INFINIBAND_VMWARE_PVRDMA=$(CONFIG_INFINIBAND_VMWARE_PVRDMA) \
		CONFIG_NVME_CORE=$(CONFIG_NVME_CORE) \
		CONFIG_BLK_DEV_NVME=$(CONFIG_BLK_DEV_NVME) \
		CONFIG_NVME_RDMA=$(CONFIG_NVME_RDMA) \
		CONFIG_NVME_FABRICS=$(CONFIG_NVME_FABRICS) \
		CONFIG_NVME_TARGET=$(CONFIG_NVME_TARGET) \
		CONFIG_NVME_TARGET_RDMA=$(CONFIG_NVME_TARGET_RDMA) \
		CONFIG_QED=$(CONFIG_INFINIBAND_QEDR) \
		CONFIG_QEDE=$(CONFIG_INFINIBAND_QEDR) \
		CONFIG_QED_LL2=$(CONFIG_INFINIBAND_QEDR) \
		CONFIG_QED_RDMA=$(CONFIG_INFINIBAND_QEDR) \
		CONFIG_INFINIBAND_QEDR=$(CONFIG_INFINIBAND_QEDR) \
		CONFIG_INFINIBAND_BNXT_RE=$(CONFIG_INFINIBAND_BNXT_RE) \
		LINUXINCLUDE=' \
		-D__OFED_BUILD__ \
		-D__KERNEL__ \
		$(CFLAGS) \
		-include $(autoconf_h) \
		$(KCONFIG_H) \
		-include $(CWD)/include/linux/compat-2.6.h \
		$(BACKPORT_INCLUDES) \
		$(KERNEL_MEMTRACK_CFLAGS) \
		$(OPENIB_KERNEL_EXTRA_CFLAGS) \
		-I$(CWD)/include \
		-I$(CWD)/include/uapi \
		-I$(CWD)/drivers/infiniband/debug \
		-I/usr/local/include/scst \
		-I$(CWD)/drivers/infiniband/ulp/srpt \
		$$(if $$(CONFIG_XEN),-D__XEN_INTERFACE_VERSION__=$$(CONFIG_XEN_INTERFACE_VERSION)) \
		$$(if $$(CONFIG_XEN),-I$$(srctree)/arch/x86/include/mach-xen) \
		-I$$(srctree)/arch/$$(SRCARCH)/include \
		-Iarch/$$(SRCARCH)/include/generated \
		-Iinclude \
		-I$$(srctree)/arch/$$(SRCARCH)/include/uapi \
		-Iarch/$$(SRCARCH)/include/generated/uapi \
		-I$$(srctree)/include \
		-I$$(srctree)/include/uapi \
		-Iinclude/generated/uapi \
		$$(if $$(KBUILD_SRC),-Iinclude2 -I$$(srctree)/include) \
		-I$$(srctree)/arch/$$(SRCARCH)/include \
		-Iarch/$$(SRCARCH)/include/generated \
		-I$(CWD)/drivers/nvme/host \
		-I$(CWD)/drivers/nvme/target \
		' \
		modules


#########################
#	Install kernel	#
#########################
install_modules:
	@echo "Installing kernel modules"

	$(MAKE) -C $(KSRC_OBJ) SUBDIRS="$(CWD)" \
		INSTALL_MOD_PATH=$(INSTALL_MOD_PATH) \
		INSTALL_MOD_DIR=$(INSTALL_MOD_DIR) \
		$(WITH_MAKE_PARAMS) modules_install;
	if [ ! -n "$(INSTALL_MOD_PATH)" ]; then $(DEPMOD) $(KVERSION);fi;

clean: clean_kernel

clean_kernel:
	$(MAKE) -C $(KSRC_OBJ) rm-files= SUBDIRS="$(CWD)" $(WITH_MAKE_PARAMS) clean

distclean: clean_kernel
	@/bin/rm -f $(clean-files)

clean-files := Module.symvers modules.order Module.markers compat/modules.order compat/configure
clean-files += $(COMPAT_CONFIG) $(COMPAT_AUTOCONF)
clean-files += include/linux/autoconf.h include/generated/autoconf.h

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
