// JavaScript for dynamically adding and removing forms
function cloneFormset(containerId, prefix) {
    const container = document.getElementById(containerId);
    const totalForms = document.querySelector(`#id_${prefix}-TOTAL_FORMS`);

    if (!totalForms) {
        console.error(`Management form for prefix '${prefix}'.`);
        return;
    }

    const emptyForm = container.querySelector(`.${prefix}-empty-form`);
    if (!emptyForm) {
        console.error(`Empty form for prefix '${prefix}' not found.`);
        return;
    }

    const formCount = parseInt(totalForms.value);
    const newForm = emptyForm.cloneNode(true);
    newForm.classList.remove("d-none");

    // Update IDs and names
    newForm.innerHTML = newForm.innerHTML.replace(
        new RegExp(`${prefix}__prefix__`, "g"),
        `${prefix}-${formCount}`
    );

    // Clear input values
    newForm.querySelectorAll("input, textarea, select").forEach(input => {
        input.value = "";
    });

    // Append the new form before the add button
    const addButton = container.querySelector(`#add-${prefix}`);
    container.insertBefore(newForm, addButton);

    // Increment the total forms count
    totalForms.value = formCount + 1;
}

// Add Additional Image
document.getElementById("add-additional_images").addEventListener("click", () => {
    cloneFormset("additional-images", "additional_images"); 
});

// Add Product Detail
document.getElementById("add-details").addEventListener("click", () => {
    cloneFormset("product-details", "details");
});
