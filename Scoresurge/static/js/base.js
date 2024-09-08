
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
        const button = event.target.closest("button");
        
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
document.addEventListener("DOMContentLoaded", function() {

    // Becuase there's more than one dropdown mean, must use all.
    const dropdownToggles = document.querySelectorAll(".dropdown-toggle");

    // Loop through each dropdown toggle
    dropdownToggles.forEach(toggle => {
        const dropdown = toggle.parentElement;
        const dropdownContent = dropdown.querySelector(".dropdown-content");

        toggle.addEventListener("click", function() {
            // Toggle the active class
            dropdown.classList.toggle("active");

            // Adjust the dropdown content's max height for smooth transition
            if (dropdown.classList.contains("active")) {
                dropdownContent.style.maxHeight = dropdownContent.scrollHeight + "px";
            } else {
                dropdownContent.style.maxHeight = 0;
            }
        });
    });
});



// TRACKING USER TIME FOR STUDY TRACKER

var start_time, end_time;

// Record the time the user enters the page
window.addEventListener("load", function() {
    start_time = new Date();
});

// Record the time the user leaves the page or closes it
window.addEventListener("beforeunload", function() {
    var class_name = document.body.getAttribute("data-class-name");
    var time_spent = new Date() - start_time;
    // Grab the date (e.g: 9/7/24)
    var current_date = new Date().toLocaleDateString();


    // Calculate the time difference in milliseconds
    var form_data = new FormData();
    form_data.append("time_spent", time_spent)
    form_data.append("time_date", current_date)
    form_data.append("class_name", class_name)

    console.log("User spent " + (time_spent / 1000) + " seconds on the page.");
    
    // Optionally, you can send the time spent to your backend via AJAX
    navigator.sendBeacon("/track_time", form_data);
});