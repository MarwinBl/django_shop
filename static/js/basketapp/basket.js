window.onload = function () {
    $('.card').on('click', '.action', function () {
        event.preventDefault();
        let elem = event.target;
        let url = elem.getAttribute('href');
        $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {
                let quantity_block = $('#'+data.name);
                quantity_block.html(data.quantity);
                basket_refresh(data.basket);
                if (data.quantity === 0){
                    quantity_block.parents('.card').remove();
                }
            },
        });
    });
};