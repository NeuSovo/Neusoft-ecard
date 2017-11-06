### 接口说明

--------------

#### 以下接口均以GET方式提交，除check/recheck方法外，必须携带用户cookie

* [check] check?code=usercode *第一次验证用户微信号。*

* [recheck] recheck?code=usercode *session失效重新绑定*

* [bind] bind?ek=userek *绑定一卡通*

* [rebind] rebind?ek=userek *重新绑定或者换绑*

* [balance] balance *获取余额*

* [detail] detail?month=[01-12] *获取详单(month可为空，默认返回未入账记录)*

#### 返回码说明
---------------------
* **re/check**
    * code
        * 10000 绑定用户成功，没有绑卡
        * 10001 已绑定此用户，但没有绑卡
        * 10002 Session 更新成功
    * message
        * Success
        * failed
* **bind**
    * code
        * 10003 Session 不可用 需要执行recheck
        * 10004 绑卡的时候，卡片已有人绑定
        * 10005 绑卡成功
    * message
        * Success
        * failed

* **balance**
    * code
        * 10003 Session 不可用 需要执行recheck
        * 10006 获取余额成功
        * 10007 获取余额失败,可能卡片失效,需要重新绑定
    * message
        * Success
        * failed
    * info
        * kpye 卡片余额
        * zhye 账户余额
        * gdye 过度余额
* **detail**
    * code
        * 10003 Session 不可用 需要执行recheck
        * 10008 获取详细成功
        * 10009 获取详细失败，可能当前时间无记录。正常
    * message
        * Success
        * failed
    * info
        * time 消费时间
        * type 消费类型
        * skck 刷卡窗口
        * jye 交易额
        * yue 余额

！注意：当balance/detail 返回码为10003时无info

