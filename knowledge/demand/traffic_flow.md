---
type: TrafficDemand
title: 断面交通量とルート・フロー需要 (traffic_flow.md)
description: 秋田県警の断面交通量オープンデータからシミュレーション用フローを生成するプロセスの詳細。
resource: city-akita/demand/akita.rou.xml
tags: [demand, route, flow, sumo]
timestamp: 2026-06-25T15:55:00+09:00
---

# 断面交通量とルート・フロー需要 (traffic_flow.md)

本ドキュメントは、秋田県警から提供される断面交通量データ（CSV）から、SUMOのシミュレーションに入力される交通需要ファイル（`akita.rou.xml`）を生成するアルゴリズムおよび実行方法についての解説です。

## 基本情報

* **交通需要ファイル**: `city-akita/demand/akita.rou.xml`
* **変換スクリプト**: `city-akita/scripts/process_traffic.py`
* **入力データソース**: 
  * `city-akita/resources/typeB_akita_2026_04/秋田県警_202604.csv` (断面交通量データ)
  * `city-akita/data/match_table.json` (交差点マッピングテーブル)

## 断面交通量データ仕様

断面交通量データCSVは、5分ごとに各リンク（車線方向）を通過した車両台数を記録しています。

* **時刻形式**: `YYYY/MM/DD HH:MM`（例: `2026/04/08 08:00`）
* **主な列**: `時刻`, `リンク番号`, `断面交通量`

## 経路（Route）およびフロー（Flow）の生成アルゴリズム

`scripts/process_traffic.py` は、以下のロジックで車流量をSUMOの移動モデルにマッピングします。

### 1. ネットワーク境界（出口）の探索
SUMOの道路網（`akita.net.xml`）上で、それ以上先に接続するエッジが存在しない道路の端点（`boundary_edges`）を、車両の最終到達目的地（出口）候補としてリストアップします。

### 2. 時刻フィルタリング
コマンドライン引数で指定された日付・開始時間から1時間（デフォルト）のデータをCSVから抽出し、リンク番号ごとの総交通量（台数）を合算します。

### 3. 最短経路検索によるルート分配（Route Distribution）
各交差点の流入リンク（SUMO流入エッジ）に対して、以下の割り当てを行います。
* **主要目的地（出口）への到達が可能な場合**:
  流入エッジから各境界エッジ（目的地）までの最短経路（`ShortestPath`）を探索します。
  到達可能な経路が複数存在する場合、確率を均等に割り振った `<routeDistribution>` を定義し、車両の最終目的地を分散させます。
* **到達可能な境界エッジがない場合（クローズドなループ等）**:
  交差点の直近にある流出エッジへの短いフォールバック経路を自動検索して割り当てます。

### 4. フロー設定の書き出し
合算した交通台数を `number` 属性にセットし、シミュレーション開始時間から終了時間にかけて車両を発生させる `<flow>` タグを生成します。

```xml
<!-- ルート分配の例 -->
<routeDistribution id="dist_29_548">
    <route edges="edge1 edge2 edge_exitA" probability="0.5000"/>
    <route edges="edge1 edge3 edge_exitB" probability="0.5000"/>
</routeDistribution>

<!-- フロー生成の例 -->
<flow id="flow_29_548" route="dist_29_548" type="car" begin="0" end="3600" number="450" departLane="free" departSpeed="max" />
```

## 車両モデル定義 (`vType`)

生成される `akita.rou.xml` の先頭には、日本の一般的な乗用車の走行特性や車線変更特性（Lane-changing behaviors）を反映した以下のモデルタイプ定義が付与されます。

* **アタッチされるID**: `car` (guiShape: `passenger`)
* **パラメータ設定**:
  * 加減速性能: `accel="2.6" decel="4.5"`
  * 車両間最小ギャップ: `minGap="2.5"` (横方向 `minGapLat="0.6"`)
  * 最大速度: `maxSpeed="13.89"` (約 50 km/h)
  * 車線変更協調性: `lcCooperative="1.0" lcSpeedGain="1.0" lcStrategic="1.0"` (車線変更を円滑に行う協調パラメータ)

## 需要データの生成手順

再現したい日付と開始時（24時間表記）を引数に指定して実行します。

```bash
# 例: 2026年4月8日 朝 8:00 〜 9:00 の交通需要を生成する
python scripts/process_traffic.py 2026/04/08 8
```

実行が完了すると、`demand/akita.rou.xml` が最新の需要で上書き生成されます。
