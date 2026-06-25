---
type: DirectoryIndex
title: シミュレーション実行インデックス
description: SUMOシミュレーションの設定・制御・実行プロセスのインデックス。
timestamp: 2026-06-25T15:55:00+09:00
---

# シミュレーション実行インデックス

本フォルダは、SUMOシミュレーションの統合設定ファイル（.sumocfg）と、Python (TraCI API) を通じてシミュレーション実行中に動的な制御（信号タイミング制御など）を行う起動スクリプトに関する知識ドキュメントを管理しています。

## 構成コンセプト

* [シミュレーション設定と起動スクリプト (sumo_sim.md)](./sumo_sim.md): akita.sumocfgの構成項目と、TraCI APIによる時間同期的な信号制御ロジックの動作解説。

## シミュレーションフォルダの物理構成
* `city-akita/sim/akita.sumocfg`: 道路網（network/）、交通需要（demand/）、シミュレーション設定を一つにまとめたSUMO構成ファイル。
* `city-akita/sim/run_simulation.py`: TraCIを経由して信号パターンをリアルタイム反映させながらシミュレーションを起動・管理するPythonスクリプト。
