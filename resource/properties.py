import json

from myconfig.config import *
from selfenum.RequestType import RequestType
from copy import copy

scene = {}

scene["putoutTrial"] = {"requestType": RequestType.post, "desc": "放款试算接口",
                        "info": {"businessRate": businessRate, "rateUnit": rateType, "businessSum": 10000, "businessTerm": "3", "putoutDate": "2019-01-02",
                                 "rptTermID": rptTermID, "defaultDueDay": None, "firstDueDate": None}
                        }

scene["putoutApply"] = {"requestType": RequestType.post, "desc": "放款申请",
                        "info": {"applyId": "", "customerId": customerId, "customerName": customerName, "contractNo": contractNo,
                                 "businessType": businessType,
                                 "productId": productId, "specificSerialNo": specificSerialNo, "businessSum": "", "currency": "CNY",
                                 "putoutDate": "2019-01-02", "businessTerm": "3",
                                 "businessRate": businessRate, "fineRate": fineRate, "rptTermId": rptTermID, "defaultDueDay": None, "graceDays": "3",
                                 "firstDueDate": None, "accountingOrgId": accountingOrgId,
                                 "channelOrgId": channelOrgId, "syndicateSerialNo": None, "selfAccountingFlag": "1", "loansUsed": "010",
                                 "operateOrgId": operateOrgId}
                        }

scene["flexiblePutoutApply"] = {
    "requestType": RequestType.post,
    "desc": "灵活放款申请",
# "putoutCouponDto": {"couponNo": None,   # 优惠券编号   "exChangeCode": None,  # 优惠券兑换码 "couponType": None,  # 优惠券类型
                    # "freeBeginPeriod":None,   # 免息开始期次 "freeDays":None,   # 免息天数  "discountRate":None  # 折扣率}  #优惠券
}
scene["flexiblePutoutApply"]["info"] = copy(scene['putoutApply']['info'])
scene["flexiblePutoutApply"]["info"].update({"putoutCouponDto": None,
                                             "flexiblePutoutSubsidyDto": {"subsidyInterestCalcType": 1,   # 贴息计算方式
                                                                          "subsidyInterestCalcMode": 1,   # 贴息方式
                                                                          "subsidyInterestBase": 2,   # 贴息基数
                                                                          "subsidyInterestRate": None,   # 贴息率（%）
                                                                          "subsidyInterestAmount": None,   # 贴息金额
                                                                          "orderAmount": None,   # 订单金额
                                                                          "subsidyEndDate": None},   # 贴息截止日期
                                             "rateList": [{"rateType": "01",   # 利率类型
                                                           "businessRate": businessRate,   # 年利率
                                                           "beginDate": None,   # 开始日期
                                                           "endDate": None},
                                                          {"rateType": "02",   # 利率类型
                                                           "businessRate": fineRate,   # 年利率
                                                           "beginDate": None,   # 开始日期
                                                           "endDate": None}],   # 结束日期
                                             "rptList": [{"rptTermId": rptTermID,   # 还款方式
                                                          "beginDate": None,   # 开始日期
                                                          "endDate": None,   # 结束日期
                                                          "segInstalmentAmt": None,   # 指定期供金额
                                                          "restPaymentAmount": None}]})


scene["executeTransaction"] = {"requestType": RequestType.post, "desc": "{}交易入账",
                               "info": {"transactionId": None, "transCode": "1001", "payOrderId": "201812190000001", "paymentStatus": "1",
                                        "paymentDate": "2018-01-02",
                                        "productId": productId, "loanSerialNo": None}
                               }

scene["prepaymentTrial"] = {
    "requestType": RequestType.post,
    "desc": "提前还款试算接口",
    "info": {"businessDate": "2018-02-02", "loanSerialNo": "", "prePayAmt": 0, "prePayAmtFlag": 2, "prePayInterestBaseFlag": 2,
             "prePayInterestDaysFlag": 1, "prePayType": 3, "productId": productId}
}

scene["paymentTrial"] = {
    "requestType": RequestType.post,
    "desc": "正常/逾期还款试算接口",
    "info": {"businessDate": "2018-02-02", "loanSerialNo": "", "productId": productId, "toPeriodNo": None}
}

scene["reverseTransaction"] = {
    "requestType": RequestType.post,
    "desc": "冲销{}交易",
    "info": {"loanSerialNo": "", "productId": None, "transCode": "4001", "reTransactionId": 0, "channelNo": "", "inputOrgNo": None,
             "inputUserNo": None}
}

