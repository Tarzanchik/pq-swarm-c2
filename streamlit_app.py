import streamlit as st
import networkx as nx
import time

st.set_page_config(page_title="PQ-Swarm C2 Monitor", layout="wide")

# Храним граф
G = nx.Graph()
nodes = [f"n{i}" for i in range(10)]
for node in nodes:
    G.add_node(node)

# Полносвязные связи
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        G.add_edge(nodes[i], nodes[j])

# Имитируем поступающие сообщения
st.title("🔵 PQ-Swarm C2 Visualization")
st.subheader("Topology View")

pos = nx.spring_layout(G, seed=42)
st.graphviz_chart(
    "\n".join([f"{src} -- {dst}" for src, dst in G.edges()])
)

st.subheader("📡 Message Log")

import json

st.subheader("🕹️ Send Command")

# Выбор цели
target = st.selectbox("Select target node", nodes)
command = st.text_input("Enter command text", value="COMMAND: HOLD POSITION")

if st.button("📤 Send to Node"):
    with open("swarm_api.json", "w") as f:
        json.dump({"target": target, "last_command": command}, f)
    st.success(f"Sent: {command} → {target}")


# Session state для накопления логов
if "logs" not in st.session_state:
    st.session_state.logs = []

# Имитируем новые сообщения
if st.button("📤 Broadcast Command"):
    sender = "n0"
    for target in nodes[1:]:
        msg = f"{sender} → {target}: COMMAND: SWEEP"
        st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")

# Отображаем логи
for log in reversed(st.session_state.logs[-20:]):
    st.write(log)

st.subheader("✅ Feedback from Nodes")

try:
    with open("logs/swarm_feedback.log", "r", encoding="utf-8") as f:
        feedback_lines = f.readlines()
    for line in reversed(feedback_lines[-20:]):
        st.success(line.strip())
except FileNotFoundError:
    st.info("No feedback yet.")
