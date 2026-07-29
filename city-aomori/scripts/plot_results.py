import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 日本語フォントの設定 (Windows環境を想定)
# フォントが設定できない場合はデフォルトフォントを使用
font_path = 'C:/Windows/Fonts/meiryo.ttc'
if os.path.exists(font_path):
    plt.rcParams['font.family'] = 'Meiryo'

def parse_summary(filepath):
    times = []
    mean_speeds = []
    running = []
    halting = []
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return [], [], [], []
        
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    for step in root.findall('step'):
        time_val = float(step.get('time'))
        # ネットワークの平均速度をkm/hに変換
        speed_ms = float(step.get('meanSpeed'))
        speed_kmh = speed_ms * 3.6
        
        running_veh = int(step.get('running'))
        halting_veh = int(step.get('halting'))
        
        times.append(time_val)
        mean_speeds.append(speed_kmh)
        running.append(running_veh)
        halting.append(halting_veh)
        
    return times, mean_speeds, running, halting

def parse_tripinfo(filepath, probe_id="probe_car_1"):
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return None
        
    tree = ET.parse(filepath)
    root = tree.getroot()
    
    for tripinfo in root.findall('tripinfo'):
        if tripinfo.get('id') == probe_id:
            duration = float(tripinfo.get('duration'))
            timeLoss = float(tripinfo.get('timeLoss'))
            depart = float(tripinfo.get('depart'))
            arrival = float(tripinfo.get('arrival'))
            
            return {
                "duration": duration,
                "timeLoss": timeLoss,
                "depart": depart,
                "arrival": arrival
            }
            
    return None

def plot_graphs():
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    summary_xml = os.path.join(output_dir, "summary.xml")
    tripinfo_xml = os.path.join(output_dir, "tripinfo.xml")
    
    # 1. データの読み込み
    times, mean_speeds, running, halting = parse_summary(summary_xml)
    probe_data = parse_tripinfo(tripinfo_xml, "probe_car_1")
    
    # --- プローブカーの出力 ---
    print("=" * 40)
    print(" プローブカー (計測車両) の結果")
    print("=" * 40)
    if probe_data:
        duration_min = probe_data['duration'] / 60
        time_loss_min = probe_data['timeLoss'] / 60
        print(f"所要時間: {duration_min:.2f} 分 ({probe_data['duration']}秒)")
        print(f"渋滞による損失時間: {time_loss_min:.2f} 分 ({probe_data['timeLoss']}秒)")
    else:
        print("プローブカーが目的地に到達していないか、シミュレーションが途中です。")
    print("=" * 40)
    
    if not times:
        return
        
    # --- グラフA: 平均速度の推移 ---
    plt.figure(figsize=(10, 5))
    plt.plot(times, mean_speeds, color='green', linewidth=2)
    plt.title("ネットワーク全体の平均速度の推移")
    plt.xlabel("シミュレーション時間 (秒)")
    plt.ylabel("平均速度 (km/h)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    graph_a_path = os.path.join(output_dir, "graph_a_avg_speed.png")
    plt.savefig(graph_a_path, dpi=150)
    print(f"グラフを保存しました: {graph_a_path}")
    
    # --- グラフB: 走行車両数と停止車両数の推移 ---
    plt.figure(figsize=(10, 5))
    plt.stackplot(times, [running, halting], labels=['走行車両', '停止・渋滞車両'], colors=['#3498db', '#e74c3c'], alpha=0.8)
    plt.title("走行車両数と停止車両数の推移")
    plt.xlabel("シミュレーション時間 (秒)")
    plt.ylabel("車両数 (台)")
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    graph_b_path = os.path.join(output_dir, "graph_b_vehicle_counts.png")
    plt.savefig(graph_b_path, dpi=150)
    print(f"グラフを保存しました: {graph_b_path}")

if __name__ == "__main__":
    plot_graphs()
