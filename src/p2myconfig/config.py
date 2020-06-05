# -*- coding: utf-8 -*-
import time
from typing import Dict

from p2myconfig.config_li import *
import datetime

# db 设置
db_base_config = {
    "mincached": 2,
    "maxcached": 5,
    "maxshared": 3,
    "maxconnections": 20,
    "use_unicode": True,
    "charset": "utf8"
}
product_db.update(db_base_config)
test_db.update(db_base_config)

# db_ref = {"calculator": cal_db, "account": account_db, "public": public_db}
#
# notCleanTable = {cal_db: ["system_setup", "acct_syndicate_info"],
#                  account_db: [],
#                  public_db: ["acct_syndicate_info", "acct_lpr_rate_info", "acct_org_info", "public_payment_config"]}
#
# base_tables = ["batch_info", "synd_mapping", "table_config"]

# product 业务相关配置
# productId = "5003"
# accountingOrgId = "10085202"

# request 相关配置
HEADERS: Dict[str, str] = {"Content-Type": "application/json", "charset": "utf-8"}

# trate 贴息利率映射
# tiexi_rate = {3: 2.6, 6: 4.5, 12: 8.15}

# model 类型设置  record  记录标准数据  check  与标准数据比较
# model = "record"

# args 其他通用参数
