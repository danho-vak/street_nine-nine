// submit시 disabled 속성 지우는 script
$('form').submit(function(e){
    $(':disabled').each(function(e){
        $(this).removeAttr('disabled');
    })
});

// 상품 option 등록시 정규표현식을 통해 세미콜론만 받을 수 있도록 걸러내는 script
$('#id_p_product_option_class_2').keyup(function(e) {
    var optionValueCheck = /[~!@\#$%^&*\()\-=+_'\[\]{}]/gi;
    var optionVal = $("#id_p_product_option_class_2");

    if (optionValueCheck.test(optionVal.val())) {
        optionVal.val(optionVal.val().replace(optionValueCheck,""));
    }
});

// product_sale_id를 조합해주는 script
$('#id_product_code').blur(function(e){
    $('#id_product_sale_id').val($('#id_product_id').val() + $('#id_product_code').val());
});


function set_category(data, target_object){

    for (var i=0; i<data.length; i++){
        $('#'+target_object).append('<option value='+data[i].category_code+'>'+data[i].category_name+'</option>');
    }
}

$('#category_select').change(function(){
    category_name = $('#category_select').find(':selected').text();
    $('#category_code_disabled').val(this.value);
    $('#category_code').val(this.value);
});