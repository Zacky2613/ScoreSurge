
// NOTES.JS:
// Handles all functionality relating to notes

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


const format_button = document.querySelectorAll("#text-format-btn");

format_button.forEach(button => {
    button.addEventListener("click", function(event) {
        button.classList.toggle("active")
    });
});


// If ctrl+s is pressed it'll save.
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 's') {
        // Prevent the broswer save .html thingy
        event.preventDefault();

        // Without this, the save is blank (moving the note stuff from div to input field)
        document.getElementById('note-content').value = document.getElementById('editor').innerHTML;
        document.getElementById('note-form').submit(); // Trigger form submission
    }
    
    else if (event.key == "Tab") {
        // TOOD: GET TAB WORKING
    }
});


// Handling chaning toolbar width when textbox one changes from user resize
function adjustToolbar() {
    const editor = document.getElementById("editor");
    const toolbar = document.querySelector(".toolbar");

    // Changing the toolbar width
    toolbar.style.width = editor.clientWidth + "px";
}

// Function to handle resizing of the editor
function handleResize() {
    const editor = document.getElementById("editor");

    // ResizeObserver() is to watch for changes in size,-
    // passed through as any argument
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


document.getElementById("note-form").addEventListener("submit", function() {
    const editorContent = document.getElementById("editor").innerHTML;

    document.getElementById("note-content").value = editorContent;
});