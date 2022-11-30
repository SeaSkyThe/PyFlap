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

var cy = cytoscape({
    container: document.getElementById('cy'), // container to render in
    elements: [

    ],
    style: [ // the stylesheet for the graph
        {
            selector: 'node',
            style: {
                'background-color': '#666',
                'label': 'data(id)'
            }
        },
        {
            selector: 'edge',
            style: {
                'width': 3,
                'line-color': '#000000',
                'target-arrow-color': '#000000',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier'
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

document.getElementById('button-edge').addEventListener('click', function () {
    eh.enableDrawMode();
    cy.removeListener('tap');
});

document.getElementById('button-cursor').addEventListener('click', function () {
    eh.disableDrawMode();
    cy.removeListener('tap');
});


// =========================================================== ADD AND REMOVE NODES FROM FINITE AUTOMATA ==========================================================
// .automove-viewport nodes kept in viewport (even if added after this call)
// convenient but less performant than `nodesMatching: collection`
cy.automove({
    nodesMatching: '.automove-viewport',
    reposition: 'viewport'
});


function button_add_handler() {
    eh.disableDrawMode();
    cy.removeListener('tap', button_remove_handler);
    cy.on('tap', function (evt) {
        var tgt = evt.target || evt.cyTarget; // 3.x || 2.x

        if (tgt === cy) {
            cy.add({
                classes: 'automove-viewport',
                data: { id: 'q' + Math.round(Math.random() * 100) },
                position: {
                    x: evt.position.x,
                    y: evt.position.y
                }
            });
        }
    });
};

function button_remove_handler() {
    eh.disableDrawMode();
    cy.removeListener('tap', button_add_handler);
    cy.on('tap', 'node', function (evt) {
        var node = evt.target;
        cy.remove(node);
    });

    cy.on('tap', 'edge', function (evt) {
        var edge = evt.target;
        cy.remove(edge);
    });

}
document.getElementById('button-add').addEventListener('click', button_add_handler);
document.getElementById('button-remove').addEventListener('click', button_remove_handler);


// Uses the extension: cytoscape-automove
function add_node() {
    return
}



// var eles = cy.add([
//     { group: 'nodes', data: { id: 'n0' }, position: { x: 100, y: 100 } },
//     { group: 'nodes', data: { id: 'n1' }, position: { x: 200, y: 200 } },
//     { group: 'edges', data: { id: 'e0', source: 'n0', target: 'n1' } },
//     { group: 'edges', data: { id: 'e1', source: 'n0', target: 'n0' } }
// ]);


// TODO
// 1. Adicionar e remover nós
//    1.1 Nós são nomeados de q0...qn
// 2. Ligar nós por setas - edges (arrasta de um nó para outro)
//    2.1 Ligar um nó a ele mesmo.
//    2.2 Ligações valoradas (podendo ser vazio)
// 3. Marcar nós como inicial ou final.
// 4. Mover nós
//