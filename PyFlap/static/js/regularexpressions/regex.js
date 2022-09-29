const regexTestForm = document.getElementById("regexForm");
const testStringInput1 = document.getElementById("test_string");
const testStringInput2 = document.getElementById("test_string2");
const regexText = document.getElementById("regex");


regexText.addEventListener('keyup', (e) => {
    e.preventDefault();

    const payload = new FormData(regexTestForm);
    fetch("/regularexpressions/", {
        method: 'POST',
        body: payload,
        headers: new Headers([['source', 'fetch_api']]),
    }).then(res => res.json()).then(data => {
        if (data.invalid_regex) {
            regexText.style.color = 'red';
            regexText.style.borderColor = 'red';
        }

        if (data.string_validation1) { // Se for valida a string 1
            testStringInput1.style.color = 'green';
            testStringInput1.style.borderColor = 'green';
        }
        else {
            testStringInput1.style.color = 'red';
            testStringInput1.style.borderColor = 'red';
        }

        // STRING 2
        if (data.string_validation2) { // Se for valida a string 2
            testStringInput2.style.color = 'green';
            testStringInput2.style.borderColor = 'green';
        }
        else {
            testStringInput2.style.color = 'red';
            testStringInput2.style.borderColor = 'red';
        }


    })
});

testStringInput1.addEventListener('keyup', (e) => {
    e.preventDefault();

    const payload = new FormData(regexTestForm);
    fetch("/regularexpressions/", {
        method: 'POST',
        body: payload,
        headers: new Headers([['source', 'fetch_api']]),
    }).then(res => res.json()).then(data => {
        if (data.string_validation1) { // Se for valida a string 1
            testStringInput1.style.color = 'green';
            testStringInput1.style.borderColor = 'green';
        }
        else {
            testStringInput1.style.color = 'red';
            testStringInput1.style.borderColor = 'red';
        }

    })
});

testStringInput2.addEventListener('keyup', (e) => {
    e.preventDefault();

    const payload = new FormData(regexTestForm);
    fetch("/regularexpressions/", {
        method: 'POST',
        body: payload,
        headers: new Headers([['source', 'fetch_api']]),
    }).then(res => res.json()).then(data => {
        // STRING 2
        if (data.string_validation2) { // Se for valida a string 2
            testStringInput2.style.color = 'green';
            testStringInput2.style.borderColor = 'green';
        }
        else {
            testStringInput2.style.color = 'red';
            testStringInput2.style.borderColor = 'red';
        }

    })
});