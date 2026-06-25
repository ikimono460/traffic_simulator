---
type: Dataset
title: OSM地図データ (osm_map.md)
description: 秋田市中心部の道路・信号機情報を定義するOpenStreetMapデータ。
resource: city-akita/data/raw/akita_center.osm
tags: [data, osm]
timestamp: 2026-06-25T15:55:00+09:00
---

# OSM地図データ (osm_map.md)

本データセットは、秋田市中心部（山王十字路を含むエリア）の道路網、レーン数、交差点接続、信号機設定の元となるOpenStreetMap（OSM）データです。

## 基本情報

* **配置パス**: `city-akita/data/raw/akita_center.osm`
* **形式**: OSM XML形式
* **データソース**: [OpenStreetMap](https://www.openstreetmap.org/) (Overpass API 経由)

## 対象エリア（Bounding Box）

シミュレーションで切り出しているエリアの緯度経度範囲は以下の通りです：

* **南西端 (Min Lat, Min Lon)**: `(39.70151, 140.10277)`
* **北東端 (Max Lat, Max Lon)**: `(39.72087, 140.11950)`
* **Overpass bbox パラメータ**: `140.10277,39.70151,140.11950,39.72087`

## 取得・更新手順

OSMデータを再取得または最新状態に更新するには、以下のスクリプトを `city-akita` ディレクトリ直下で実行します。

```bash
python scripts/download_osm.py
```

* **スクリプト詳細**: `scripts/download_osm.py` は Overpass API のエンドポイント (`https://overpass-api.de/api/map`) にリクエストを送り、対象のバウンディングボックスの全データを取得して `data/raw/akita_center.osm` に保存します。
* **依存関係**: `requests` パッケージが必要です。

## 次のステップへの繋がり

* 本データは、`network/build_network.py` スクリプトの入力として使われ、SUMO用の道路網ファイルである `akita.net.xml` のビルドに使用されます。詳細は [SUMO道路網の構築](../network/road_network.md) を参照してください。
