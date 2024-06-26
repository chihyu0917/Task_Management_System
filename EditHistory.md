# Task Management System
## 紀錄
- 0329 by Sophie: http://127.0.0.1:8000/tasks/

- 0415 by Siowan
    1.  DB建立 由於Event需要DataBase存放數據，所以我用MySQL新增了一個DataBase，並且把db.sqlite3(Django內建的DB)的內容遷移到Django_SQL.sql
        [SQL 使用MySQL 8.3.0]
        - <__init__.py>
            ```
            import pymysql
            pymysql.install_as_MySQLdb()
            ```
            ->  將pymysql視為MySQLdb，使Django能夠正確地與MySQL數據庫進行交互。
                    原因：Django中使用MySQL數據庫時，Django的某些部分預期導入的是MySQLdb庫，但在Python3 中，MySQLdb 庫不再被廣泛支持。
        -   遷移指令：  
                `python manage.py makemigrations (APP_NAME)`
                `python manage.py migrate`
        - <tasksmanagement/setting.py> 修改
            -   在INSTALLED_APPS的list中加入我們APP（tasks）-> 告訴 Django在專案中包含這個應用程式，Django就會相應地加載和管理它。
            
            -   在開頭import os，以便進行下面操作
            
            -   TEMPLATE的 'DIRS': [os.path.join(BASE_DIR, 'templates')] -> 要渲染的HTML都放在'templates'目錄中，os.path.join(BASE_DIR, 'templates') 將構建出templates目錄的完整路徑
    
    2.  tasks目錄下的修改
        - <tasks/urls.py>
            -   根據新增的功能對應配置子路由
        - <tasks/models.py>
            -   在models.py中創建了一個新的模型用來存放Event的資訊
            -   Event继承自models.Model
            -   Data：
                    id是識別Event名稱的主鍵，Event的主鍵是唯一的
                    name是Event名稱，每個Event的name可以重複
                    label是Event的標籤，用於對Event進行分類
                    date是Event的日期
            -   Method：
                    def __str__(self) -> 當我們在shell中輸入Event.objects.all()時，我們希望返回事件
        - <tasks/template>
            -   新建了template的文件夾用來存放渲染的html
            -   首頁，包含了創建及查詢Event、以及跳轉到其他頁面的按鈕：create_event.html
                    可以通過輸入名稱（Name）、標籤（Label）、日期（Date）進行創建Event
                    可以在查詢欄輸入查詢之Event的標籤（Label）找到對應的Event
            -   分類表頁面： categorized_events.html
                    根據標籤（Label）進行分類並顯示在頁面
            -   進行删除Event的頁面： delete_event.html
                    可以點擊checkbox選擇Event，按下按鈕即可删除（可多選）
            -   進行Event內容修改的頁面： update_event.html
                    可以點擊checkbox選擇Event，在對應想修改內容的輸入框填寫新資訊，按下按鈕即可（僅單選），這裏只要輸入至少一個輸入框也可以修改對應資訊，若三個輸入框皆無填寫則網頁回應會顯示失敗訊息
        - <tasks/views.py>
            -   創建一個Class名為JumpToPage -> 實作跳轉頁面
                1.  `tocreate_event(request)`: 跳轉到/tasks/
                2.  `toupdate_event(request)`: 跳轉到/tasks/update_event
                3.  `todelete_event(request)`: 跳轉到/tasks/delete_event 
                4.  `get_all_events()`: 由於toupdate_event和todelete_event均使用了重複的函式去提取相同的Event，故在Class內直接定義一個Method實作提取資料的動作，這樣可使程式更容易維護
            -   創建一個Class名為EventManager -> 實作所有和Event管理相關的動作Method：
                1.  `create_event(request)`: 
                    目的：新增Event的Object並存到資料庫中
                    利用POST拿到首頁填寫創建Event的三項Data並賦值給name, label, date
                    進行邏輯判斷看三個Data是否都不為空
                    如果都不為空則把新創一個object到Event Class內，並且返回成功訊息
                    如果變數皆為空，則返回失敗的訊息。
                2.  `update_event(request)`:
                    目的：負責接收用戶提交的事件更新數據，將更新應用到數據庫中的相應事件，並返回相應的成功或失敗訊息給用戶
                    實作方法：
                    利用POST拿到更新Event頁面填寫創建Event的三項Data並賦值給name, label, date，並且還獲取事件的 ID
                    進行邏輯判斷看三個Data是否都不為空
                    如果至少一個不為空則通過事件的ID從數據庫中獲取相應的事件對象，
                    這裏使用get_object_or_404函數從資料庫中查詢指定ID的事件，如果找不到對應的事件，則返回 404 錯誤頁面，若找到則更新對應的Data並返回成功訊息
                    如果變數皆為空，則返回失敗的訊息
                3.  `delete_event(request)`: 
                    目的：實現了根據用戶提交的事件 ID，刪除數據庫中對應的事件的功能
                    實作方法：
                    利用POST拿到删除頁面中checkbox被選擇的events的id列表
                    遍歷這些Events的id，並根據每個id使用`Event.objects.filter(id=event_id).delete()`來從資料庫中刪除相應的事件
                    刪除操作完成後返回成功訊息
                    如果請求的方法不是POST，則直接返回，不執行任何操作
                4.  `categorized_events(request)`:
                    目的：按標籤（Label）分類事件並在網頁上顯示
                    實作方法：
                    通過`Event.objects.values_list('label', flat=True).distinct()`從數據庫中獲取所有不重複的標籤(label) 列表
                    創建了一個空字典categorized_events來存儲按標籤分類後的事件
                    之後再遍歷每個不重複的標籤，並將該標籤對應的事件過濾出來，存儲在 categorized_events中
                    分類好的事件傳遞給categorized_events.html，並將其作為 categorized_events的值，以供html使用。
                5.  `search_events(request)`:
                    目的：根據標籤(label) 進行事件搜索並在網頁上顯示搜索結果
                    實作方法：
                    利用GET取得在查詢輸入框所填寫的event_label
                    使用`Event.objects.filter(label__icontains=search_label)`從數據庫中過濾具有包含搜索標籤的事件
                    檢查是否有符合搜索標籤的事件
                    如果有符合，則使用列表推導式將搜索結果中每個事件的名稱、標籤和日期格式化為字符串，並使用<br>標籤連接起來，最後將其作為HTTP響應返回。
                    如果沒有符合搜索標籤的事件，則返回失敗訊息
                    如果請求方法不是GET，則什麼也不做

