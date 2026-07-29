---
type: SimulationEvaluation
title: シミュレーション評価指標と計測車両 (evaluation.md)
description: 交通渋滞の客観的評価指標（平均速度グラフ・車両数推移グラフ）および計測用車両（プローブカー）の設定と解析手順。
resource: city-aomori/sim/aomori.sumocfg
tags: [evaluation, probe_car, metrics, visualization, python]
timestamp: 2026-07-29T20:33:00+09:00
---

# シミュレーション評価指標と計測車両 (evaluation.md)

本ドキュメントは、SUMO交通シミュレーションにおける条件変更（交差点パッチ適用前後やレーン変更パラメータの調整など）の効果を客観的に評価するための「グラフ出力」および「計測用車両（プローブカー）」の仕様と実行手順について記述したナレッジです。

---

## 1. 評価指標とグラフ仕様

交通流の改善効果を定量的かつ視覚的に把握するため、2種類のグラフおよびプローブカーの旅行時間を評価指標として採用しています。

### 案A：ネットワーク全体の平均走行速度の推移（折れ線グラフ）
* **データソース**: `output/summary.xml` の `meanSpeed` 属性
* **単位**: km/h（m/s × 3.6 で換算）
* **目的**: シミュレーション経過時間（0〜3600秒）ごとのネットワーク全体における平均速度を可視化します。渋滞の発生・進行・解消の挙動が一目で把握できます。

### 案B：走行車両数と停止車両数の推移（積み上げ面グラフ）
* **データソース**: `output/summary.xml` の `running` および `halting` 属性
* **目的**: ネットワーク内の「走行中の車両数（青）」と「停止・渋滞中の車両数（赤）」の推移を表示します。デッドロックや滞留車両の蓄積の度合いを客観評価できます。

### プローブカー（計測用車両）の旅行時間計測
* **データソース**: `output/tripinfo.xml` の `duration` および `timeLoss` 属性
* **目的**: 固定のOD（出発地・目的地）を一定の時刻に走行する1台の計測用車両を投入し、その車両の「総所要時間（Travel Time）」および「渋滞による損失時間（Time Loss）」を計測します。ユーザー視点での実効的な改善効果を評価できます。

---

## 2. 構成ファイルと設定

### 2.1 プローブカーの定義 (`city-aomori/demand/probe_vehicle.rou.xml`)

青森市立甲田小学校前付近から青森県庁前付近へ向かう計測車両を定義しています。

* **出発地エッジ**: `110011449#0`（x: 791.09, y: 650.19 付近）
* **目的地エッジ**: `86199509#5`（x: 1212.41, y: 1727.43 付近）
* **出発時刻**: 600秒（シミュレーション開始10分後）
* **車両ID**: `probe_car_1`（車体色: 赤 `color="1,0,0"`）

```xml
<routes>
    <trip id="probe_car_1" depart="600" from="110011449#0" to="86199509#5" color="1,0,0"/>
</routes>
```

### 2.2 シミュレーション出力設定 (`city-aomori/sim/aomori.sumocfg`)

`aomori.sumocfg` の `<input>` に `probe_vehicle.rou.xml` を追加し、`<output>` ブロックでログを出力させています。

```xml
<configuration>
    <input>
        <net-file value="../network/aomori.net.xml"/>
        <route-files value="../demand/aomori.rou.xml,../demand/probe_vehicle.rou.xml"/>
    </input>
    ...
    <output>
        <summary-output value="../output/summary.xml"/>
        <tripinfo-output value="../output/tripinfo.xml"/>
    </output>
</configuration>
```

### 2.3 解析およびグラフ生成スクリプト (`city-aomori/scripts/plot_results.py`)

`output/summary.xml` と `output/tripinfo.xml` をパースし、以下を出力します：
1. **コンソール出力**: `probe_car_1` の所要時間（分・秒）と損失時間（分・秒）
2. **`output/graph_a_avg_speed.png`**: 平均速度推移グラフ
3. **`output/graph_b_vehicle_counts.png`**: 車両数推移グラフ

---

## 3. 再現・評価実行手順

シミュレーションのバックグラウンド実行から結果表示までの一連の手順は以下の通りです。

```bash
# 1. city-aomori ディレクトリに移動
cd city-aomori

# 2. CUI非GUIモードでシミュレーションを実行（--threads 8 で高速化）
python -u sim/run_simulation.py 2026/05/08 8 --nogui

# 3. 解析スクリプトを実行してプローブカーのタイム表示とグラフ出力
python scripts/plot_results.py
```
