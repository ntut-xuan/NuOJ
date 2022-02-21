# NuOJ

<img src="https://i.imgur.com/YHtW6Kj.png" alt="img" style="zoom: 25%;" />

你好，歡迎來到 NuOJ 開發計劃。

目前 NuOJ 依然還在建造中，請稍待我們的發行版。



## 簡介

由 國立臺北科技大學 109 資訊工程系 黃漢軒 開發，一款來自國立臺北科技大學的開源的 Online Judge，可供教學與競賽使用。



銘謝：國立臺北科技大學 資訊工程系 郭忠義 教授。



## 使用開源資源

### 前端

JQuery, Boostrap, Tailwindcss, SweetAlert2



### 後端

Flask, MariaDB





## ChangeLog / TODO

### 2022-02-11

#### ChangeLog

- 正在著手製作新增題目的部份，目前可以將新增題目的部份加入資料庫了。



### 2022-02-12

#### ChangeLog

- 修改了 Problem 的資料庫 Table 結構，將原先的 problem_deadline 移除，並且將資料庫欄位名稱修改稍微簡短一點。
- 修正 register 失敗後依然會產生 cookie 給使用者的問題。
- 使用 tailwindcss 重新編寫 index.html
- 使用 tailwindcss 重新編寫 login.html

#### TODO

- 使用 tailwindcss 重新編寫 register.html



### 2022-02-13

#### ChangeLog

 - 完成 github 登入的功能
 - 完成 https 的網域建置
 - Google OAuth 初勘

#### TODO

 - 使用 tailwindcss 重新編寫 register.html



### 2022-02-14

#### ChangeLog

 - 完成 Google OAuth 登入的功能
 - 廢除原先使用帳號密碼登入的功能



### 2022-02-15

#### ChangeLog

 - 完成一些的題目建置的部份



### 2022-02-16

#### ChangeLog

- 完成一些個人檔案的前端
- 新增 setting.json，用於設定 NuOJ 的相關設定

### 2022-02-19 

#### ChangeLog

- 修改 setting.json，使它能夠完全支援 github 與 google 的 OAuth 功能
- 重新改寫註冊與登入系統

### 2022-02-20

#### ChangeLog

- 推進新增題目功能的進度

### 2022-02-21

#### ChangeLog

- 初勘 pre-compile system 並進行實作
