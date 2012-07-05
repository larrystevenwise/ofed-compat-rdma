obj-y := compat/
obj-$(CONFIG_INFINIBAND)        += drivers/infiniband/
obj-$(CONFIG_CHELSIO_T3)        += drivers/net/ethernet/chelsio/cxgb3/
obj-$(CONFIG_CHELSIO_T4)        += drivers/net/ethernet/chelsio/cxgb4/
obj-$(CONFIG_MLX4_CORE)         += drivers/net/ethernet/mellanox/mlx4/
obj-$(CONFIG_RDS)               += net/rds/
obj-$(CONFIG_SUNRPC_XPRT_RDMA)  += net/sunrpc/xprtrdma/
