// Pegando o input de Simbolo inicial da gramatica

const grammar_initial_input = document.getElementById('grammar_initial');
const grammar_left_side_input = document.getElementById('rule_left_side');
const grammar_right_side_input = document.getElementById('rule_right_side');
const add_rule_button = document.getElementById('add_rule_button');

document.addEventListener("DOMContentLoaded", function (event) {

    if (isLetter(grammar_initial_input.value)) {
        grammar_initial_input.style.borderColor = 'green';
    }
});
// FUNCAO PARA TRATAR O INPUT DO SIMBOLO INICIAL DA GRAMATICA
grammar_initial_input.addEventListener("input", function (event) {
    if (isLetter(this.value)) { // Se for uma letra
        this.value = this.value.toUpperCase(); // GARANTE QUE SEJA UPPERCASE
        text = this.value;

        // Mudar cor do input
        this.style.borderColor = 'green';
    }
    else {
        add_rule_button.disabled = true
        // Mudar cor do input
        this.style.borderColor = 'red';
    }

    if (everyOneIsLetter()) {
        add_rule_button.disabled = false
    }
});
// INPUT DO LADO ESQUERDO DA REGRA
grammar_left_side_input.addEventListener("input", function (event) {
    if (isLetter(this.value)) { // Se for uma letra
        this.value = this.value.toUpperCase(); // GARANTE QUE SEJA UPPERCASE
        text = this.value;
        this.style.borderColor = 'green';
    }
    else {
        add_rule_button.disabled = true
        this.style.borderColor = 'red';
    }

    if (everyOneIsLetter()) {
        add_rule_button.disabled = false
    }
});

// INPUT DO LADO DIREITO DA REGRA
grammar_right_side_input.addEventListener("input", function (event) {
    if (matchPattern(this.value)) { // Se for uma letra ou "|" ou " "

        this.style.borderColor = 'green';
    }
    else {
        add_rule_button.disabled = true;
        this.style.borderColor = 'red';
    }

    if (everyOneIsLetter() && matchPattern(this.value)) {
        add_rule_button.disabled = false
    }
});




function matchPattern(string) {
    if (typeof string !== 'string') {
        return false
    }
    return /^[a-zA-Z| ]+$/.test(string)
}
function isLetter(character) {
    if (typeof character !== 'string') {
        return false
    }
    return /^[a-zA-Z]$/.test(character)
}

function everyOneIsLetter() {
    if (isLetter(grammar_initial_input.value) && isLetter(grammar_left_side_input.value)) {
        return true
    }
    return false
}