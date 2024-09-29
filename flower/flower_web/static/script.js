const selectImage = document.querySelector('.select-image');
const inputFile = document.querySelector('#file');
const imgArea = document.querySelector('.img-area');
const submitBtn = document.querySelector('#submit');
const outputField = document.querySelector('#output input');
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Get the CSRF token

selectImage.addEventListener('click', function () {
    inputFile.click();
});

inputFile.addEventListener('change', function () {
    const image = this.files[0];
    if (image.size < 200000000000) {
        const reader = new FileReader();
        reader.onload = () => {
            const allImg = imgArea.querySelectorAll('img');
            allImg.forEach(item => item.remove());
            const imgUrl = reader.result;
            const img = document.createElement('img');
            img.src = imgUrl;
            imgArea.appendChild(img);
            imgArea.classList.add('active');
            imgArea.dataset.img = image.name;
        };
        reader.readAsDataURL(image);
    } else {
        alert("Image size more than 2GB");
    }
});

submitBtn.addEventListener('click', async function () {
    const formData = new FormData();
    const realClassField = document.querySelector('.tt');
    
    // Append CSRF token to form data
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('image', inputFile.files[0]); // Add the image file to the form data
    formData.append('real_class', realClassField.value);

    const response = await fetch('/', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    outputField.value = data.class_idx; // Assuming your backend returns a JSON response
});

  