- 0417 by Sophie
    1. DB修改 : 由於Event增加新欄位Description作為備註，在migrate後資料庫更新為Django_SQL_0417.sql
    2. code修改
        - <tasks/urls.py> : 同上
        - <tasks/models.py>
            - Data：description是Event的備註說明
        - <tasks/template>
            - 首頁增加列出所有Event，方便之後修改個別Event，之後可整合到周檢視頁面
            - 列表頁面 : list_event.html
            - 查看/修改備註頁面 : event_detail.html
        - <tasks/views.py>
            - 在EventManager新增兩Method
            1. `list_event(request)` : 列出所有行程，無排序。點選查看，可進入個別Event備註頁面
            2. `update_event_detail(request, event_id)` : 可查看及更新備註內容
- 0419 by manchien
    1. code修改
        - <tasks/urls.py> : 增加register、login、logout的path
        - <tasks/templates/create_enent.html>：增加登出按鈕與"welcome 使用者"字樣，之後如果有主頁再修改到主頁
    2. tasks目錄下的新增
        - <tasks/templates/login.html>
        - <tasks/templates/register.html>
        - <tasks/auth_views.py>

- 0419 by xiaoqian
    1. code修改
        - <tasks/urls.py> : 增加week_events的path
        - <tasks/views.py>
            - 在EventManager新增一個Method
            1. `week_events(request)`： 獲取所有Event進行日期的排序，並分類到其所屬的週
        - <tasks/templates/create_event.html> : 加入週檢視按鈕
    2. tasks目錄下新增
        - <tasks/templates/week_events.html>
        - <tasks/week_events.py>

