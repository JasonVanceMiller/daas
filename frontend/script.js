// loading the shared banner
fetch("banner.html")
    .then(response => response.text())
    .then(data => {
        document.getElementById('banner_container_id').innerHTML = data;

        // This is a little annoying because if you just insert the html into the dom it won't run the javascript, so we have to do it manually.
        const script = document.createElement('script');
        script.src = 'banner.js';
        document.body.appendChild(script); // Append the script to the bodyk
    })
    .catch(error => console.error('Error loading banner:', error));
