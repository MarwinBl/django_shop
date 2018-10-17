$(document).ready(function () {
    $('.action').click(function (event) {
        event.preventDefault();
        let url = $(this).attr('href');
        $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {
                basket_refresh(data.basket);
            },
            error: function f(data) {
                let newDoc = document.open("text/html", "replace");
                newDoc.write(data.responseText);
                newDoc.close();
        }
        });
    })
});