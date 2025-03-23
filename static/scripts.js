// Upload Functionality
document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();
    let formData = new FormData(this);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let statusDiv = document.getElementById("uploadStatus");
        statusDiv.innerHTML = "<h4>Upload Status:</h4>";
        data.uploads.forEach(file => {
            let message = `<p>${file.filename} - ${file.status}</p>`;
            statusDiv.innerHTML += message;
        });
    })
    .catch(error => {
        console.error("Upload failed:", error);
        document.getElementById("uploadStatus").innerHTML = "<p style='color: red;'>Upload failed!</p>";
    });
});

// Filter Functionality
document.getElementById("filterForm").addEventListener("submit", function(event) {
    event.preventDefault();
    let formData = new FormData(this);

    fetch("/filter", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let resultsDiv = document.getElementById("results");
        resultsDiv.innerHTML = "<h4>Matching Resumes:</h4>";

        if (data.matching_resumes.length > 0) {
            data.matching_resumes.forEach(resume => {
                resultsDiv.innerHTML += `<p>${resume}</p>`;
            });
        } else {
            resultsDiv.innerHTML += "<p>No matching resumes found.</p>";
        }
    })
    .catch(error => {
        console.error("Filtering failed:", error);
        document.getElementById("results").innerHTML = "<p style='color: red;'>Filtering failed!</p>";
    });
});

// Global variable to store job roles
let jobRoles = {};

// Function to Fetch and Populate Job Roles Dropdown
function updateJobRoles() {
    fetch("/api/job_roles")
        .then(response => response.json())
        .then(data => {
            jobRoles = {}; // Reset jobRoles
            let jobRoleSelect = document.getElementById("job_role");
            jobRoleSelect.innerHTML = '<option value="">Select a Role</option>';

            data.forEach(role => {
                jobRoles[role.title] = role; // Store job roles in a global object

                let option = document.createElement("option");
                option.value = role.title;
                option.textContent = role.title;
                jobRoleSelect.appendChild(option);
            });

            console.log("✅ Job roles loaded successfully!");
        })
        .catch(error => console.error("Error loading job roles:", error));
}

// Function to Populate Must-Have & Nice-To-Have Skills
function updateSkills() {
    let role = document.getElementById("job_role").value;
    let mustHaveContainer = document.getElementById("must_have_list");
    let niceToHaveContainer = document.getElementById("nice_to_have_list");

    mustHaveContainer.innerHTML = "";
    niceToHaveContainer.innerHTML = "";

    if (!role || !jobRoles[role]) return; // Ensure role exists

    let mustHaveSkills = jobRoles[role].must_have;
    let niceToHaveSkills = jobRoles[role].nice_to_have;

    // Ensure skills are treated as arrays
    if (typeof mustHaveSkills === "string") {
        mustHaveSkills = mustHaveSkills.split(",").map(skill => skill.trim());
    }
    if (typeof niceToHaveSkills === "string") {
        niceToHaveSkills = niceToHaveSkills.split(",").map(skill => skill.trim());
    }

    console.log("Must-Have Skills for", role, ":", mustHaveSkills);
    console.log("Nice-To-Have Skills for", role, ":", niceToHaveSkills);

    // Populate Must-Have Skills
    mustHaveSkills.forEach(skill => {
        if (skill) {
            let div = document.createElement("div");
            div.classList.add("form-check");

            let checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.classList.add("form-check-input");
            checkbox.name = "must_have";
            checkbox.value = skill;
            checkbox.id = "must_" + skill.replace(/\s+/g, "_");

            let label = document.createElement("label");
            label.classList.add("form-check-label");
            label.setAttribute("for", checkbox.id);
            label.textContent = skill;

            div.appendChild(checkbox);
            div.appendChild(label);
            mustHaveContainer.appendChild(div);
        }
    });

    // Populate Nice-to-Have Skills
    niceToHaveSkills.forEach(skill => {
        if (skill) {
            let div = document.createElement("div");
            div.classList.add("form-check");

            let checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.classList.add("form-check-input");
            checkbox.name = "nice_to_have";
            checkbox.value = skill;
            checkbox.id = "nice_" + skill.replace(/\s+/g, "_");

            let label = document.createElement("label");
            label.classList.add("form-check-label");
            label.setAttribute("for", checkbox.id);
            label.textContent = skill;

            div.appendChild(checkbox);
            div.appendChild(label);
            niceToHaveContainer.appendChild(div);
        }
    });
}

// Event Listener for Job Role Selection
document.getElementById("job_role").addEventListener("change", updateSkills);

// Load Job Roles on Page Load
document.addEventListener("DOMContentLoaded", function () {
    updateJobRoles();
});
