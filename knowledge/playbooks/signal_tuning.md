---
type: Playbook
title: 信号制御・レーン接続調整プレイブック (signal_tuning.md)
description: 自動生成されたSUMO道路網における信号機の有無、レーン接続の競合、およびマッピングの不一致を手動修正するプレイブック。
tags: [playbook, tuning, sumo, network]
timestamp: 2026-06-25T15:55:00+09:00
---

# 信号制御・レーン接続調整プレイブック (signal_tuning.md)

OSMデータから自動インポートされた道路網は、実世界と車線数や右左折車線の設定、信号制御の有無などが一致しないことがあります。本手順書（プレイブック）は、これらを手動パッチファイルを用いて安全かつ再現可能に修正・適合させるための手順を解説します。

---

## 修正が必要になる代表的な事象

1. **車線数や右左折専用レーンの不一致**:
   OSM上では単一エッジだが、実際は交差点手前で「右折専用レーン」や「左折専用レーン」に分岐しているため、直進車と右折車が同じレーンに詰まってシミュレーション上のみで異常な大渋滞（デッドロック）が発生する場合。
2. **自動信号マッチングのずれ**:
   実世界の観測点交差点の近くに複数のSUMOジャンクション（ノード）があり、本来とは異なるノードに信号タイミングが適用されてしまう場合。
3. **無信号であるべき交差点に信号が設置されている場合**:
   OSMのタグ情報により信号制御（`traffic_light`）が誤って設定され、不要な赤信号待ちが発生している場合。

---

## 修正手順

### 手順 A. 交差点の制御タイプ変更 (信号の追加・削除)
無信号化、または信号機を新規追加したい場合は `city-akita/data/patch/nodes.nod.xml` を編集します。

* **例: 信号機の削除 (無信号・一時停止化)**
  ノードのタイプを `priority`（優先道路）または `right_before_left`（右方優先）に変更します。
  ```xml
  <nodes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd">
      <node id="1386371624" type="priority"/>
  </nodes>
  ```
* **例: 信号機の追加**
  ノードのタイプを `traffic_light` に変更します。
  ```xml
  <node id="1386371624" type="traffic_light"/>
  ```

---

### 手順 B. レーン接続（右左折レーン）の明示的修正
「右折車がどのレーンに入るか」「どのレーンから右左折を許可するか」は `city-akita/data/patch/connections.con.xml` にて修正します。

* **記述フォーマット**
  ```xml
  <connections xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/connections_file.xsd">
      <!-- 例: エッジ "edge_in" の右端レーン(index 0)から、エッジ "edge_out" のレーン 0 への接続を追加 -->
      <connection from="edge_in" to="edge_out" fromLane="0" toLane="0"/>
      
      <!-- 例: 不要な自動接続を削除したい場合 (例: 直進レーンからの強制右折などを防ぐ) -->
      <delete from="edge_in" to="edge_out_right" fromLane="1"/>
  </connections>
  ```
※車線数が不足している場合は、必要に応じて `data/patch/edges.edg.xml` で該当するエッジの `numLanes`（車線数）を明示的に増やすパッチをあてることも可能です。

---

### 手順 C. 交差点マッピングテーブル (`match_table.json`) の手動補正
最近傍探索（70m以内）での自動マッチングがずれたり、車流の流入/流出エッジの割り当てが実世界と異なっている場合は、[交差点マッピングテーブル](../data/intersections.md)（`data/match_table.json`）を直接手動で修正します。

1. `data/match_table.json` をエディタで開きます。
2. 修正対象の交差点番号（例: `"29"`）のブロックを探します。
3. `sumo_junction_id` が正しいノードIDになっているか確認・修正します（SUMO-GUI上で該当ノードをクリックしてIDを確認できます）。
4. `incoming_links` および `outgoing_links` のキー（県警リンクID）に対応する値（SUMOエッジID）を正しいものに上書きします。

---

## 修正後のビルド・検証ワークフロー

パッチファイルやマッピングテーブルを編集した後は、以下のコマンドを順番に実行して道路網を再ビルドし、正しく適用されたかを検証してください。

```bash
# 1. 道路網の再ビルド (パッチファイルが読み込まれます)
python network/build_network.py

# 2. 交差点マッピングテーブルの再マッチング (必要に応じて)
# ※手動で json を書き換えた場合は、このコマンドを実行すると json が初期化上書きされてしまうため、
# 手動修正した json のバックアップを取るか、スクリプトを実行せずに直接書き換えてください。
python scripts/match_network.py

# 3. 交通需要の再生成 (エッジIDが変わった場合に経路探索を再計算するため)
python scripts/process_traffic.py 2026/04/08 8

# 4. SUMO-GUIによる目視確認
python sim/run_simulation.py 2026/04/08 8
```

SUMO-GUI起動後、該当の交差点付近を拡大表示し、車の流れが詰まらず、右左折レーンが意図通り接続されていること、またコマンドライン出力で信号タイミングが正しく更新適用されていることを確認してください。
