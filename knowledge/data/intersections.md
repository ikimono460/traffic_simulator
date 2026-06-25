---
type: Dataset
title: 交差点データとマッピングテーブル (intersections.md)
description: 実世界の交差点データ（断面交通量観測点）とSUMOノードのマッピング構成。
resource: city-akita/data/match_table.json
tags: [data, intersection, mapping]
timestamp: 2026-06-25T15:55:00+09:00
---

# 交差点データとマッピングテーブル (intersections.md)

本データセットは、秋田県警から提供される実世界の「断面交通量」および「信号情報」オープンデータの交差点と、SUMO上の道路ネットワーク上の交差点ノード（Junction）およびレーン（Edge）を紐付けるための中心的なマッピングデータです。

## 基本情報

* **マッピング定義ファイル**: `city-akita/data/match_table.json`
* **実交差点位置リスト**: `city-akita/data/raw/intersections.csv`
* **紐付け生成スクリプト**: `city-akita/scripts/match_network.py`
* **交差点定義オープンデータ**: `city-akita/resources/typeC_akita_2026_04/秋田県警_定義_202604.csv`

## データ構造概要

`match_table.json` は、実世界の交差点番号（キー）ごとに以下の情報を保持するJSONオブジェクトです。

### 主要なプロパティ

* `sumo_junction_id`: SUMO上の信号交差点のノードID（Junction ID）。
* `lat`, `lon`: 実世界における交差点の緯度経度。
* `incoming_links`: 県警データ上の「流入方向リンクID」と、SUMO上の「流入エッジID（Edge ID）」のマッピング辞書。
* `outgoing_links`: 県警データ上の「流出方向リンクID」と、SUMO上の「流出エッジID（Edge ID）」のマッピング辞書。
* `all_sumo_incoming`: 交差点に流入するすべてのSUMOエッジのリスト。
* `all_sumo_outgoing`: 交差点から流出するすべてのSUMOエッジのリスト。

### データ例（山王十字路付近の例）

```json
"29": {
    "sumo_junction_id": "cluster_1332330172_9242143122",
    "lat": 39.70334829,
    "lon": 140.10504384,
    "incoming_links": {
        "548": "-1001269102",
        "54": "1001269099#3",
        "248": "1001269103",
        "6": "376882518#4"
    },
    "outgoing_links": {
        "49": "-376882518#4",
        "549": "1001269101",
        "7": "1001269102",
        "239": "640595612#0"
    },
    "all_sumo_incoming": [
        "-1001269102",
        "1001269099#3",
        "1001269103",
        "376882518#4"
    ],
    "all_sumo_outgoing": [
        "-376882518#4",
        "1001269101",
        "1001269102",
        "640595612#0"
    ]
}
```

## マッピング生成アルゴリズム

`scripts/match_network.py` は、以下のロジックで自動紐付けを行います：

1. **実交差点の座標読み込み**: `intersections.csv` から対象エリア内の実交差点情報（番号・緯度経度）を取得。
2. **SUMOノードのロード**: `network/akita.net.xml` から信号機設定を持つノード（`type="traffic_light"`）のXY座標を抽出し、緯度経度に逆変換。
3. **最近傍探索とマッチング**: 各実交差点の座標から一定距離以内（閾値: 70m）にあるSUMOの信号交差点を探し、最も近いノードと紐付け。
4. **リンク紐付けの初期推定**: `秋田県警_定義_202604.csv` に定義されているリンク数に応じて、ノードに接続するSUMOエッジを順番にマッピング。

## 手動微調整とパッチ適用

自動推定でのリンク紐付けが間違っている場合、または実世界の対応関係とずれている場合は、`data/match_table.json` を直接編集して、正しいエッジIDを割り当ててください。
※詳細な修正とビルドの手順は [調整プレイブック](../playbooks/signal_tuning.md) に記載されています。
