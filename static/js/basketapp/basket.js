window.onload = function () {
    function refresh_del_all(element, value){
        let href = $(element).attr('href');
        let list_href = href.split('/');
        list_href[list_href.length-1] = value;
        $(element).attr('href', list_href.join('/'));
    }
    $('.card').on('click', '.action', function () {
        event.preventDefault();
        let elem = event.target;
        let del_all = $(elem).parents('.card').find('.del-all');
        let url = elem.getAttribute('href');
        $.ajax({
            url: url,
            dataType: 'json',
            success: function (data) {
                let quantity_block = $('#'+data.name);
                quantity_block.html(data.quantity);
                basket_refresh(data.basket);
                refresh_del_all(del_all, data.quantity);
                if (data.quantity === 0){
                    quantity_block.parents('.card').remove();
                }
            },
        });
    });
};