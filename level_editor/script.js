let data = {level_x: {
    walls:[],
    grounds: []
}};

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const width = canvas.width;
const height = canvas.height;

function draw() {
    draw_background();
    for (let k in data.level_x) {
        if (k=="player_pos") {
            if (data.level_x[k][0] && data.level_x[k][1]) {
                ctx.fillStyle = "blue";
                ctx.beginPath();
                ctx.arc(data.level_x[k][0], data.level_x[k][1], 10, 0, 2 * Math.PI);
                ctx.fill();
            }
        }
        else if (k=="hole_pos") {
            if (data.level_x[k][0] && data.level_x[k][1]) {
                ctx.fillStyle = "red";
                ctx.beginPath();
                ctx.arc(data.level_x[k][0], data.level_x[k][1], 10, 0, 2 * Math.PI);
                ctx.fill();
            }
        }
        else if (k=="walls") {
            for (let i = 0; i < data.level_x[k].length; i++) {
                ctx.strokeStyle = `rgb(${data.level_x[k][i].color[0]}, ${data.level_x[k][i].color[1]}, ${data.level_x[k][i].color[2]})`;
                ctx.beginPath();
                ctx.moveTo(data.level_x[k][i].start_pos[0], data.level_x[k][i].start_pos[1]);
                ctx.lineTo(data.level_x[k][i].end_pos[0], data.level_x[k][i].end_pos[1]);
                ctx.lineWidth = data.level_x[k][i].width;
                ctx.stroke();
            }
        }
        else if (k== "grounds") {
            for (let i = 0; i < data.level_x[k].length; i++) {
                ctx.fillStyle = data.level_x[k][i].type == "sand" ? "yellow" : "cyan";
                ctx.fillRect(data.level_x[k][i].rect[0], data.level_x[k][i].rect[1], data.level_x[k][i].rect[2], data.level_x[k][i].rect[3]);
            }
        }
    }
    draw_scale();
}

function draw_background() {
    ctx.fillStyle = 'rgb(131, 177, 73)';
    ctx.fillRect(0, 0, width, height);
    const CELL_SIZE = 50;
    for (let i = 0; i < width / CELL_SIZE; i++) {
        for (let j = 0; j < height / CELL_SIZE; j++) {
            if ((i + j) % 2 == 0) {
                ctx.fillStyle = 'rgb(161, 197, 75)';
                ctx.fillRect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE);
            }
        }
    }
}

function draw_scale() {
    const CELL_SIZE = 50;
    ctx.font = "12px Arial";
    ctx.fillStyle = "black";
    for (let i = 1; i < height / CELL_SIZE; i++) {
        ctx.fillText(i*CELL_SIZE, 6, i*CELL_SIZE+4);
    }
    for (let i = 1; i< width / CELL_SIZE; i++) {
        ctx.fillText(i*CELL_SIZE, i*CELL_SIZE-9, 10);
    }
};

function show_data() {
    const element_container = document.getElementsByClassName('element-container')[0];
    element_container.innerHTML = "";

    if (data.level_x.player_pos) {
        element_container.appendChild(create_wrapper("spawn"));
    }
    if (data.level_x.hole_pos) {
        element_container.appendChild(create_wrapper("hole", true));
    }
    if (data.level_x.walls.length > 0) {
        data.level_x.walls.forEach((wall, index) => {
            element_container.appendChild(create_wrapper("walls", index));
        });
    }
    if (data.level_x.grounds.length > 0) {
        data.level_x.grounds.forEach((ground, index) => {
            element_container.appendChild(create_wrapper("grounds", index));
        })
    }
}

function createNumberInput(labelText, value, onChange, max_value =1000) {
    const wrapper = document.createElement("div");

    const label = document.createElement("label");
    label.innerText = labelText;
    wrapper.appendChild(label);

    const input = document.createElement("input");
    input.type = "number";
    input.value = value;
    input.step = 10;
    input.min = 0;
    input.max = max_value;
    input.addEventListener("input", (e) => onChange(Number(e.target.value)));
    wrapper.appendChild(input);

    return wrapper;
}

