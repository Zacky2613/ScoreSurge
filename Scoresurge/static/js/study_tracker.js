document.addEventListener("DOMContentLoaded", function() {

    // Becuase there's more than one dropdown mean, must use all.
    const dropdownToggles = document.querySelectorAll(".study-tracker-dropdown-toggle");

    // Loop through each dropdown toggle
    dropdownToggles.forEach(toggle => {
        const dropdown = toggle.parentElement;
        const dropdownContent = dropdown.querySelector(".study-tracker-content");

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