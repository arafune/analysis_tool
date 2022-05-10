# PES module

自分のため。

## Active Library

* calib1d.py: 2D detecterのキャリブレーションデータ成形用。
* lpes_basic.py: 波長->エネルギー変換等、基本的な関数
* parabolaband.py: 電子の静止質量を単位としたパラボリックバンド
* prodigy_util: PHOIBOSシステムのデータローダ。
* SPD_main.py: pyarpes 用のPHOIBOSシステム・エンドステーション・クラス。prodigy_util.pyと共につかう。

## Obsolute LIbrary

使わないけど、スニペットとしては使えるかもしれないのでとっておく。Git 管理だから消しちゃえば？という考えもあるけど。

* splab.py: SPLabのファイルローダ
* arpes.py: APRESデータのプロット。さすがに pyarpesの方が便利。pyarpesの不安定性を考えても、xarrayベースで取り扱う方が、いろいろとスマートなので、（NDArrayベースのこのライブラリは使わない）

## Todo

* 複数の angle resolved data を一つにまとめる。
  * 各データの角度は同じステップ だけど、試料を回して測定したデータセットもまとめてバンドとかにしたい。⇒単純に二つのデータセットをくっつける、じゃだめ。
    * シンプルには、重なる角度があるように測定する（はずな）ので（それを元にデータを補間するのが良いんですかね）
