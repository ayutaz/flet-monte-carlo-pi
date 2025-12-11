Monte Carlo π 可視化 (Flet)
============================

概要
----
- Flet を使ったモンテカルロ法の円周率近似デモ。乱数打点を高速で回し、推定値の推移をリアルタイム表示します。
- Python 3.12 を uv で固定し、依存は `flet==0.28.3` のみです。

セットアップ
------------
1. プロジェクト直下で依存を同期（初回のみ）  
   `UV_CACHE_DIR=.uvcache uv sync`
2. 仮想環境に入る場合（任意）  
   `source .venv/bin/activate`

実行
----
- 仮想環境を有効化: `source .venv/bin/activate`
- デスクトップ表示: `flet run main.py`
- ブラウザ表示: `flet run --web main.py`（表示された URL を開く）

使い方
------
- Start / Stop で打点を開始・停止、Reset で初期化。
- グラフは推定値の履歴を表示（最大800点を保持）。
- Webモードのままにすれば Qiita 読者がブラウザで体験できます。

Zabbix 連携メモ
---------------
- `on_tick` 内で得た推定値 `est` を `subprocess.run(["zabbix_sender", "-z", "<server>", "-s", "<host>", "-k", "mo_pi_gui", "-o", str(est)])` のように送れば、既存のアイテムやトリガーに流用可能です。
