let data = {
    level_x: {

        hole_pos:   [300, 200],
        walls: [
            {start_pos: [100, 950], end_pos: [500, 950], width: 19, color: [170, 170 ,245]},
            {start_pos: [109, 940], end_pos: [109, 70], width: 19, color: [200, 200 ,200]},
            {start_pos: [100, 60], end_pos: [500, 60], width: 19, color: [200, 200 ,200]},
            {start_pos: [491, 70], end_pos: [491, 940], width: 19, color: [200, 200  ,200]}
        ]}};

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const width = canvas.width;
const height = canvas.height;

function draw() {
    for (let k in data.level_x) {
        if (k=="player_pos") {
            ctx.fillStyle = "blue";
            ctx.fillRect(data.level_x[k][0], data.level_x[k][1], 10, 10);
        }
        else if (k=="hole_pos") {
            ctx.fillStyle = "red";
            ctx.fillRect(data.level_x[k][0], data.level_x[k][1], 10, 10);
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
    }
}

function show_data() {
    const element_container = document.getElementsByClassName('element-container')[0];
    for (let k in data.level_x) {
        let wrapper;
        if (k == "player_pos") {
            wrapper = create_wrapper("spawn", true, false, false, false, false);
            element_container.appendChild(wrapper);
        }
        else if (k = "hole_pos") {
            wrapper = create_wrapper("hole", true, false, false, false, false);
            element_container.appendChild(wrapper);
        }
        else if (k = "walls") {
            for (let i = 0; i < data.level_x[k].length; i++) {
                wrapper = create_wrapper("wall", false, true, true, true, true);
                element_container.appendChild(wrapper);
            }
        }
        
    }
}

function create_wrapper(name, pos, start, end, width, color) {
    const wrapper = document.createElement('div');
    wrapper.classList.add('element');

    const element_name = document.createElement('label');
    element_name.innerText = name;
    wrapper.appendChild(element_name);

    if (pos == true) {
        const label_x = document.createElement('label');
        label_x.innerText = "x: ";
        wrapper.appendChild(label_x);
        const label_y = document.createElement('label');
        label_y.innerText = "y: ";
        wrapper.appendChild(label_y);

        const input_x = document.createElement('input')
        input_x.type = "text";
        input_x.value = 300;
        wrapper.appendChild(input_x);
        const input_y = document.createElement('input')
        input_y.type = "text";
        input_y.value = 500;
        wrapper.appendChild(input_y);
    }
    else if (start == true) {
                
        }

    const del_button = document.createElement('button');
    del_button.innerText = "Del";
    del_button.onclick = remove_element;
    del_button.classList.add('del_button');
    wrapper.appendChild(del_button);

    return wrapper;
}

function add_spawn() {
    data.level_x.player_pos = [300, 600];
    show_data();
    draw();
}
function add_hole() {

}
function add_wall() {

}
function add_sand() {

}
function remove_element(){

}
function export_level(){

}