import cytoscape from 'cytoscape';
import automove from 'cytoscape-automove';
import edgehandles from 'cytoscape-edgehandles';

cytoscape.use(automove);
cytoscape.use(edgehandles);

// 'fa' is the main structure of our finite automata
// its in the form:
// [
// { group: 'nodes', data: { id: 'n0' }, position: { x: 100, y: 100 } },
// { group: 'nodes', data: { id: 'n1' }, position: { x: 200, y: 200 } },
// { group: 'edges', data: { id: 'e0', source: 'n0', target: 'n1' } },
// { group: 'edges', data: { id: 'e1', source: 'n0', target: 'n0' } }
// ]
let fa = []
var q_counter = 0;
var q_numbers_left = [];

var cy = cytoscape({
    container: document.getElementById('cy'), // container to render in
    elements: [

    ],
    style: [ // the stylesheet for the graph
        {
            selector: 'node',
            style: {
                'background-color': '#FFF',
                'border-color': '#000',
                'border-width': 1,
                'label': 'data(id)',
                'text-valign': 'center',
                'text-halign': 'center',
                'width': '2.5em',
                'height': '2.5em',
            }
        },
        {
            selector: 'edge',
            style: {
                'label': 'data(label)',
                // 'text-margin-x': '12px',
                // 'text-margin-y': '-12px',
                'text-background-color': '#F8F9FA',
                'text-background-opacity': 1,
                'text-background-padding': '3px',
                'text-rotation': 'autorotate',
                'text-events': 'yes',
                'color': '#000000',
                'width': 2,
                'line-color': '#666',
                'target-arrow-color': '#666',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
            }
        },
        {
            selector: '.eh-preview, .eh-ghost-edge',
            style: {
                'background-color': '#17A2B8',
                'line-color': '#17A2B8',
                'target-arrow-color': '#17A2B8',
                'source-arrow-color': '#17A2B8'
            }
        },

        {
            selector: '.eh-ghost-edge.eh-preview-active',
            style: {
                'opacity': 0
            }
        }

    ],
    layout: {
        name: 'grid',
        rows: 1
    },

    wheelSensitivity: 0.3,

});

// =========================================================== CREATE EDGES BETWEEN NODES IN FINITE AUTOMATA ==========================================================

var eh = cy.edgehandles({
    canConnect: function (sourceNode, targetNode) {
        return true
    },
    hoverDelay: 150, // time spent hovering over a target node before it is considered selected
    snap: true, // when enabled, the edge can be drawn by just moving close to a target node (can be confusing on compound graphs)
    snapThreshold: 20, // the target node must be less than or equal to this many pixels away from the cursor/finger
    snapFrequency: 10, // the number of times per second (Hz) that snap checks done (lower is less expensive)
    //noEdgeEventsInDraw: true, // set events:no to edges during draws, prevents mouseouts on compounds
    disableBrowserGestures: true // during an edge drawing gesture, disable browser gestures such as two-finger trackpad swipe and pinch-to-zoom
});

//ADD DOUBLE TAP EVENT ON EDGE
function double_tap_on_edge_handler(evt) {
    let new_label = window.prompt("Digite um não terminal: ", evt.target.data('label'));

    if (new_label !== '') {
        evt.target.data('label', new_label);
    } else {
        evt.target.data('label', 'λ');

    }

}
document.getElementById('button-cursor').addEventListener('click', function () {
    eh.disableDrawMode();
    cy.removeListener('tap');
    cy.on('dbltap', 'edge', double_tap_on_edge_handler);
    this.classList.add('button-selected');
    remove_selected_from_buttons(this.id);
});

document.getElementById('button-edge').addEventListener('click', function () {
    eh.enableDrawMode();
    cy.removeListener('tap');
    cy.removeListener('dbltap');
    this.classList.add('button-selected');
    remove_selected_from_buttons(this.id);
});

// =========================================================== ADD AND REMOVE NODES FROM FINITE AUTOMATA ==========================================================
// .automove-viewport nodes kept in viewport (even if added after this call)
// convenient but less performant than `nodesMatching: collection`
cy.automove({
    nodesMatching: '.automove-viewport',
    reposition: 'viewport'
});


// Funcao que vai como handler do evento 'tap' do CY
function btn_add_cy_handler(evt) {
    var tgt = evt.target;
    var q_number;
    if (q_numbers_left.length === 0) {
        q_number = q_counter;
        q_counter += 1;
    } else {
        q_number = q_numbers_left[0];
        q_numbers_left.splice(0, 1);
    }
    cy.add({
        classes: 'automove-viewport',
        data: { id: 'q' + q_number },
        position: {
            x: evt.position.x,
            y: evt.position.y
        }
    });
}

// Função que vai como handler do botao de add
function button_add_handler() {
    eh.disableDrawMode();
    cy.removeListener('tap', btn_remove_cy_handler);

    cy.on('tap', btn_add_cy_handler);
    this.classList.add('button-selected');
    remove_selected_from_buttons(this.id);
};

// Funcao que vai como handler do evento 'tap' do CY
function btn_remove_cy_handler(evt) {
    var item = evt.target;
    if (evt.target.group() === 'nodes') {
        q_numbers_left.push(parseInt(evt.target.id().slice(1,)));
        q_numbers_left.sort();
    }
    cy.remove(item);
}

// Função que vai como handler do botao de remove
function button_remove_handler() {
    eh.disableDrawMode();
    cy.removeListener('tap', btn_add_cy_handler);

    cy.on('tap', 'node', btn_remove_cy_handler);
    cy.on('tap', 'edge', btn_remove_cy_handler);

    this.classList.add('button-selected');
    remove_selected_from_buttons(this.id);
}
document.getElementById('button-add').addEventListener('click', button_add_handler);
document.getElementById('button-remove').addEventListener('click', button_remove_handler);



function remove_selected_from_buttons(except) {
    let button_list = document.getElementById("buttons-div").children

    for (let button of button_list) {
        if (button.id.toLocaleLowerCase() !== except.toLocaleLowerCase()) {
            button.classList.remove('button-selected');
        }
    }
}


// 1. Adicionar e remover nós --- DONE
//    1.1 Nós são nomeados de q0...qn --- DONE
// 2. Ligar nós por setas - edges (arrasta de um nó para outro) --- DONE
//    2.1 Ligar um nó a ele mesmo. --- DONE
//    2.2 Ligações valoradas (podendo ser vazio) --- DONE
// TODO
// 3. Marcar nós como inicial ou final.
// 4. Mover nós --- DONE
//