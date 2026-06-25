---
type: DirectoryIndex
title: データ管理インデックス
description: プロジェクトで使用するOpenStreetMapデータや実交差点データなどの各種データ定義のインデックス。
timestamp: 2026-06-25T15:55:00+09:00
---

# データ管理インデックス

本フォルダは、秋田市中心部のシミュレーションで必要とされる各種データソース（OpenStreetMapからの地図データ、県警の交差点・交通量オープンデータ、それらを紐付けるマッピングデータ）についての知識ドキュメントを管理しています。

## 構成コンセプト

* [OSM地図データ (osm_map.md)](osm_map.md): OpenStreetMapからダウンロードした生データと取得手順。
* [交差点データとマッピングテーブル (intersections.md)](intersections.md): 実世界の交差点データ（断面交通量観測点）とSUMOノードの紐付けテーブル。

## データフォルダの物理構成
* `city-akita/data/raw/akita_center.osm`: 対象エリアの生のOSMデータ。
* `city-akita/data/raw/intersections.csv`: 秋田県警の交通情報オープンデータに対応する主要交差点の緯度経度リスト。
* `city-akita/data/match_table.json`: 実世界の交差点IDと、SUMO上のジャンクション（ノード）IDとのマッピング定義。
