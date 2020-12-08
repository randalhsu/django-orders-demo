## 用 Django 實作基本電商介面

## [Live Demo](https://martdemo.herokuapp.com/)

![Mart demo](https://i.imgur.com/ioUsP7P.jpg)

* 頁面包含：購買欄位、商品庫存列表、訂單紀錄列表、Top 3 按鈕
* 可從購買欄位選擇商品和數量並加入，成為訂單
    * 若庫存不足，則報錯
    * 若商品僅供 VIP 身份購買，但使用者不具 VIP 身分，則報錯
* 可刪除既有訂單
    * 若商品由庫存 0 釋出，則回報到貨
* 計算 Top 3 最受歡迎的商品
* 提供 API endpoint 供爬蟲 (``crawler.py``) 爬取訂單統計
* 具備單元測試 (``orders/tests.py``)
