---
type: Simulation
title: シミュレーション設定と起動スクリプト (sumo_sim.md)
description: シミュレーション構成ファイル（.sumocfg）の設定内容と、TraCI APIを用いた信号の動的適用制御スクリプト。
resource: city-akita/sim/akita.sumocfg
tags: [simulation, sumo, traci, python]
timestamp: 2026-06-25T15:55:00+09:00
---

# シミュレーション設定と起動スクリプト (sumo_sim.md)

本ドキュメントは、SUMOシミュレーションの設定定義ファイル（`akita.sumocfg`）および、リアルタイムに信号スプリット・サイクル長を適用しながらシミュレーションを起動・制御する Python スクリプトの仕様解説です。

## 基本情報

* **シミュレーション構成ファイル**: `city-akita/sim/akita.sumocfg`
* **実行用 Python スクリプト**: `city-akita/sim/run_simulation.py`
* **入力依存ファイル**: 
  * `city-akita/network/akita.net.xml` (道路網ファイル)
  * `city-akita/demand/akita.rou.xml` (交通需要フローファイル)
  * `city-akita/resources/typeC_akita_2026_04/秋田県警_制御_202604.csv` (信号機スプリット制御オープンデータ)

---

## 1. シミュレーション構成設定 (`akita.sumocfg`)

`akita.sumocfg` は、シミュレーション起動に必要な道路網、需要ファイルを指定し、以下の特殊な実行処理を設定しています。

```xml
<configuration ...>
    <input>
        <net-file value="../network/akita.net.xml"/>
        <route-files value="../demand/akita.rou.xml"/>
    </input>
    <time>
        <begin value="0"/>
        <end value="3600"/> <!-- 1時間 (3600秒) -->
    </time>
    <processing>
        <time-to-teleport value="-1"/> <!-- テレポートの抑止 -->
        <lateral-resolution value="0.3"/> <!-- サブレーンモデルの有効化 -->
    </processing>
</configuration>
```

### 処理オプションの意図:
* `<time-to-teleport value="-1"/>`: SUMOのデフォルトの振る舞いである「一定時間車列が動かないと車両をテレポート（消去）させる機能」を無効化します。これにより、交差点でのグリッドロックや渋滞の本当の発生状況を正しく測定・可視化できます。
* `<lateral-resolution value="0.3"/>`: 幅0.3メートルのサブレーンモデル（Sublane Model）を有効化します。車線幅の中での自動二輪車のすり抜けや、複数台の車が緩やかに車線内に収まる挙動など、日本の密度の高い道路状況をシミュレートします。

---

## 2. 信号の動的適用制御スクリプト (`run_simulation.py`)

`run_simulation.py` は、単にシミュレーションを実行するだけでなく、起動時に実世界の信号パターン（サイクル長およびスプリット値）を動的に各信号機ノードへ適用します。

### 信号制御の適用プロセスと計算ロジック

1. **信号制御CSVデータのロード**:
   `秋田県警_制御_202604.csv` から、指定された日時の「交差点番号」「サイクル長」、および最大6個の「スプリット値」を取得します。
2. **SUMO信号フェーズ情報の取得**:
   TraCI を介して `traci.trafficlight.getCompleteRedYellowGreenDefinition(tls_id)` を呼び出し、対象交差点の現在のフェーズ状態（RYG定義）を取得します。
3. **青信号フェーズ時間の算出**:
   * 黄色（`y`）や赤色（`r`）など、遷移フェーズに必要な固定秒数を合算します（`fixed_time`）。
   * 全体サイクル時間から固定秒数を引き、青信号として利用可能な総時間（`available_green_time`）を計算します。
   * 県警データの「スプリット値」の比率に従って、各青信号フェーズに対して比率配分した秒数を計算して割り当てます。
     \[
     \text{フェーズ秒数} = \frac{\text{スプリット値}}{\sum(\text{全スプリット})} \times \text{青信号可能総時間}
     \]
4. **プログラムロジックの設定**:
   計算された時間配分でフェーズリストを上書きし、`traci.trafficlight.setProgramLogic(tls_id, logic)` を実行して変更を適用します。

### 実行手順

シミュレーションを起動するには、再現したい日付と開始時間を指定して実行します。

* **GUI版 (SUMO-GUIが起動)**:
  ```bash
  python sim/run_simulation.py 2026/04/08 8
  ```
* **CUI非GUI版 (高速シミュレーション)**:
  ```bash
  python sim/run_simulation.py 2026/04/08 8 --nogui
  ```

※非GUI版は、コンテキスト切り替えが少なく計算負荷が低いため、大量の実験や自動チューニングを実行するAIエージェントの利用に最適です。
