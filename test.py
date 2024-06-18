import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    G = nx.DiGraph()
    # 使用 LaTeX 风格的标签
    # 添加状态节点
    states = [r'$S_0$', r'$S_1$', r'$S_2$', r'$S_3$']
    for state in states:
        G.add_node(state)

    # 添加观测节点
    observations = [r'$O_0$', r'$O_1$', r'$O_2$', r'$O_3$']
    for obs in observations:
        G.add_node(obs)

    # 添加状态转移边
    for i in range(len(states) - 1):
        G.add_edge(states[i], states[i+1])

    # 添加状态到观测的边
    for i in range(len(states)):
        G.add_edge(states[i], observations[i])
        
    G.remove_node(r'$O_0$')
   
    G.add_node(r'$\cdots$')
    G.add_edge(r'$S_3$', r'$\cdots$')
    states.append(r'$\cdots$')
    pos = nx.bipartite_layout(G, states, align='horizontal')
    # 绘制节点和边
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20)
    nodes = nx.draw_networkx_nodes(G, pos, node_color='none', edgecolors='black', node_size=1500)
    nx.draw_networkx_labels(G, pos, labels={n: n for n in G.nodes()}, font_size=12)

    # 绘制边的标签
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    # 设置图形的其他属性
    plt.axis('off')  # 关闭坐标轴
    plt.show()