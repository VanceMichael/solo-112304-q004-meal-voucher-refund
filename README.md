# 联营餐券离线核销与分项退款

商户网页展示券包，收银网关提供结班后补传的核销与冲销。业务金额均以整数分表示。

本地来源与合作端均使用合成业务资料。Python 3.11 运行来源服务，服务默认绑定回环地址。

```sh
python3 source_fixture.py --port 8765
python3 -m unittest discover -s tests -v
```

浏览器测试使用 Playwright 1.56.0 和随该版本安装的 Chromium。首次建立环境时运行 `python3 -m pip install -r requirements-browser.txt` 与 `python3 -m playwright install chromium`。

## 数据交换

- `/merchant/activity` 链接券包、门店组授权及转让。各权益价格独立。转给新店前的有效核销仍须使用原授权窗。
- `/pos/closures` 给出每设备营业班的序号闭区间和确认空号。另一设备的相同序号与本班无关。
- `/pos/sync` 通过原设备、营业班、序号指向先前核销。occurred 为当地实际发生时间，received 为网关收件时间，两者都保留。
- `/merchant/refunds` 为商户退券页面，按权益编号核对逐项回执。财务侧 `/finance/debts` 只接确有冲突的权益。

演练运维端 `GET /__scene` 返回当前时间点，`POST /__scene` 接受 JSON 字段 `index`，从 0 开始顺序切换，每次加 1。换场不会清除合作端当次运行已生成的回执。需要开始新的独立演练时重启服务。业务时间以各来源的当前版本为准。

合作端允许按 `request` 字段查找同路径下的业务请求号，提交使用 `request`、`operation`、`items`（字符串数组）。业务明细使用可选 JSON 对象 `details`，以此请求内的条目编号为键。界面端填多项时按逗号分隔。来源约定的业务动作按下表允许值填写。统一回执含请求号、模拟回执号与各行状态。相同请求号的原样重交返回原回执，参数有变则返回 HTTP 409。回执检索的 404 表示该时刻未查到。描述业务状态的可读来源会随演练进度独立更新，某次提交回执不会提前改写该来源。

## 合作端动作

- `/merchant/refunds` 接受 `refund`、`inquire`。
- `/finance/debts` 接受 `claim`。
