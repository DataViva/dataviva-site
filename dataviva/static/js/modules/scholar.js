$(document).ready(function(){
    setAlertTimeOut(8000);
});

function handleChange(e) {
    let arrayItens = []
    let itens = document.querySelectorAll(".checkBoxes [type=checkbox]:checked")
    for(let item of itens) {
        arrayItens.push(Number(item.id));
    }

    let page_url = window.location.href;
    base_url = page_url.split("://")[1].split("/")[0];

    window.location.href = `/${dataviva.language}/scholar/${arrayItens.length != 0 ? `?keyword=${arrayItens}` : ""}`;
}

$(function() {
    $('#search-form').submit(function() {
        let arrayItens = []
        let itens = document.querySelectorAll(".checkBoxes [type=checkbox]:checked")
        for(let item of itens) {
            arrayItens.push(Number(item.id));
        }

        if ($(this).find('input').val())
            window.location.href = '/' + dataviva.language + `/scholar/?${arrayItens.length != 0 ? `keyword=${arrayItens}&` : ""}search=` + $(this).find('input').val().replace(' ', '+');
        else
            window.location.href = '/' + dataviva.language + `/scholar${arrayItens.length != 0 ? `/?keyword=${arrayItens}` : ""}`;
        return false;
    });
});