$(document).ready(function () {
    let csrftoken = '';
    let parent_class = '';
    let parent = '';
    let name = '';
    let object = '';
    let action = '';
    let url = '';

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function fill_modal(action, name){
        if(action==='del'){
            $('#modal-body').text('Уверены, что хотите удалить '+name);
            $('#modal-button').text('Удалить');
        }else if(action==='restore') {
            $('#modal-body').text('Уверены, что хотите восстановить '+name);
            $('#modal-button').text('Восстановить');
        }
    }

    function change_block(parent, action){
        if(action==='del'){
            $(parent).addClass('disabled');
            $(parent).find('a[action="del"]').attr('action', 'restore').text('восстановить');
        }else if(action==='restore'){
            $(parent).removeClass('disabled');
            $(parent).find('a[action="restore"]').attr('action', 'del').text('удалить');
        }
    }


    $('#modal-button').click(function () {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });

        $.ajax({
            url: url,
            method: 'POST',
            data: {
                action: action,
                object: object,
            },
            success: function (data) {
                if (data.status===true){
                    $('#ModalCenter').modal('hide');
                    change_block(parent, action);
                }else {
                    alert(data.message)
                }
            }
        });
    });

    $('a[action]').click(function (event) {
        csrftoken = getCookie('csrftoken');
        parent_class = $(event.target).attr('parent');
        parent = $(event.target).parents('.'+parent_class);
        name = $(parent).find('#name').text();
        object = $(event.target).attr('object');
        action = $(event.target).attr('action');
        url = $(event.target).attr('url');

        fill_modal(action, name);
        $('#ModalCenter').modal('show');

        event.preventDefault();
    })
});