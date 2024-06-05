README.md

- installation setup
    - 本地端程式使用雲端資料庫PostgreSQL
        1.  設置一個 Python 虛擬環境。(python版本3.11) 
        2.  切換到/taskmanagement_deploy
        3.  使用 pip install -r requirements.txt 安裝所需的套件。
            *如果是MAC 要先brew install postgresql
        4.  執行 python manage.py runserver 啟動伺服器，以啟動應用程序。
    - 本地端程式使用本地端資料庫MySQL
        1.  設置一個 Python 虛擬環境。(python版本3.11) 
        2.  切換到/taskmanagement
        3.  使用 pip install -r requirements.txt 安裝所需的套件。
        4.  下載並使用 MySQL 執行提供的 SQL 腳本來設置資料庫。
        5.  在 Django  setting.py中配置資料庫連接。
        6.  執行 python manage.py makemigrations 和 python manage.py migrate 來設置資料庫模式。
        7.  使用 python manage.py runserver 啟動伺服器，以啟動應用程序。

- file organization
    ```
    taskmanagement_deploy
    ├── db.sqlite3
    ├── diary_images
    │   └── 水.jpg
    ├── manage.py
    ├── media
    │   └── diary_images
    │       └── water.jpg
    ├── requirements.txt
    ├── taskmanagement
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   ├── __init__.cpython-39.pyc
    │   │   ├── settings.cpython-39.pyc
    │   │   ├── urls.cpython-39.pyc
    │   │   └── wsgi.cpython-39.pyc
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── tasks
        ├── __init__.py
        ├── __pycache__
        │   ├── __init__.cpython-39.pyc
        │   ├── admin.cpython-39.pyc
        │   ├── apps.cpython-39.pyc
        │   ├── auth_views.cpython-39.pyc
        │   ├── calendar.cpython-39.pyc
        │   ├── chat.cpython-39.pyc
        │   ├── email.cpython-39.pyc
        │   ├── forms.cpython-39.pyc
        │   ├── models.cpython-39.pyc
        │   ├── pomodoro.cpython-39.pyc
        │   ├── reminder.cpython-39.pyc
        │   ├── share.cpython-39.pyc
        │   ├── statistics.cpython-39.pyc
        │   ├── urls.cpython-39.pyc
        │   ├── userinfo.cpython-39.pyc
        │   ├── views.cpython-39.pyc
        │   └── week_events.cpython-39.pyc
        ├── admin.py
        ├── apps.py
        ├── auth_views.py
        ├── calendar.py
        ├── chat.py
        ├── email.py
        ├── forms.py
        ├── migrations
        │   ├── 0001_initial.py
        │   ├── __init__.py
        │   └── __pycache__
        │       ├── 0001_initial.cpython-39.pyc
        │       └── __init__.cpython-39.pyc
        ├── models.py
        ├── pomodoro.py
        ├── reminder.py
        ├── share.py
        ├── static
        │   └── alarmclock.mp3
        ├── statistics.py
        ├── templates
        │   ├── calendar.html
        │   ├── categorized_events.html
        │   ├── chat_detail.html
        │   ├── chat_list.html
        │   ├── chat_room.html
        │   ├── create_event.html
        │   ├── delete_event.html
        │   ├── diary_list.html
        │   ├── event_detail.html
        │   ├── event_list_for_sharing.html
        │   ├── friend_list.html
        │   ├── list_event.html
        │   ├── list_users.html
        │   ├── login.html
        │   ├── pomodoro.html
        │   ├── register.html
        │   ├── reminder_email.html
        │   ├── select_sharee.html
        │   ├── share_event.html
        │   ├── shared_events.html
        │   ├── signup_success_email.html
        │   ├── statistics.html
        │   ├── todo_list.html
        │   ├── update_event.html
        │   ├── user_ranking.html
        │   └── week_events.html
        ├── tests.py
        ├── urls.py
        ├── userinfo.py
        ├── views.py
        └── week_events.py
    12 directories, 80 files
    ```
    以下是比較主要的File或directories描述：
    - /taskmanagement_deploy/manage.py：是將來要操作Django的一個元件
    - /taskmanagement_deploy/taskmanagement
        1. init.py
        2. settings.py：settings掌管了整個專案的運作，包括專案使用哪一個的資料庫。
        3. url.py：定義了特定URL模式和相應視圖函數之間的映射列表。
        4. wsgi.py：WSGI則是扮演著web server與web application之間溝通的一個介面
    - /taskmanagement_deploy/task:在這個目錄下會有migrations,static,templates和所有的python檔
        1. migrations:進行資料遷移後生成的檔案，定義了即將要在資料庫執行的動作。
           當執行migrate指令，則會依照此檔案，同步models.py中所建立的類別到我們的資料庫中。
        2. static:開發時用來放置靜態檔的目錄，裏面放有alarmclock.mp3
        3. templates：存放了所有客製化頁面顯示的html檔，用作給Django進行渲染的。
        4. python檔：各項功能的程式碼及urls.py定義了特定URL模式和相應視圖函數之間的映射列表。
        
