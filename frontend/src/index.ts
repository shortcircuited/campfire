document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("testbtn").addEventListener("click", () => {
        fetch("http://localhost:3000/test")
        .then(response => response.json())
        .then(data => {
            if(data.error){
                let test = document.getElementById("testreturn");
                test.innerHTML = `<p>${data.error}</p>`;
                console.error(data.error);
            }
            else{
                let test = document.getElementById("testreturn");
                test.innerHTML = `<p>${data.error}</p>`;
                console.log(data.error);
            }
        })
        .catch(error => {
            console.error(error);
        })
    })










    let div1 = document.getElementById('div1');
    div1.innerHTML = '<p>This is a test element</p>';
    console.log("page loaded");
});