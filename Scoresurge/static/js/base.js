
// BASE.JS:
// Handles all universal functionality


// -=-=-= MODALS -=-=-=

// Modal variables
var class_modal = document.getElementById("class-modal");
var add_to_planner_modal = document.getElementById("add-to-planner-modal");
var planner_modal = document.getElementById("planner-modal");
var edit_grades_modal = document.getElementById("edit-grades-modal");
var modal_close_btn = document.querySelectorAll(".close");

document.querySelectorAll("#add-btn").forEach(button => {
    button.addEventListener("click", function(event) {
        const button = event.target.closest('button');
        
        if (button.className === "add-class-btn") {
            class_modal.style.display = "flex"
        } else if (button.className === "add-to-planner-btn") {
            add_to_planner_modal.style.display = "flex"
        } else if (button.className === "make-planner-btn") {
            planner_modal.style.display = "flex"
        } else if (button.className === "edit-grades-btn") {
            edit_grades_modal.style.display = "flex"        
        }

    });
});


// Click X to close the modal
modal_close_btn.forEach(button => {
    button.addEventListener("click", function(event) {
        try {class_modal.style.display = "none";} catch (e) {}
        try {add_to_planner_modal.style.display = "none";} catch (e) {}
        try { planner_modal.style.display = "none"; } catch (e) {}
        try { edit_grades_modal.style.display = "none"; } catch (e) {}
    });
});


// -=-=-=- DROPDOWNS -=-=-=-=-
document.addEventListener('DOMContentLoaded', function() {

    // Becuase there's more than one dropdown mean, must use all.
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    // Loop through each dropdown toggle
    dropdownToggles.forEach(toggle => {
        const dropdown = toggle.parentElement;
        const dropdownContent = dropdown.querySelector('.dropdown-content');

        toggle.addEventListener('click', function() {
            // Toggle the active class
            dropdown.classList.toggle('active');

            // Adjust the dropdown content's max height for smooth transition
            if (dropdown.classList.contains('active')) {
                dropdownContent.style.maxHeight = dropdownContent.scrollHeight + "px";
            } else {
                dropdownContent.style.maxHeight = 0;
            }
        });
    });
});

