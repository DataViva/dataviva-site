$(function() {
    $('#search-form').submit(function() {
        let arrayItens = []
        let itens = document.querySelectorAll(".checkBoxes [type=checkbox]:checked")
        for(let item of itens) {
            arrayItens.push(Number(item.id));
        }

        if ($(this).find('input').val())
            window.location.href = '/' + dataviva.language + `/blog/?${arrayItens.length != 0 ? `subject=${arrayItens}&` : ""}search=` + $(this).find('input').val().replace(' ', '+');
        else
            window.location.href = '/' + dataviva.language + `/blog${arrayItens.length != 0 ? `/?subject=${arrayItens}` : ""}`;
        return false;
    });
});
