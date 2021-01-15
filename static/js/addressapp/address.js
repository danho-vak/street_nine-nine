function setDefaultAddress(){
    address_pk = $('input[type=checkbox]:checked').val();
    name = $('input[type=checkbox]:checked').parent().siblings('#alias').text()

    confirm = confirm('"'+name+'"를 기본 배송지로 설정할까요?');

    if (confirm) {
        $.ajax({
            url : '/addresses/update/'+address_pk+'/',
            type : 'post',
            data : {
                csrfmiddlewaretoken : csrftoken,
                address_pk : address_pk
                },
            success : function(data){
                alert('수정 완료');
                location.reload();
            }, error : function(err, status) {
                alert(err+' : '+status);
            }
        });
    }
}

function deleteAddress() {
    address_pk = $('input[type=checkbox]:checked').val();
    name = $('input[type=checkbox]:checked').parent().siblings('#alias').text()

    confirm = confirm('배송지 "'+name+'"를 삭제할까요?');

    if (confirm) {
        $.ajax({
            url : '/addresses/delete/'+address_pk+'/',
            type : 'post',
            data : {
                csrfmiddlewaretoken : csrftoken,
                address_pk : address_pk
                },
            success : function(data){
                alert('삭제 완료');
                location.reload();
            }, error : function(err, status) {
                alert(err+' : '+status);
            }
        });
    }
}