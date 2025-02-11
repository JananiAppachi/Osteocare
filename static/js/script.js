const slides = document.querySelector(".slides");
const slideImages = document.querySelectorAll(".slides img");

document.documentElement.style.setProperty("--total-slides", slideImages.length);


let index = 0;
const totalSlides = slideImages.length;

// Auto-slide function
function nextSlide() {
    index++;

    // If at the last image, reset instantly to the first image (prevents blank space)
    if (index >= totalSlides) {
        slides.style.transition = "none";  // Remove animation
        slides.style.transform = `translateX(0%)`; 
        index = 0;
        
        // Small delay before resuming normal sliding
        setTimeout(() => {
            slides.style.transition = "transform 1s ease-in-out";
        }, 50);  
        return;
    }

    // Move the slides properly
    slides.style.transform = `translateX(-${index * 100}%)`;
}

// Slide every 3 seconds
setInterval(nextSlide, 3000);







document.getElementById('xrayUpload').addEventListener('change', function (event) {
    let file = event.target.files[0];
    if (file) {
        let reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('uploadedImage').src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
});

function uploadImage() {
    let fileInput = document.getElementById("xrayUpload");
    let file = fileInput.files[0];

    if (!file) {
        alert("Please select an image first!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("prediction").innerText = "Error: " + data.error;
        } else {
            document.getElementById("prediction").innerText = "Prediction: " + data.prediction;
        }
    })
    .catch(error => {
        document.getElementById("prediction").innerText = "Error: " + error.message;
    });
}

