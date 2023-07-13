
const url = location.href;

const title = $('#title').text();

const button = document.getElementById('share-button');
button.value = url;

button.onclick = () => {
    if (navigator.share) {
        navigator.share({
            title: `${title}`,
            text: 'Confira esse notícia de Dataviva!',
            url: url,
        })
            .catch((error) => console.log('Error sharing', error));
    } else {
        var tempInput = document.createElement("input");
        tempInput.value = button.value;
        document.body.appendChild(tempInput);
        
        tempInput.select();
        tempInput.setSelectionRange(0, 99999); /* Para dispositivos móveis */
        document.execCommand("copy");
        
        document.body.removeChild(tempInput);
        alert('Link copiado para a área de transferência!');
        console.log('Navigator object not supported on this browser, do it the old way.');
    }
}