scene["returnGoodsTrial"] = {
    "requestType": RequestType.post,
    "desc": "退货试算",
    "info": {"loanSerialNo": "", "productId": productId, "hesitantFlag": False, "hesitationDays": "7", "returnType": "2", "amountType": "1",
             "returnAmount": "", "prePayType": "1"}
}

scene["returnGoods"] = {
    "requestType": RequestType.post,
    "desc": "退货申请",
    "info": {"loanSerialNo": "", "productId": productId, "hesitantFlag": True, "hesitationDays": 7, "returnType": 1, "amountType": 1,
             "returnAmount": 0,
             "prePayType": 1, "applyId": ''}
}

scene["endOfDay"] = {
    "requestType": RequestType.post,
    "desc": "借据日切",
    "info": {"loanId": "", "productId": productId}
}

scene["paymentApply"] = {
    "requestType": RequestType.post,
    "desc": "{}还款申请",
    "info": {"applyId": '', "loanSerialNo": "", "transCode": "2001", "amt": 0, "productId": productId, "prePayType": 3, "businessDate": None,
             "bankName": "测试银行1",
             "payRuleType": None, "prePayInterestDaysFlag": 1, "prePayInterestBaseFlag": 2, "prePayAmtFlag": 2, "accountNo": "6666777788881111",
             "accountName": "测试账户1", "waiveInterestAmt": 0,
             "waivePrincipalPenaltyAmt": 0, "waiveInterestPenaltyAmt": 0, "waivePrepayPenaltyAmt": 0, "waiveFeeAmt": 0, "paymentType": 11,
             "remark": "test备注1", "coupons": []}
}

scene["endOfDayAllToDate"] = {
    "requestType": RequestType.post,
    "desc": "单产品跑批至指定日期",
    "info": {"toBusinessDate": "", "productId": productId, "accountingOrgNo": accountingOrgId}
}

scene["writeOff"] = {
    "requestType": RequestType.post,
    "desc": "贷款核销",
    "info": {"applyId": '', "loanSerialNo": "", "productId": productId}
}

scene["changeTransaction"] = {
    "requestType": RequestType.post,
    "desc": "变更交易",
    "info": {"applyId": '', "loanSerialNo": "", "productId": productId, "transCode": "", "maturityDate": None,
             "accountingOrgId": accountingOrgId, "defaultDueDay": None, "rptTermId": None,
             "loanRateTermId": None, "loanRateType": None, "rateChangeFlag": None}
}

scene["underLinePayment"] = {
    "requestType": RequestType.post,
    "desc": "记录线下还款申请",
    "info": {"registeredPhone": "13222222222", "customerNo": customerId, "customerName": customerName, "confirmationAmount": "", "loadNo": "",
             "submitDate": "",
             "submitTime": ""}
}

scene["createProcessData"] = {
    "requestType": RequestType.post,
    "desc": "准备代扣数据",
    "info": {"applyId": ''}
}

scene["calcPamentDate"] = {
    "requestType": RequestType.post,
    "desc": "计算客户还款日及到期日",
    "info": {"customerId": contractNo, "productId": productId, "putoutDate": "2018-01-02", "term ": None}
}

scene["queryCustomerSchedule"] = {
    "requestType": RequestType.post,
    "desc": "客户还款计划查询",
    "info": {"customerId": contractNo, "productId": productId, "accountingOrgId": accountingOrgId, "payDate ": None}
}

scene["queryLoan"] = {
    "requestType": RequestType.post,
    "desc": "客户借据查询",
    "info": {"customerId": "", "productId": productId, "accountingOrgId": accountingOrgId, "contractSerialNo": None, "loanSerialNo": None}
}

scene["queryLoanSchedule"] = {
    "requestType": RequestType.post,
    "desc": "借据还款计划查询",
    "info": {"loanSerialNo": "", "productId": productId}
}

scene["queryPaymentLog"] = {
    "requestType": RequestType.post,
    "desc": "查询借据还款流水",
    "info": {"loanSerialNo": "", "productId": productId}
}

scene["interestChange"] = {
    "requestType": RequestType.post,
    "desc": "息费调整",
    "info": {"loanSerialNo": "", "productId": productId, "waiveInterestAmt": 0.0, "waivePrincipalPenaltyAmt": 0.0, "waiveInterestPenaltyAmt": 0.0,
             "waiveFeeAmt": 0.0, "schedules": {}}
}

