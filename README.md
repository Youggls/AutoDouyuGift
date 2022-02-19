# AutoDouyuGift

## 注意！

斗鱼 Cookie 变化较快，本人暂未找到解决方案，如有解决方案可以通过issue、PR等方法联系本人，十分感谢您的贡献！

斗鱼自动送礼物脚本，自动赠送每天系统赠送的荧光棒给指定主播

## 支持功能

每天定时将背包内所有物品赠送给指定主播，暂不支持自定义赠送给不同主播

## 配置方法

1. fork 本仓库

2. 获取账号对应 Cookie，到斗鱼网页版，点开一个带有 Cookie 的请求，复制，并粘贴到本仓库的 SECRET 配置中。

    ![secrets](./img/secrets.png)

    ![secrets](./img/secrets2.png)

    ![secrets](./img/secrets3.png)

3. 类似地方法，在仓库中添加一个 `ROOMID` 字段，填入你想送礼物主播的房间号

4. `SCON` 和 `SCKEY`，如果想要开启 SERVER 酱的通知功能，请设置 `SCON` 字段为 `ON`，否则请填入 `OFF`。具体配置请见 [SERVER 酱](https://sct.ftqq.com/)

5. 触发方式：每次仓库提交时，或者是每天定时的时间点。本仓库目前配置的每天定时时间大概在北京时间 16:10 左右。
