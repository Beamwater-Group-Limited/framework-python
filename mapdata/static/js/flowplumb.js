const instance = jsPlumb.getInstance({ Container: 'canvas' });
  let selectedNode = null; // 当前选中的节点
  const connections = []; // 存储节点的连接信息

  function addNode() {
    const canvas = document.getElementById('canvas');
    const node = document.createElement('div');
    node.className = 'node';
    node.textContent = '节点';
    node.style.left = `${Math.random() * 300}px`;
    node.style.top = `${Math.random() * 200}px`;
    node.dataset.name = '节点'; // 默认名称
    node.dataset.attribute = 'option1'; // 默认属性值

    // 当节点被点击时，加载数据到编辑面板
    node.addEventListener('click', () => selectNode(node));

    canvas.appendChild(node);

    // 添加拖动功能
    instance.draggable(node, { containment: 'parent' });

    // 为节点添加连接端点
    instance.addEndpoint(node, {
      anchor: "Continuous", // 端点可以连接的所有方向
      isSource: true,       // 可以作为连接的起点
      isTarget: true,       // 可以作为连接的终点
      connector: "Straight", // 连接线的样式（直线）
      endpoint: "Dot",      // 端点的样式
      paintStyle: { fill: "blue", radius: 5 } // 端点样式
    });
  }

  function selectNode(node) {
    selectedNode = node;

    // 启用编辑控件
    document.getElementById('nodeName').disabled = false;
    document.getElementById('nodeAttribute').disabled = false;
    document.getElementById('saveButton').disabled = false;

    // 加载节点数据到编辑控件
    document.getElementById('nodeName').value = node.dataset.name;
    document.getElementById('nodeAttribute').value = node.dataset.attribute;
  }

  function saveNode() {
    if (selectedNode) {
      // 获取编辑控件中的值
      const name = document.getElementById('nodeName').value;
      const attribute = document.getElementById('nodeAttribute').value;

      // 更新节点的数据属性
      selectedNode.dataset.name = name;
      selectedNode.dataset.attribute = attribute;

      // 更新节点显示的内容
      selectedNode.textContent = name;
    }
  }

  // 新增连接时触发
  instance.bind("connection", function(info) {
    const sourceId = info.source.id || info.source.dataset.name;
    const targetId = info.target.id || info.target.dataset.name;

    // 保存连接信息
    connections.push({
      source: sourceId,
      target: targetId
    });

    console.log("创建了连接：", { source: sourceId, target: targetId });
  });

  // 删除连接时触发
  instance.bind("connectionDetached", function(info) {
    const sourceId = info.source.id || info.source.dataset.name;
    const targetId = info.target.id || info.target.dataset.name;

    const index = connections.findIndex(conn => conn.source === sourceId && conn.target === targetId);
    if (index !== -1) {
      connections.splice(index, 1);
    }

    console.log("删除了连接：", { source: sourceId, target: targetId });
  });

  function exportData() {
    const nodes = document.querySelectorAll('.node');
    const data = Array.from(nodes).map(node => {
      const rect = node.getBoundingClientRect(); // 获取位置 (相对于画布)
      const canvasRect = document.getElementById('canvas').getBoundingClientRect();

      return {
        id: node.id || null,
        name: node.dataset.name, // 节点名称
        attribute: node.dataset.attribute, // 节点属性
        position: {
          left: rect.left - canvasRect.left,
          top: rect.top - canvasRect.top
        }
      };
    });

    const exportData = {
      nodes: data,
      connections: connections
    };

    console.log(JSON.stringify(exportData, null, 2)); // 导出 JSON 到控制台
    alert('JSON 已导出，请查看控制台！');
  }