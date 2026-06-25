---
type: DirectoryIndex
title: 道路網関連インデックス
description: SUMO用道路ネットワークの生成とパッチ適用プロセスのインデックス。
timestamp: 2026-06-25T15:55:00+09:00
---

# 道路網関連インデックス

本フォルダは、ダウンロードしたOpenStreetMap（OSM）データから、SUMOのシミュレーションで使用可能な道路ネットワーク定義（.net.xml）を構築するための知識ドキュメントを管理しています。

## 構成コンセプト

* [SUMO道路網データの構築 (road_network.md)](road_network.md): netconvertを用いたビルド処理および手動パッチ適用の説明。

## ネットワークフォルダの物理構成
* `city-akita/network/akita.net.xml`: コンパイルされたSUMO道路網ファイル。
* `city-akita/network/build_network.py`: OSMデータから道路網を生成するビルドスクリプト。
* `city-akita/data/patch/nodes.nod.xml`: 信号機の有無やタイプを上書きするためのパッチ。
* `city-akita/data/patch/connections.con.xml`: 右左折レーン接続関係を上書きするためのパッチ。
