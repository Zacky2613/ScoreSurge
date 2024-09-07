



// Code for modal period content
document.getElementById("planner-add-onto").addEventListener("submit", function(event) {
    // Becuase the id's are be an unknown length we iterate through all of them
    const period_content_elements = document.querySelectorAll("[id^='period-content-']");
    console.log(period_content_elements)

    period_content_elements.forEach(function(period_element, index) {
        const period_content = period_element.innerHTML;
        console.log("content: " + period_content)
        const hidden_content_input = document.getElementById("hidden-period-content-" + (index+1));
        // console.log(index)

        hidden_content_input.value = period_content
        // console.log(note_content_input.value)
    });


    console.log("out of the for loop!")
    // remove pressing enter
    // event.preventDefault();
});