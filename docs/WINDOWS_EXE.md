# Windows双击启动版

双击MEGA_Tool_Windows.exe。启动器会先启动本地服务，待就绪后自动打开浏览器；窗口中的“打开阅读器”可重新打开网页。阅读期间保留启动器窗口，完成后关闭它或点击“退出”。关闭浏览器标签不会退出服务。

这是文件夹式便携版本，运行时无需安装Python。保留exe、_internal、app.py、data和.streamlit的完整目录；复制到别处时复制整个文件夹。

放在原MEGA_Tool项目的dist目录内时，优先使用原项目中的语料、人工审核和PDF，继续已有24条确认。移到独立目录后使用随包84组样本；个人审核记录和PDF不随包分发。新确认写入该副本的data/reviews.json。原页预览可将对应PDF放在Asset_by_user，或依照local_sources.example.json建立local_sources.json。来源哈希仍核验。

默认地址http://127.0.0.1:8501/。如果端口已被其他程序占用，启动器选择空闲端口并打开正确地址，窗口内显示实际地址。同一研究目录重复双击会打开已有服务，不重复启动。

网页出现“拒绝连接”时，先打开exe，待窗口显示“已启动”后点击“打开阅读器”。运行日志在所用研究目录的tmp/desktop；启动器异常日志在Windows临时目录MEGA_Tool-launcher-error.log。将整个便携目录放在可写文件夹内，例如文档或桌面。

开发者重建：在项目环境安装requirements-build.txt，运行python scripts/build_windows.py。构建工具采用PyInstaller的文件夹模式：https://www.pyinstaller.org/en/stable/usage.html 。服务限本机访问；启动器只关闭自己创建的进程树，未修改原语料或审核记录。

原项目也可双击根目录“打开巴黎手稿”快捷方式；它指向dist内的exe。

本次验收（2026-10-07）：完整100测试通过，实际exe在本机Windows独立中文目录中启动，运行不调用外部Python；端口占用回退、重复双击和退出通过。未配置PDF的便携副本可正常阅读84组样本；原项目保留24条人工确认，并验证原页图像、跨页引用及对读跳转。其他Windows机器仍需实际运行验证。
