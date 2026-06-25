---
type: DirectoryIndex
title: 交通需要関連インデックス
description: 実世界の断面交通量データからSUMO用のルート・フロー定義を生成するプロセスのインデックス。
timestamp: 2026-06-25T15:55:00+09:00
---

# 交通需要関連インデックス

本フォルダは、実世界（秋田県警オープンデータ）の交差点別「断面交通量」をシミュレーション上の車両の発生・移動（ルートおよびフロー定義）へと変換・反映するための知識ドキュメントを管理しています。

## 構成コンセプト

* [断面交通量とルート・フロー需要 (traffic_flow.md)](./traffic_flow.md): オープンデータのフォーマット、車両フロー算出、`akita.rou.xml` の生成ロジックの説明。

## 交通需要フォルダの物理構成
* `city-akita/demand/akita.rou.xml`: 生成されたSUMO用ルート・フロー定義ファイル（シミュレーション入力用）。
* `city-akita/scripts/process_traffic.py`: 断面交通量CSVを解析し、需要ファイルを生成する変換スクリプト。
* `city-akita/resources/typeB_akita_2026_04/`: 断面交通量データCSVが格納されたディレクトリ。
