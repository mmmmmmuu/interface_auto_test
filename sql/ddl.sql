/*
 Navicat Premium Data Transfer

 Source Server         : 10.9.18.53
 Source Server Type    : MySQL
 Source Server Version : 50635
 Source Host           : 10.9.18.53:3306
 Source Schema         : mogo

 Target Server Type    : MySQL
 Target Server Version : 50635
 File Encoding         : 65001

 Date: 08/08/2019 11:29:59
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for batch_info
-- ----------------------------
DROP TABLE IF EXISTS `batch_info`;
CREATE TABLE `batch_info`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'id',
  `batch_no` int(11) NOT NULL COMMENT '批次号',
  `data_list` text NOT NULL COMMENT '放款信息表',
  `flow_day` text NOT NULL COMMENT 'flow',
  `create_date` date NOT NULL COMMENT '创建时间',
  `update_time` datetime(0) NOT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '批次表' ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for table_config
-- ----------------------------
DROP TABLE IF EXISTS `table_config`;
CREATE TABLE `table_config`  (
  `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
  `sort_no` int(10) UNSIGNED NOT NULL COMMENT '排序编号',
  `table_schema` varchar(40) NOT NULL DEFAULT 'calculator_xfh' COMMENT '表库名',
  `table_name` varchar(40) NOT NULL COMMENT '要检测的表名',
  `amount` int(10) NOT NULL DEFAULT 0 COMMENT '表个数',
  `columns` varchar(255) NOT NULL COMMENT '列名',
  `test_table` varchar(40) NOT NULL COMMENT '测试表名',
  `create_date` date NOT NULL COMMENT '创建日期',
  `update_time` datetime(0) NOT NULL ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新日期',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique`(`table_name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '配置表' ROW_FORMAT = Compact;

-- ----------------------------
-- Records of table_config
-- ----------------------------
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (1, 0, 'cal', 'acct_change_rate_segment', 1, '', 'acct_change_rate_segment', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (2, 0, 'cal', 'acct_change_rpt_segment', 1, '', 'acct_change_rpt_segment', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (3, 0, 'cal', 'acct_coupon_log', 1, '', 'acct_coupon_log', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (4, 0, 'cal', 'acct_finance_process', 1, '', 'acct_finance_process', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (5, 0, 'cal', 'acct_interest_change_schedule', 1, '', 'acct_interest_change_schedule', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (6, 0, 'cal', 'acct_interest_difference', 1, '', 'acct_interest_difference', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (7, 0, 'cal', 'acct_interest_log', 16, '', 'acct_interest_log', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (8, 1, 'cal', 'acct_loan', 1, '', 'acct_loan', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (9, 0, 'cal', 'acct_loan_change', 1, '', 'acct_loan_change', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (10, 0, 'cal', 'acct_loan_creditor', 1, '', 'acct_loan_creditor', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (11, 0, 'cal', 'acct_loan_rate_segment', 0, '', 'acct_loan_rate_segment', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (12, 0, 'cal', 'acct_loan_rpt_segment', 1, '', 'acct_loan_rpt_segment', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (13, 0, 'cal', 'acct_loan_subsidy', 1, '', 'acct_loan_subsidy', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (14, 0, 'cal', 'acct_margin_detail', 1, '', 'acct_margin_detail', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (15, 0, 'cal', 'acct_payment', 16, '', 'acct_payment', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (16, 0, 'cal', 'acct_payment_log', 16, '', 'acct_payment_log', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (17, 0, 'cal', 'acct_payment_schedule', 16, '', 'acct_payment_schedule', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (18, 0, 'cal', 'acct_payment_schedule_tmp', 1, '', 'acct_payment_schedule_tmp', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (19, 0, 'cal', 'acct_payment_tmp', 1, '', 'acct_payment_tmp', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (20, 0, 'cal', 'acct_putout', 1, '', 'acct_putout', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (21, 0, 'cal', 'acct_putout_rate_segment', 1, '', 'acct_putout_rate_segment', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (22, 0, 'cal', 'acct_putout_rpt_segment', 1, '', 'acct_putout_rpt_segment', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (23, 0, 'cal', 'acct_transaction', 16, '', 'acct_transaction', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (24, 0, 'cal', 'acct_transaction_tnd', 16, '', 'acct_transaction_tnd', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (25, 0, 'cal', 'acct_writeoff_log', 1, '', 'acct_writeoff_log', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (26, 0, 'cal', 'bat_task_log', 1, '', 'bat_task_log', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (27, 0, 'cal', 'system_setup', 1, '', 'system_setup', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (28, 0, 'cal', 'withdrawal_form', 1, '', 'withdrawal_form', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (29, 0, 'cal', 'acct_loan_exended_attribute', 16, '', 'acct_loan_exended_attribute', '0000-00-00 00:00:00', '2020-05-11 22:03:52');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (101, 0, 'account', 'acct_subledger_detail', 128, '', 'acct_subledger_detail', '0000-00-00 00:00:00', '2020-05-11 22:04:09');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (102, 0, 'account', 'acct_subsidiary_ledger', 16, '', 'acct_subsidiary_ledger', '0000-00-00 00:00:00', '2020-05-11 22:04:11');
INSERT INTO `table_config`(`id`, `sort_no`, `table_schema`, `table_name`, `amount`, `columns`, `test_table`, `create_date`, `update_time`) VALUES (201, 0, 'public', 'acct_loan_reference', 1, '', 'acct_loan_reference', '0000-00-00 00:00:00', '2020-05-11 22:03:52');

-- ----------------------------
-- Table structure for synd_mapping
-- ----------------------------
DROP TABLE IF EXISTS `synd_mapping`;
CREATE TABLE `synd_mapping` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `batch_no` varchar(40) NOT NULL COMMENT '批次编号',
  `syndicate_no` varchar(40) NOT NULL DEFAULT '' COMMENT '银团编号',
  `org_no` varchar(10) NOT NULL DEFAULT '' COMMENT '机构号',
  `serialno` varchar(40) NOT NULL DEFAULT '' COMMENT '借据编号',
  `loan_id` bigint(20) NOT NULL DEFAULT '0' COMMENT '系统编号id',
  PRIMARY KEY (`id`),
  KEY `batch_synd_org` (`batch_no`,`syndicate_no`,`org_no`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE = utf8mb4_general_ci COMMENT='联合贷银团编号借据号映射表';

SET FOREIGN_KEY_CHECKS = 1;
