$(document).ready(() => {

    const url = location.pathname;

    const title = $('#title').text();

    $('#share-button').on('click', () => {
        if (navigator.share) {
            navigator.share({
                title: `${title}`,
                text: 'Confira esse notícia de Dataviva!',
                url: url,
            })
                .catch((error) => console.log('Error sharing', error));
        } else {
            console.log('Share not supported on this browser, do it the old way.');
        }
    });
})

