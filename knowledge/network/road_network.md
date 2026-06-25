---
type: SUMONetwork
title: SUMO道路網データの構築 (road_network.md)
description: OSMデータから左側通行、パッチ適用を含めてSUMO道路網ファイル（.net.xml）をコンパイルする処理。
resource: city-akita/network/akita.net.xml
tags: [network, sumo, netconvert]
timestamp: 2026-06-25T15:55:00+09:00
---

# SUMO道路網データの構築 (road_network.md)

本ドキュメントは、生のOpenStreetMap（OSM）ファイルから、日本仕様（左側通行）および実世界のレイアウト修正を適用したSUMO道路網ファイル（`akita.net.xml`）を生成するビルドプロセスについての解説です。

## 基本情報

* **道路網ファイル**: `city-akita/network/akita.net.xml`
* **ビルドスクリプト**: `city-akita/network/build_network.py`
* **ビルドツール**: SUMO付属 `netconvert` ツール

## 道路網ビルドコマンドと引数

`network/build_network.py` は、内部で SUMO の `netconvert` を呼び出し、以下の重要なオプションを適用してビルドを行います。

```bash
netconvert \
  --osm-files data/raw/akita_center.osm \
  -o network/akita.net.xml \
  --lefthand \
  --geometry.junction-mismatch-threshold 20 \
  --tls.discard-simple true \
  --tls.join true \
  --no-turnarounds \
  --junctions.join \
  --keep-edges.by-vclass passenger
```

### 重要パラメータの役割
* `--lefthand`: 日本の交通ルールに合わせ、車両を**左側通行**に設定します（極めて重要）。
* `--keep-edges.by-vclass passenger`: 乗用車（passenger）が通行可能な道路のみを抽出し、歩行者専用道路や線路などを排除してネットワークを軽量化します。
* `--tls.join` & `--junctions.join`: 近接する交差点や信号を一つに結合し、現実的な交差点グループ（クラスタ）としてまとめます。

## パッチ適用メカニズム

OSMからの自動変換だけでは、交差点の右左折レーン接続や信号の有無が実世界と異なる場合があります。これを非破壊的かつ再現可能に修正するため、`data/patch/` ディレクトリ内に配置された以下のXMLパッチファイルをビルド時に動的に検出して適用します。

| オプション | パッチファイルパス | 用途 |
|---|---|---|
| `--connection-files` | `data/patch/connections.con.xml` | レーン同士の右左折・直進の接続関係の明示的修正（右折専用レーンなど） |
| `--node-files` | `data/patch/nodes.nod.xml` | 交差点ノードの制御タイプ（信号あり/なし、優先道路）の上書き |
| `--edge-files` | `data/patch/edges.edg.xml` | 道路（エッジ）の車線数や制限速度の上書き |
| `--tfl-files` | `data/patch/traffic_lights.tfl.xml` | 信号機のフェーズ・定義の明示的な割り当て |

## ビルド・更新手順

1. パッチファイルを `city-akita/data/patch/` 内に記述または追加します。
2. 以下のコマンドを `city-akita` ディレクトリ内で実行します。

```bash
python network/build_network.py
```

ビルドが成功すると、`network/akita.net.xml` が更新され、SUMO-GUIやシミュレーション実行スクリプトでロード可能な状態になります。
また、地図や道路網を更新した場合は、必ず [交差点紐付け](../data/intersections.md) の再構築スクリプト（`python scripts/match_network.py`）を実行してください。
