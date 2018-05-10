

function addnum(good_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/users/addnum/',
        type:'POST',
        headers:{'X-CSRFToken':csrf},
        data:{'good_id':good_id},
        dataType:'json',
        success:function(msg){
            $('#num_'+ good_id).html(msg['c_num'])
            $('#totalprice').html('总价:' + msg['totalprice'])
        },
        error:function(msg){
            alert('请求失败')
        }
    })
}

function subnum(good_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/users/subnum/',
        type:'POST',
        headers:{'X-CSRFToken':csrf},
        data:{'good_id':good_id},
        dataType:'json',
        success:function(msg){
            console.log(msg);
            $('#num_'+ good_id).html(msg['c_num'])
            $('#totalprice').html('总价:' + msg['totalprice'])
        },
        error:function(msg){
            alert('请求失败')
        }
    })
}

function change(good_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/users/change/',
        type:'POST',
        headers:{'X-CSRFToken':csrf},
        data:{'good_id':good_id},
        dataType:'json',
        success:function(msg){
            if(msg['is_select']){
                s = "<span onclick=change({{" + good_id + "}}) id=is_{{" +  good_id + "}}>√</span>"
            }else{
                s = "<span onclick=change({{" + good_id + "}}) id=is_{{" +  good_id + "}}>X</span>";
                $('#selectall').html('　')
            }
            console.log(s);
            $('#is_' + good_id).html(s);
            console.log(msg['totalprice']);
            $('#totalprice').html('总价:' + msg['totalprice'])
        },
        error:function(msg){
            alert('请求失败')
        }
    })
}

function selectall() {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    console.log(csrf);
    $.ajax({
        url:'/users/selectall/',
        type:'POST',
        headers:{'X-CSRFToken':csrf},
        data:{},
        dataType:'json',
        success:function(msg){
            $('span[id*="is_"]').html('√');
            $('#selectall').html('√');
            if(1){
            $('#totalprice').html('总价:' + msg['totalprice'])}
        },
        error:function(msg){
            alert('请求失败')
        }
    })
}

