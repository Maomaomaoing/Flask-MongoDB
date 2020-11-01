# Flask-MongoDB

<img src="https://github.com/Maomaomaoing/Flask-MongoDB/blob/master/cloud.png" width="250" height="150">
建立一個從將資料存入資料庫 ，進行資料分析 ，到查詢資料庫中內容和呈現分析結果的網頁，功能完整的系統。

## 將資料集存入mongoDB

*to_database.py*

資料集: Kaggle的”Homicide Reports, 1980-2014”

## 分析資料

*make_plot.py*

製作圖表
* 加害人和被害人年齡
* 被害人和加害人關系
* 被害人種族和性別
* 加害人種族和性別
* 使用的武器
* 發生地區
* 案件是否解決

<img src="https://github.com/Maomaomaoing/Flask-MongoDB/blob/master/analys_figure.png" width="500" height="300">

## 建立網頁

*index.py, attribute_value.py*

### Home  網頁首頁

<img src="https://github.com/Maomaomaoing/Flask-MongoDB/blob/master/web1.png" width="400" height="400">

### Analysis Result 資料圖表

<img src="https://github.com/Maomaomaoing/Flask-MongoDB/blob/master/web2.png" width="400" height="400">

### Querying  查詢資料庫

<img src="https://github.com/Maomaomaoing/Flask-MongoDB/blob/master/web3.png" width="400" height="400">
