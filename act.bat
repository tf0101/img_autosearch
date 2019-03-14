@echo off
rem システム環境変数に　C:\Users\〇〇〇〇\Anaconda3\Scripts を追加することで
rem windousのコマンドラインからAncondaのプロンプトを操作できる、これによりancondaの環境をbatファイルから弄れるようになる
rem activate "Ancondaで構築した環境名"　で環境を起動する　その後コードのあるディレクトリに移動してstartauto.batを実行すると自動処理が実行される


call activate tensor-cpu 
call cd img_auto_search_end
call startauto.bat
pause >nul
