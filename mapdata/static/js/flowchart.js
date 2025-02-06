// 初始化画布
const canvas = new fabric.Canvas('canvas');

// 添加矩形
function addRectangle() {
  const rect = new fabric.Rect({
    left: 100,
    top: 100,
    fill: 'blue',
    width: 100,
    height: 50,
    stroke: 'black',
    strokeWidth: 2,
    hasControls: true,
  });
  canvas.add(rect);
}

// 添加圆形
function addCircle() {
  const circle = new fabric.Circle({
    left: 150,
    top: 150,
    fill: 'red',
    radius: 30,
    stroke: 'black',
    strokeWidth: 2,
    hasControls: true,
  });
  canvas.add(circle);
}

// 导出 JSON
function exportJSON() {
  const json = canvas.toJSON();
  console.log(json);
  alert('JSON 导出成功，请查看控制台');
}

// 导入 JSON
function importJSON() {
  const input = document.getElementById('jsonFile');
  input.click();
  input.onchange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const json = event.target.result;
        canvas.loadFromJSON(json, () => {
          canvas.renderAll();
          alert('JSON 导入成功！');
        });
      };
      reader.readAsText(file);
    }
  };
}
function deleteSelected() {
  const activeObject = canvas.getActiveObject();
  if (activeObject) {
    canvas.remove(activeObject);
  } else {
    alert('未选中任何对象');
  }
}

let line, isDrawing = false;

// 在画布上按下时创建线
canvas.on('mouse:down', (o) => {
  if (o.target) {
    const pointer = canvas.getPointer(o.e);
    isDrawing = true;
    line = new fabric.Line([pointer.x, pointer.y, pointer.x, pointer.y], {
      stroke: 'black',
      strokeWidth: 2,
    });
    canvas.add(line);
  }
});

// 在画布上移动时更新线的终点
canvas.on('mouse:move', (o) => {
  if (!isDrawing) return;
  const pointer = canvas.getPointer(o.e);
  line.set({ x2: pointer.x, y2: pointer.y });
  canvas.renderAll();
});

// 在画布上松开鼠标停止绘制
canvas.on('mouse:up', () => {
  isDrawing = false;
});

// 使对象可拖拽
canvas.on('object:moving', (e) => {
  const obj = e.target;
  obj.setCoords();
});
