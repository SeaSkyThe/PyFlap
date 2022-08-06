
// // ADDING NAVBAR ITEMS
// const navBar = document.querySelectorAll(".nav_list");
// console.log(navBar[0]);
// // homepage item
// const homePageItem = document.createElement('a');
// homePageItem.href = "/";
// homePageItem.className = "nav_link active";
// homePageItem.innerHTML = "<i class='bx bx-grid-alt nav_icon'></i> <span class='nav_name'>Presentation</span>";
// // participants page item
// const participantsPageItem = document.createElement('a');
// participantsPageItem.href = "#";
// participantsPageItem.className = "nav_link";
// participantsPageItem.innerHTML = "<i class='bx bx-user nav_icon'></i> <span class='nav_name'>Participants</span> ";
// // Regex page item
// const regexPageItem = document.createElement('a');
// regexPageItem.href = "/regularexpressions/";
// regexPageItem.className = "nav_link";
// regexPageItem.innerHTML = "<i class='bx bx-message-square-detail nav_icon'></i> <span class='nav_name'>Regex Validator</span> ";
// // Bookmark page item
// const bookmarkPageItem = document.createElement('a');
// bookmarkPageItem.href = "#";
// bookmarkPageItem.className = "nav_link";
// bookmarkPageItem.innerHTML = "<i class='bx bx-bookmark nav_icon'></i> <span class='nav_name'>Bookmark</span>";
// // Files page item
// const filesPageItem = document.createElement('a');
// filesPageItem.href = "#";
// filesPageItem.className = "nav_link";
// filesPageItem.innerHTML = "<i class='bx bx-folder nav_icon'></i> <span class='nav_name'>Files</span> ";
// // Stats page item
// const statsPageItem = document.createElement('a');
// statsPageItem.href = "#";
// statsPageItem.className = "nav_link";
// statsPageItem.innerHTML = "<i class='bx bx-bar-chart-alt-2 nav_icon'></i> <span class='nav_name'>Stats</span>";

// //Appending all pages item to sidebar
// navBar[0].appendChild(homePageItem);
// navBar[0].appendChild(participantsPageItem);
// navBar[0].appendChild(regexPageItem);
// navBar[0].appendChild(bookmarkPageItem);
// navBar[0].appendChild(filesPageItem);
// navBar[0].appendChild(statsPageItem);

document.addEventListener("DOMContentLoaded", function (event) {

    const showNavbar = (toggleId, navId, bodyId, headerId) => {
        const toggle = document.getElementById(toggleId),
            nav = document.getElementById(navId),
            bodypd = document.getElementById(bodyId),
            headerpd = document.getElementById(headerId);

        // Validate that all variables exist
        if (toggle && nav && bodypd && headerpd) {
            toggle.addEventListener('click', () => {
                // show navbar
                nav.classList.toggle('show');
                // change icon
                toggle.classList.toggle('bx-x');
                // add padding to body
                bodypd.classList.toggle('body-pd');
                // add padding to header
                headerpd.classList.toggle('body-pd');
            })
        }
    }

    showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header');

    /*===== LINK ACTIVE =====*/
    const linkList = document.querySelectorAll('.nav_link');

    // function changeActiveLink() {
    //     const activeLink = document.querySelectorAll('.active');
    //     activeLink[0].classList.remove('active');
    //     this.classList.add('active');
    //     linkList.forEach(l => { console.log(l.outerHTML) });

    // }
    // linkList.forEach(l => { l.addEventListener('click', changeActiveLink); });


    linkList.forEach(l => {
        if (l.href === window.location.href) {
            const activeLink = document.querySelectorAll('.active');
            activeLink[0].classList.remove('active');
            l.classList.add('active');
        }
    });

    //console.log("The URL of this page is: " + window.location.href);

    // Your code to run since DOM is loaded and ready
});

