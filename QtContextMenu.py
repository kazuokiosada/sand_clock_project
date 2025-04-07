"""
PyQtを使用して、ウィンドウのどこかをマウスで右クリックしたときにプルダウンメニュー（コンテキストメニュー）を表示し、アクションを選択できるようにするには、以下の手順を実行します。

1.  **コンテキストメニューの作成:**
    * `QMenu`クラスを使用してコンテキストメニューを作成します。
    * `addAction()`メソッドを使用して、メニューにアクションを追加します。

2.  **マウスイベントの処理:**
    * `mousePressEvent()`メソッドをオーバーライドし、マウスの右クリックを検出します。
    * 右クリックされたら、コンテキストメニューを表示します。

3.  **アクションの処理:**
    * メニューでアクションが選択されたときに実行されるスロット（関数）を定義します。
    * `triggered`シグナルをスロットに接続します。

以下に、具体的なコード例を示します。

```python"
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMenu
from PyQt5.QtCore import Qt, QPoint

class ContextMenuWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('コンテキストメニュー')
        self.show()

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        action1 = context_menu.addAction("アクション1")
        action2 = context_menu.addAction("アクション2")
        action3 = context_menu.addAction("アクション3")
        exit_action = context_menu.addAction("終了")
        exit_action.triggered.connect(QApplication.quit) # 終了アクション
        
        action1.triggered.connect(self.action1_triggered)
        action2.triggered.connect(self.action2_triggered)
        action3.triggered.connect(self.action3_triggered)

        context_menu.exec_(self.mapToGlobal(event.pos()))

    def action1_triggered(self):
        print("アクション1が選択されました")

    def action2_triggered(self):
        print("アクション2が選択されました")

    def action3_triggered(self):
        print("アクション3が選択されました")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ContextMenuWidget()
    sys.exit(app.exec_())
"""
```

**コードの説明:**

1.  **`ContextMenuWidget`クラス:**
    * `QWidget`を継承し、コンテキストメニューを表示するカスタムウィジェットを作成します。
2.  **`contextMenuEvent(self, event)`メソッド:**
    * ウィジェット上でコンテキストメニューを表示するイベントが発生したときに呼び出されます。
    * `QMenu`オブジェクトを作成し、`addAction()`メソッドでメニュー項目を追加します。
    * 各アクションの`triggered`シグナルを、対応するスロット（`action1_triggered`など）に接続します。
    * `exec_()`メソッドでコンテキストメニューを表示します。`self.mapToGlobal(event.pos())`で、マウスカーソルの位置をグローバル座標に変換し、メニューを表示する位置を指定します。
3.  **`action1_triggered(self)`などのスロット:**
    * メニュー項目が選択されたときに実行される処理を記述します。ここでは、選択されたアクションの名前をコンソールに出力しています。

**ポイント:**

* `contextMenuEvent()`メソッドは、ウィジェットのコンテキストメニューを表示するイベントを処理します。
* `QMenu`クラスを使用して、コンテキストメニューを作成します。
* `addAction()`メソッドを使用して、メニュー項目を追加します。
* `triggered`シグナルを使用して、メニュー項目が選択されたときに実行される処理を定義します。
* `exec_()`メソッドを使用して、コンテキストメニューを表示します。

このコードを実行すると、ウィンドウ内で右クリックしたときにコンテキストメニューが表示され、メニュー項目を選択すると対応する処理が実行されます。
"""