module Settings
	UploaderName	= "Uploader"

	# ファイルを保存するディレクトリの名前
	# chmod 777 パーミッション許可の必要があります。
	Storage_Dir	= "./storage/"

	# アップロードなどの操作の後、リダイレクションするファイル。
	# 基本的にはアップローダのフロントページにしておくのが吉(変えないほうが良い)
	RedirectDestination = "./uploader_frontpage.cgi"

	# アップロードされたファイルの情報を記録しておくファイルの場所および名前。
	LogFile		= "./storage/uploader_log.yml"

	# 変更しないほうがいいです。
	UploadForm	= "./uploader_2.html"

	# アップロード可能ファイルのサイズ上限
	# 上限を設けないときは nil
	LimitFileSize	= 1024 * 1024	#bytes

	# もしアップローダから「戻る」ボタンが必要な時、このアドレスを指定しておけばそこに飛びます。
	# 必要なければnilでok
	ParentPage	= nil	# "www.yahoo.co.jp"
	
	# アップロードを許可しないファイルの拡張子。
	# cgiとかで使われるスクリプトはアップしてしまうと開くときにサーバに間違って実行されかけて、
	# その後実行パーミッションがないということで落ちてしまうので、cgiスクリプトとして使われる一連の拡張子をここに設定しておくのがよい。
	Restrict_Ext	= ["rb", "cgi", "pl", "php"]

	# ファイルにカテゴリを指定することができます。それによって、表示するときにフィルタできます。
	# 以下にカテゴリ名を配列の形で。
	CategoryName 	= [
		"C/C++",
		"Haskell",
		"Lisp",
		"Ruby",
		"Others"
	]
end
