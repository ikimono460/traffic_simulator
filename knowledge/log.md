---
type: UpdateHistory
title: 更新履歴 (log.md)
description: ナレッジベースの変更および更新の歴史。
timestamp: 2026-07-29T20:34:00+09:00
---

# 更新履歴 (log.md)

本ファイルは、秋田市・青森市交通シミュレーションプロジェクトのナレッジベース（OKF Bundle）に対する変更履歴を時系列に記録するログファイルです。

## [2026-07-29] 青森市シミュレーション評価基盤・計測車両およびピンポイント通行止め機能の導入

*   **更新者**: Antigravity (AIエージェント)
*   **概要**: 青森市交通シミュレーションにおける客観的評価指標（平均速度・車両数推移グラフ）、計測用プローブカー、および任意時間帯での動的通行止め制御機能の追加。
*   **修正・追加ファイル**:
    *   `knowledge/playbooks/road_closure.md`: 特定道路の動的通行止め・時間解除設定（`data/road_closures.json`）の指定・運用手順プレイブック（新規追加）。
    *   `knowledge/playbooks/index.md`: プレイブックインデックスへの `road_closure.md` の追加。
    *   `knowledge/simulation/evaluation.md`: 評価指標、プローブカー定義、解析スクリプト、再現手順のドキュメント（新規追加）。
    *   `knowledge/simulation/index.md`: シミュレーションインデックスへの `evaluation.md` の追加。
    *   `city-aomori/data/road_closures.json`: 道路ID直接指定および座標指定に対応した通行止め設定ファイル（新規追加）。
    *   `city-aomori/sim/run_simulation.py`: TraCI経由で指定エッジの侵入禁止・解除を動的に行うロジックの追加。
    *   `city-aomori/demand/probe_vehicle.rou.xml`: 青森市立甲田小学校前〜青森県庁前間の計測用プローブカー設定。
    *   `city-aomori/sim/aomori.sumocfg`: XMLログ出力設定（`summary.xml`, `tripinfo.xml`）および動的リルーティング設定。
    *   `city-aomori/scripts/plot_results.py`: ログパースおよびグラフ自動出力スクリプト。

## [2026-07-16] 交差点パッチWebエディタのUI向上と幾何計算の高度化

*   **更新者**: Antigravity (AIエージェント)
*   **概要**: 交差点パッチWebエディタでの左側通行アライメント対応、極小エッジ（20cm）対応、直進/右左折矢印の干渉を回避する高度な幾何座標制御を実装し、操作マニュアルとスクリーンショットを追加。
*   **修正・追加ファイル**:
    *   [index.html](file:///c:/Users/Genno_Shirou/Documents/works/traffic_simulator/city-akita/web_editor/templates/index.html)
    *   [editor_instructions.md](file:///c:/Users/Genno_Shirou/Documents/works/traffic_simulator/knowledge/playbooks/editor_instructions.md)
    *   `knowledge/resources/editor_main.png` & `editor_editing.png`

## [2026-06-25] ナレッジベースの新規開設

*   **更新者**: Antigravity (AIエージェント)
*   **概要**: OKF v0.1 仕様に準拠したナレッジベースの設計および初期構築。
*   **追加されたコンセプトドキュメント**:
    *   `knowledge/index.md`
    *   `knowledge/project_overview.md`
    *   `knowledge/data/index.md`
    *   `knowledge/network/index.md`
    *   `knowledge/demand/index.md`
    *   `knowledge/simulation/index.md`
    *   `knowledge/playbooks/index.md`
