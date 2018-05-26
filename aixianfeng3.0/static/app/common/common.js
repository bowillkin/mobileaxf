

function addnum(good_id){
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/users/addnum/',
        type:'POST',
        data:{'good_id': good_id},
        dataType:'json',
        headers:{'X-CSRFToken': csrf},
        success:function(msg){
            console.log(msg);
            $('#num_' + good_id).html(msg['c_num'])
        },
        error:function(msg){
            alert('请求失败')
        }
    })
}

function subnum(good_id){
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/users/subnum/',
        type:'POST',
        data:{'good_id': good_id},
        dataType:'json',
        headers:{'X-CSRFToken': csrf},
        success:function(msg){
            console.log(msg);
            $('#num_' + good_id).html(msg['c_num'])
        },
        error:function(msg){
            alert('请求失败')
        }
    })
}