- 0419 by Sophie : 合併列表功能到周檢視，備註功能在周檢視頁面

- 0521 by SioWan : 
    1. code修改
        - <tasks/urls.py> : 增加了create_chart的path
        - <tasks/templates/create_event.html> : 加入統計圖按鈕
    2. tasks目錄下新增
        - <tasks/statistics.py>：根據chart_type的值生成統計圖，使用Event的Label作X值，從Event 模型中獲取所有不重複的Label並返回QuerySet，用迴圈計算對應事Label的數量存到statistics_events中（型別是Counter），創建了一個字典context，存取要傳遞給模板的數據。json.dumps() 方法將Python列表轉換為JSON字符串。
        - <tasks/templates/statistics.html>：引用了Chart.js library的 JavaScript 代碼，用於生成圖表。

- 0524 by Sophie:
    1. code修改
        - <taskmanagement/urls.py> : 首頁預設為登入介面
        - <tasks/auth_view.py> : Store user ID in session
        - <tasks/userinfo.py> : Customuser關掉email檢查Unique
        - <tasks/models.py> : 增加Friendship model
        - <tasks/views.py> : 增加friend_list, add_friend, list_users, user_ranking_by_last_login
    2. template修改
        - friend_list.html : 好友列表
        - list_users.html : 新增好友
        - create_event,html : 增加好友列表，增加好友
        - user_ranking.html : 新增排行榜
        - login.html, register.html : 新增引導至對方的連結
    3. migrate與資料庫更動
        ```sh
        # 1. sql更新
        Django_SQL_0523.sql
        ## 已新增3個users範例，請直接在login介面中登入
        ## username, password
        ## 1. Amy, 123
        ## 2. Betty, 123
        ## 3. Cindy, 123
        # 2. 視情況需要migrate
        python manage.py makemigrations # 可能不用
        python manage.py migrate # 可能不用
        # P.S. setting.py中password請修改為自己的密碼
        ```
- 0525 by SioWan:
    1. 修改Code
        - <tasks/statistics.py>：改成用Class
          a.StatisticManager Class
            createChart用來創建圖表的函數
            --> chart_type是圖表類型，預設值為Pie
            --> chart = Chart(chart_type)創建Chart Class的實例
            --> context = chart.get_context()調用Chart的method
            --> 最後回傳到模板
          b.Chart Class
            --> __init__構造函數，初始化圖表類型
            --> load_data是加載數據的方法，從Event中提取不同標籤及其計數
            --> get_context調用load_data加載數據，並返回包含labels、data和chart_type 的上下文字典，將數據轉換為JSON格式以便在模板中使用
        - <tasks/templates/statistics.html>：改了使用dataset和options
- 0530 by manchien
    1. 新增功能Todolist、diary 
        * 修改</tasks/userinfo.py>與</tasks/auth_views.py>、</tasks/templates/create_event.html>
        * 新增</tasks/templates/diary_list.html>、</tasks/templates/todo_list.html>       
      
- 0601 by Sherry : 修改email相關設定、新增番茄鐘、新增行事曆
    1. 安裝django-apscheduler
        - pip install django-apscheduler
        - python manage.py makemigrations
        - python manage.py migrate
        - 執行完資料庫中會新增'django_apscheduler_djangojob'、'django_apscheduler_djangojobexecution' 兩個table
        - 不知道是不是是背景執行的關係，reminder程式碼沒註解掉會影響migrate，所以我先註解掉

    2. 因為我們的data只有日期，所以時間表我就做成行事曆的樣式
       
- 0602 by xiaoqian : 共享行程、聊天室
    - python manage.py makemigrations
    - python manage.py migrate
    - (目前聊天室還沒辦法雙向...我盡力了QQ)
 
- 0603 by Sherry : 取消註解提醒功能
    - 如果還要 migrate 的話要註解掉 remider.py 再 migrate，不然會出錯
