from p8executor.batchRnner import Batch
from p2myconfig import config
from p5common.utils import *

logging.getLogger().setLevel(logging.DEBUG)

batch_no = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
# batch_no = "20200523003810329422"
response = Batch(batch_no=batch_no, batch_id=1, params={"businessSum": 10000, "businessTerm": 6, "defaultDueDay": "20", "syndicateSerialNo": "56010002", "putoutDate": "2019-09-20"}).execute()
# print(response)

# json.loads("1:2:3；4")
# print(time.time())

# datetime.datetime.now().strftime()

# param = {"businessSum": 100000, "businessTerm": 3, "defaultDueDay": "25", "syndicateSerialNo": "56010002", "putoutDate": "2019-09-20", "paymentDate": "2019-09-20","flexiblePutoutSubsidyDto": {"subsidyInterestRate": 0.2, "subsidyInterestAmount": 3120, "orderAmount": 12000}}
# print(json.dumps(param))



