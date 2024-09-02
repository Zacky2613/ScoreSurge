
var modal = document.getElementById("classModal");

var btn = document.getElementById("add-btn");

var span = document.getElementsByClassName("close")[0];

document.getElementById("add-btn").onclick = function() {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


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


// This is for the textboxes in the NOTES area

// Changes fonts with the selector
function changeFont(font) {
    if (font) {
        // It's depracted but it works so idc
        document.execCommand("fontName", false, font);
    }
}

function formatText(command) {
    document.execCommand(command, false, null);
}


// MY OWN JS | IT WORKS YIPPIE

const format_button = document.querySelectorAll("#text-format-btn");

format_button.forEach(button => {
    button.addEventListener("click", function(event) {
        button.classList.toggle("active")
    });
});


// If ctrl+s is pressed it'll save.
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 's') {

        // Preven the broswer save .html thingy
        event.preventDefault();

        // Without this, the save is blank (moving the note stuff from div to input field)
        document.getElementById('note-content').value = document.getElementById('editor').innerHTML;
        document.getElementById('note-form').submit(); // Trigger form submission
    }
});


// Handling chaning toolbar width when textbox one changes from user resize
function adjustToolbar() {
    const editor = document.getElementById("editor");
    const toolbar = document.querySelector(".toolbar");

    // Changing the toolbar width
    // Why the -20? I honestly don't know, it stops the overhand with the toolbar
    toolbar.style.width = editor.clientWidth-20 + "px";
}

// Function to handle resizing of the editor
function handleResize() {
    const editor = document.getElementById("editor");

    // ResizeObserver() is to watch for changes in size, passed through
    // as any argument
    let resise_observer = new ResizeObserver(() => {
        adjustToolbar();
    });

    // Like here
    resise_observer.observe(editor);
}

// On page load initalize a function to be 
window.onload = function() {
    handleResize();
};

// Also, handle cases where the window is resized
window.onresize = function() {
    adjustToolbar();
};


document.getElementById('note-form').addEventListener('submit', function() {
    const editorContent = document.getElementById('editor').innerHTML;

    document.getElementById('note-content').value = editorContent;
});
