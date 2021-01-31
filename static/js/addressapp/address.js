function setDefaultAddress(){
    if (isChecked()) {
        address_pk = $('input[type=radio]:checked').val();
        name = $('input[type=radio]:checked').parent().siblings('#alias').text()

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
}


function deleteAddress() {
    if (isChecked()) {
        address_pk = $('input[type=radio]:checked').val();
        name = $('input[type=radio]:checked').parent().siblings('#alias').text()

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
}


function isChecked(){
        var checked_item = checked_item = $('input[name=is_default]:checked');

        if (checked_item.length > 0) {
            return checked_item;
        } else {
            alert('배송지를 선택해주세요!');
            return false;
        }
    }