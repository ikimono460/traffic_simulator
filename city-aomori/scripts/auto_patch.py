import os
import math
import xml.etree.ElementTree as ET
import sys

if "SUMO_HOME" not in os.environ:
    os.environ["SUMO_HOME"] = "C:\\Program Files (x86)\\Eclipse\\Sumo"
if "SUMO_HOME" in os.environ:
    sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))
import sumolib

NET_FILE = "network/aomori.net.xml"
PATCH_DIR = "data/patch"

def run():
    print("Loading network...")
    if not os.path.exists(NET_FILE):
        print(f"Error: {NET_FILE} not found.")
        return
        
    net = sumolib.net.readNet(NET_FILE)
    tree = ET.parse(NET_FILE)
    root = tree.getroot()

    nodes_root = ET.Element("nodes")
    nodes_root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    nodes_root.set("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/nodes_file.xsd")

    edges_root = ET.Element("edges")
    edges_root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    edges_root.set("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/edges_file.xsd")

    conns_root = ET.Element("connections")
    conns_root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    conns_root.set("xsi:noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/connections_file.xsd")

    tls_junctions = [j.get("id") for j in root.findall("junction") if j.get("type") == "traffic_light" and not j.get("id").startswith("cluster")]
    print(f"Found {len(tls_junctions)} traffic light junctions.")

    edges = {}
    for e in root.findall("edge"):
        if e.get("function") == "internal": continue
        disallow = e.get("disallow")
        if disallow and "passenger" in disallow: continue
        edges[e.get("id")] = e

    connections_map = {}
    for c in root.findall("connection"):
        frm = c.get("from")
        if frm not in connections_map:
            connections_map[frm] = []
        connections_map[frm].append(c)

    patch_count = 0
    taper_len = 30.0

    for j_id in tls_junctions:
        incoming = [e for e in edges.values() if e.get("to") == j_id]
        
        for edge in incoming:
            edge_id = edge.get("id")
            lanes = edge.findall("lane")
            numLanes = len(lanes)
            if numLanes < 2:
                continue
                
            shape_str = lanes[0].get("shape")
            if not shape_str: continue
            
            points = [list(map(float, pt.split(","))) for pt in shape_str.split(" ")]
            p_start = points[0]
            p_end = points[-1]
            dx = p_end[0] - p_start[0]
            dy = p_end[1] - p_start[1]
            length = (dx**2 + dy**2)**0.5
            
            if length <= taper_len + 5:
                continue
                
            ratio = (length - taper_len) / length
            nx = p_start[0] + ratio * dx
            ny = p_start[1] + ratio * dy
            lon, lat = net.convertXY2LonLat(nx, ny)
            
            taper_node_id = f"node_{j_id}_{edge_id}_taper"
            node_elem = ET.SubElement(nodes_root, "node")
            node_elem.set("id", taper_node_id)
            node_elem.set("x", f"{lon:.6f}")
            node_elem.set("y", f"{lat:.6f}")
            node_elem.set("type", "priority")
            
            taper_edge_id = f"edge_{j_id}_{edge_id}_taper_to_junc"
            edge_elem = ET.SubElement(edges_root, "edge")
            edge_elem.set("id", taper_edge_id)
            edge_elem.set("from", taper_node_id)
            edge_elem.set("to", j_id)
            edge_elem.set("numLanes", str(numLanes))
            edge_elem.set("spreadType", "right")
            
            if edge_id in connections_map:
                for c in connections_map[edge_id]:
                    to_edge = c.get("to")
                    dir_ = c.get("dir")
                    
                    d_elem = ET.SubElement(conns_root, "delete")
                    d_elem.set("from", edge_id)
                    d_elem.set("to", to_edge)
                    
                    valid = True
                    fromLane = int(c.get("fromLane"))
                    toLane = int(c.get("toLane"))
                    
                    if dir_ == "l" and fromLane != 0:
                        valid = False
                    elif dir_ == "r" and fromLane != numLanes - 1:
                        valid = False
                    elif dir_ == "s" and (fromLane == numLanes - 1 and numLanes > 2): 
                        valid = False
                        
                    if valid:
                        c_elem = ET.SubElement(conns_root, "connection")
                        c_elem.set("from", taper_edge_id)
                        c_elem.set("to", to_edge)
                        c_elem.set("fromLane", str(fromLane))
                        c_elem.set("toLane", str(toLane))
                        
            patch_count += 1

    print(f"Generated patches for {patch_count} incoming edges.")
    os.makedirs(PATCH_DIR, exist_ok=True)
    ET.ElementTree(nodes_root).write(os.path.join(PATCH_DIR, "nodes.nod.xml"), encoding="utf-8", xml_declaration=True)
    ET.ElementTree(edges_root).write(os.path.join(PATCH_DIR, "edges.edg.xml"), encoding="utf-8", xml_declaration=True)
    ET.ElementTree(conns_root).write(os.path.join(PATCH_DIR, "connections.con.xml"), encoding="utf-8", xml_declaration=True)
    print("Saved patches.")

if __name__ == "__main__":
    run()
