$('.dropdown-toggle').dropdown();

function basket_refresh(data) {
    if (data === null) {
        $('#basket').html('Корзина пуста');
        $('#basket-empty').show();
    } else {
        $('#basket').html('<span id="basket-count" class="badge badge-dark">' + data.count + ' шт</span> /'+
                          ' <span id="basket-summ" class="badge badge-dark">' + data.total_price + ' руб</span>');
    }
}