scene["endOfDay"] = {
    "requestType": RequestType.post,
    "desc": "借据日切",
    "info": {"loanId": "", "productId": productId}
}


# initSql = [
#     "delete from calculator_public.acct_syndicate_info where syndicate_no in ('10091001','10091002','10091003');",
#     "INSERT INTO calculator_public.acct_syndicate_info(syndicate_no, org_no, org_name, principal_ratio, principal_amt, profit_pay_type, profit_ratio, status, creditor_way, principal_penalty_ratio, interest_palenalty_ratio, fee_ratio, trans_fee_ratio, create_time) VALUES ('10091001', 'test1', '测试用联合贷资金方1', 30, 0.00, '01', 0.0, 1, '01', 0.0, 0.0, 0.0, 0.0, now());",
#     "INSERT INTO calculator_public.acct_syndicate_info(syndicate_no, org_no, org_name, principal_ratio, principal_amt, profit_pay_type, profit_ratio, status, creditor_way, principal_penalty_ratio, interest_palenalty_ratio, fee_ratio, trans_fee_ratio, create_time) VALUES ('10091002', 'test2', '测试用联合贷资金方2', 80, 0.00, '02', 60.0, 1, '01', 20.0, 30.0, 40.0, 25.0, now());",
#     "INSERT INTO calculator_public.acct_syndicate_info(syndicate_no, org_no, org_name, principal_ratio, principal_amt, profit_pay_type, profit_ratio, status, creditor_way, principal_penalty_ratio, interest_palenalty_ratio, fee_ratio, trans_fee_ratio, create_time) VALUES ('10091003', 'test3', '测试用联合贷资金方3', 90, 0.00, '03', 8.0, 1, '01', 9.0, 10.0, 30.0, 25.0, now());",
#     "truncate table product_center.prd_business_type;",
#     "INSERT INTO product_center.prd_business_type(type_name, type_no, remark, create_time, update_time, status) VALUES ('幸福花', 'XFH001', '', now(), now(), 1);",
#     "INSERT INTO product_center.prd_business_type(type_name, type_no, remark, create_time, update_time, status) VALUES ('幸福结', 'XFJ002', '', now(), now(), 1);",
#     "INSERT INTO product_center.prd_business_type(type_name, type_no, remark, create_time, update_time, status) VALUES ('幸福买-建材贷', 'XFM001', '', now(), now(), 1);",
#     "INSERT INTO product_center.prd_business_type(type_name, type_no, remark, create_time, update_time, status) VALUES ('幸福买-装修贷', 'XFM002', '', now(), now(), 1);",
#     "INSERT INTO product_center.prd_business_type(type_name, type_no, remark, create_time, update_time, status) VALUES ('幸福买-教育贷', 'XFM003', '', now(), now(), 1);",
#     "truncate table product_center.prd_spec_limit_resource;",
#     "INSERT INTO product_center.prd_spec_limit_resource(spec_limit_name, spec_limit_code, create_time, update_time) VALUES ('客源', 'customerType', now(), now());",
#     "INSERT INTO product_center.prd_spec_limit_resource(spec_limit_name, spec_limit_code, create_time, update_time) VALUES ('渠道', 'channel', now(), now());",
#     "INSERT INTO product_center.prd_spec_limit_resource(spec_limit_name, spec_limit_code, create_time, update_time) VALUES ('期限', 'terms', now(), now());",
#     "truncate table product_center.prd_parameter;",
#     "INSERT INTO product_center.prd_parameter(parameter_no, parameter_name, value_type, data_type, create_time, update_time, status) VALUES ('useDays', '贷款使用天数', 1, 1, now(), now(), 1);",
#     "INSERT INTO product_center.prd_parameter(parameter_no, parameter_name, value_type, data_type, create_time, update_time, status) VALUES ('feeRatio', '提前还款费率', 2, 1, now(), now(), 1);",
#     "INSERT INTO product_center.prd_parameter(parameter_no, parameter_name, value_type, data_type, create_time, update_time, status) VALUES ('serviceCharge', '手续费基础', 2, 3, now(), now(), 1);",
#     "delete from product_center.prd_decision where decision_no='TQHKSXF';",
#     "INSERT INTO product_center.prd_decision(decision_no, decision_name, parameter_no, parameter_name, status, create_time, update_time) VALUES ('TQHKSXF', '提前还款手续费', 'useDays', '贷款使用天数', 1, now(), now());",
#     "INSERT INTO product_center.prd_decision(decision_no, decision_name, parameter_no, parameter_name, status, create_time, update_time) VALUES ('TQHKSXF', '提前还款手续费', 'feeRatio', '提前还款费率', 1, now(), now());",
#     "INSERT INTO product_center.prd_decision(decision_no, decision_name, parameter_no, parameter_name, status, create_time, update_time) VALUES ('TQHKSXF', '提前还款手续费', 'serviceCharge', '手续费基础', 1, now(), now());",
#     "delete from product_center.prd_unit_decision where unit_code='TQHKSXF';",
#     "INSERT INTO product_center.prd_unit_decision(unit_code, unit_name, unit_class, unit_type, decision_no, decision_name, remark, status, create_time, update_time) VALUES ('TQHKSXF', '提前还款手续费', '4', '1', 'TQHKSXF', '提前还款手续费', '1,2,3', 1, now(), now());",
#     #    "update product_center.prd_spec set status = 0 where prd_no='{}' and prd_spec_no='2018060800000006'".format('1001'),
#     "delete from product_center.prd_spec where prd_no='{}' and prd_spec_no='2018060800000006'".format('1001'),
#     "INSERT INTO product_center.prd_spec(prd_no, prd_name, prd_spec_no, prd_spec_name, status, remark, create_time, update_time) VALUES ('{}', '幸福花', '2018060800000006', '幸福花', 1, '', now(), now());".format(
#         '1001'),
#     "delete from product_center.prd_spec_param_decision where decision_no='TQHKSXF' and prd_spec_no='2018060800000006';",
#     "INSERT INTO product_center.prd_spec_param_decision(decision_no, sort_no, parameter_no, parameter_value, parameter_value_min, parameter_value_max, prd_spec_no, status, create_time) VALUES ('TQHKSXF', '1', 'useDays', '', '1', '7', '2018060800000006', 1, now());",
#     "INSERT INTO product_center.prd_spec_param_decision(decision_no, sort_no, parameter_no, parameter_value, parameter_value_min, parameter_value_max, prd_spec_no, status, create_time) VALUES ('TQHKSXF', '1', 'feeRatio', '0', '', '', '2018060800000006', 1, now());",
#     "INSERT INTO product_center.prd_spec_param_decision(decision_no, sort_no, parameter_no, parameter_value, parameter_value_min, parameter_value_max, prd_spec_no, status, create_time) VALUES ('TQHKSXF', '1', 'serviceCharge', '1', '', '', '2018060800000006', 1, now());",
#     "INSERT INTO product_center.prd_spec_param_decision(decision_no, sort_no, parameter_no, parameter_value, parameter_value_min, parameter_value_max, prd_spec_no, status, create_time) VALUES ('TQHKSXF', '2', 'useDays', '', '8', '13', '2018060800000006', 1, now());",
#     "INSERT INTO product_center.prd_spec_param_decision(decision_no, sort_no, parameter_no, parameter_value, parameter_value_min, parameter_value_max, prd_spec_no, status, create_time) VALUES ('TQHKSXF', '2', 'feeRatio', '3', '', '', '2018060800000006', 1, now());",
#     "INSERT INTO product_center.prd_spec_param_decision(decision_no, sort_no, parameter_no, parameter_value, parameter_value_min, parameter_value_max, prd_spec_no, status, create_time) VALUES ('TQHKSXF', '2', 'serviceCharge', '1', '', '', '2018060800000006', 1, now());",
#     "INSERT INTO product_center.prd_spec_param_decision(decision_no, sort_no, parameter_no, parameter_value, parameter_value_min, parameter_value_max, prd_spec_no, status, create_time) VALUES ('TQHKSXF', '3', 'useDays', '', '14', '999999999', '2018060800000006', 1, now());",
#     "INSERT INTO product_center.prd_spec_param_decision(decision_no, sort_no, parameter_no, parameter_value, parameter_value_min, parameter_value_max, prd_spec_no, status, create_time) VALUES ('TQHKSXF', '3', 'feeRatio', '5', '', '', '2018060800000006', 1, now());",
#     "INSERT INTO product_center.prd_spec_param_decision(decision_no, sort_no, parameter_no, parameter_value, parameter_value_min, parameter_value_max, prd_spec_no, status, create_time) VALUES ('TQHKSXF', '3', 'serviceCharge', '1', '', '', '2018060800000006', 1, now());"
# ]
#
