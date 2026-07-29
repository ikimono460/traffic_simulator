---
type: Playbook
title: 指定道路のピンポイント通行止め手順 (road_closure.md)
description: シミュレーション実行中に特定道路の通行止めおよび解除を行う動的制御設定（data/road_closures.json）の指定・運用手順。
resource: city-aomori/data/road_closures.json
tags: [playbook, road_closure, traci, sumo, python]
timestamp: 2026-07-29T21:00:00+09:00
---

# 指定道路のピンポイント通行止め手順 (road_closure.md)

本ドキュメントは、SUMOシミュレーションの実行中に、工事・事故・イベント等による「特定の道路のピンポイント通行止め」および「時間指定による通行止め解除」を行うための設定方法と運用手順について解説したプレイブックです。

---

## 1. 設定方法 (`city-aomori/data/road_closures.json`)

`city-aomori/data/road_closures.json` ファイルを作成・編集することで、コードを変更することなく柔軟に通行止めを設定できます。

### 1.1 設定ファイルの例

```json
[
  {
    "name": "事故による一時通行止め（道路ID直接指定）",
    "edges": ["958818105#6", "-958818105#6"],
    "start_time": 300,
    "end_time": 2700
  },
  {
    "name": "甲田小学校前の工事規制（座標指定）",
    "coordinates": {"x": 791.09, "y": 650.19},
    "radius": 30.0,
    "both_directions": true,
    "start_time": 600,
    "end_time": 1800
  }
]
```

### 1.2 設定パラメータ仕様

| 項目 | 型 | 必須 | 説明 |
| :--- | :--- | :--- | :--- |
| `name` | 文字列 | 任意 | 通行止めの名称・理由（シミュレーションログに出力されます） |
| `edges` | 配列 | 選択 | 通行止めにするSUMOのエッジIDリスト（例: `["958818105#6", "-958818105#6"]`） |
| `coordinates` | オブジェクト | 選択 | SUMO内の座標 `{"x": ..., "y": ...}`。指定した場合、最寄りの道路を自動検出します |
| `radius` | 数値 | 任意 | 座標指定時の最寄り道路の検索半径（メートル、デフォルト: 30m） |
| `both_directions`| ブール値 | 任意 | 座標指定時、反対車線のエッジも自動で同時に通行止めにするか（デフォルト: `true`） |
| `start_time` | 数値 | 任意 | 通行止めを開始するシミュレーション経過時間（秒、デフォルト: `0`） |
| `end_time` | 数値 | 任意 | 通行止めを解除するシミュレーション経過時間（秒、デフォルト: 無制限） |

※ `edges` または `coordinates` のいずれかの指定が必要です。両方指定した場合は結合されます。

---

## 2. 内部動作ロジック (`sim/run_simulation.py`)

1. **初期化時**:
   * `data/road_closures.json` を読み込みます。
   * `coordinates` が指定されている項目は、`sumolib.net.readNet()` を用いて最寄りのSUMOエッジIDを動的に特定します。
2. **実行中ループ (TraCI)**:
   * シミュレーションの各ステップにおいて時間を監視します。
   * `step >= start_time` かつ `step < end_time` の間、`traci.edge.setDisallowed(edge_id, ["all"])` を適用して全車両の侵入を禁止します。
   * `step >= end_time` に達した時点で、`traci.edge.setAllowed(edge_id, [])` を実行して通常通行へ自動解除します。
   * ※ネットワークの `device.rerouting` 設定により、通行止めが発生すると車両は自動的に手前の交差点で迂回路を再検索して走行します。

---

## 3. 実行および検証手順

```bash
# 1. 通行止め設定を作成/編集
# city-aomori/data/road_closures.json を編集

# 2. シミュレーションを実行
cd city-aomori
python -u sim/run_simulation.py 2026/05/08 8 --nogui

# 3. 実行ログで閉鎖・解除ログを確認
# ログ出力例:
# Step 300s: [CLOSED] Edge '958818105#6' (テスト通行止め)
# ...
# Step 2700s: [REOPENED] Edge '958818105#6' (テスト通行止め)

# 4. 迂回や渋滞への影響を可視化・計測
python scripts/plot_results.py
```