function create_wrapper(type, index=null) {
    const wrapper = document.createElement('div');
    wrapper.classList.add('element');

    const element_name = document.createElement('label');
    wrapper.appendChild(element_name);
    let name;
    
    if (type == "spawn") {
        name = "player_pos";
        const x = createNumberInput("pos x:", data.level_x.player_pos[0], (val) => {data.level_x.player_pos[0] = val; draw();}, width);
        const y = createNumberInput("pos y:", data.level_x.player_pos[1], (val) => {data.level_x.player_pos[1] = val; draw();}, height);
        wrapper.appendChild(x);
        wrapper.appendChild(y);
        wrapper.dataset.tags = "spawn";
    }
    else if (type == "hole")  {
        name = "hole_pos";
        const x = createNumberInput("pos x:", data.level_x.hole_pos[0], (val) => {data.level_x.hole_pos[0] = val; draw();}, width);
        const y = createNumberInput("pos y:", data.level_x.hole_pos[1], (val) => {data.level_x.hole_pos[1] = val; draw();}, height);
        wrapper.appendChild(x);
        wrapper.appendChild(y);
        wrapper.dataset.tags = "hole";
    }
    else if (type == "walls") {
        name = `wall ${index}`;
        const start_x = createNumberInput("start x:", data.level_x.walls[index].start_pos[0], (val) => {
            data.level_x.walls[index].start_pos[0] = val;
            draw();
        }, 600);
        const start_y = createNumberInput("start y:", data.level_x.walls[index].start_pos[1], (val) => {
            data.level_x.walls[index].start_pos[1] = val;
            draw();
        }, 1000);
        const end_x = createNumberInput("end x:", data.level_x.walls[index].end_pos[0], (val) => {
            data.level_x.walls[index].end_pos[0] = val;
            draw();
        }, 600);
        const end_y = createNumberInput("end y:", data.level_x.walls[index].end_pos[1], (val) => {
            data.level_x.walls[index].end_pos[1] = val;
            draw();
        }, 1000);
        const width = createNumberInput("width:", data.level_x.walls[index].width, (val) => {
            data.level_x.walls[index].width = val;
            draw();
        }, 400);
        wrapper.appendChild(start_x);
        wrapper.appendChild(start_y);
        wrapper.appendChild(end_x);
        wrapper.appendChild(end_y);
        wrapper.appendChild(width);
        wrapper.dataset.tags = "wall";
    }
    else if (type == "grounds") {
        name = `${data.level_x.grounds[index].type} ${index}`;
        const x = createNumberInput("pos x:", data.level_x.grounds[index].rect[0], (val) => {
            data.level_x.grounds[index].rect[0] = val;
            draw();
        }, 600);
        const y = createNumberInput("pos y:", data.level_x.grounds[index].rect[1], (val) => {
            data.level_x.grounds[index].rect[1] = val;
            draw();
        }, 1000);
        const width = createNumberInput("width:", data.level_x.grounds[index].rect[2], (val) => {
            data.level_x.grounds[index].rect[2] = val;
            draw();
        }, 600);
        const height = createNumberInput("height:", data.level_x.grounds[index].rect[3], (val) => {
            data.level_x.grounds[index].rect[3] = val;
            draw();
        }, 1000);
        wrapper.appendChild(x);
        wrapper.appendChild(y);
        wrapper.appendChild(width);
        wrapper.appendChild(height);
        wrapper.dataset.tags = "ground";
    }

    element_name.innerText = name;
    

    const del_button = document.createElement('button');
    del_button.innerText = "Del";
    del_button.onclick = () => remove_element(name, index);
    del_button.onclick = remove_element;
    del_button.classList.add('del_button');
    wrapper.appendChild(del_button);

    return wrapper;
}
function add_spawn() {
    data.level_x.player_pos = [300, 750];
    show_data();
    draw();
}
function add_hole() {
    data.level_x.hole_pos = [300, 250];
    show_data();
    draw();
}
function add_wall() {
    data.level_x.walls.push({start_pos: [100, 500], end_pos: [500, 500], width: 19, color: [20, 20 ,20]});
    show_data();
    draw();
}
function add_sand() {
    data.level_x.grounds.push({rect: [275, 475, 50, 50], type: "sand"});
    show_data();
    draw();
}

function remove_element(){
    const parent = this.parentElement;
    const tags = parent.dataset.tags;
    if (tags == "spawn") {
        delete data.level_x.player_pos;
    }
    else if (tags == "hole") {
        delete data.level_x.hole_pos;
    }
    else if (tags == "wall") {
        index = parent.firstChild.innerText.split(" ")[1];
        data.level_x.walls.splice(index, 1); 
    }
    else if (tags == "ground") {
        index = parent.firstChild.innerText.split(" ")[1];
        data.level_x.grounds.splice(index, 1);
    }
    parent.remove();
    show_data();
    draw();
}

function export_level() {
    const textToCopy = JSON.stringify(data, null, 2); // Convertir l'objet en JSON formaté
    navigator.clipboard.writeText(textToCopy)
        .then(() => {
            alert("Les données ont été copiées !");
        })
        .catch(err => {
            console.error("Erreur lors de la copie : ", err);
        });
}
draw();