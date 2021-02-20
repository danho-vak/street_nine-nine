
    // 상품 가지수 별 iamport결제시 출력될 상품명 설정하는 script
    function productCount(){
        var rows = document.getElementsByName('cart_item_checkbox').length;
        var first_product_name = $('table.table.table-borderless > tbody > tr:nth-child(2) > td:nth-child(3) > a').text().trim();
        if (rows > 1) {
            return first_product_name +'외 ' + String(rows-1) + '건'
        } else {
            return first_product_name
        }
    }

    // 새로운 주문을 생성하는 script
    function createOrder(){
        result = {}
        $.ajax({
            url : order_create_url,
            type : 'post',
            dataType : 'json',
            async : false,
            data : {
                'csrfmiddlewaretoken' : csrftoken,
                'address_pk' : $('#user_default_address').val()
            }, success : function (data){
                result['is_saved'] = true;
                result['merchant_uid'] = data['merchant_uid'];
                result['amount'] = data['amount'];

            }, error : function (err, status) {
                alert(err+' : '+status);
            }
        });
        return result  // 주문 object 생성 여부에 따른 결과 리턴
    }

    // 실제 결제된 금액이 맞는지 확인 요청 보내는 script
    function paymentCheck(merchant_uid, amount){
        $.ajax({
            url : payment_check_url,
            type : 'post',
            dataType : 'json',
            data : {
                'csrfmiddlewaretoken' : csrftoken,
                'merchant_uid' : merchant_uid,
                'amount' : amount
            }, success : function (data){
                location.href=order_list_url;
            }, error : function (err, status) {
                alert(err+' : '+status);
            }
        });
    }

    // 사용자가 결제를 취소할 경우 주문 내역을 삭제하는 script
    function paymentError(merchant_uid){
        $.ajax({
            url : payment_error_url,
            type : 'post',
            dataType : 'json',
            data : {
                'csrfmiddlewaretoken' : csrftoken,
                'merchant_uid' : merchant_uid,
            }, success : function (data){
                console.log(data);
            }, error : function (err, status) {
                alert(err+' : '+status);
            }
        });
    }
