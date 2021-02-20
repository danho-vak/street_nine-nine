// Modal을 닫으면 그 안에 있던 form 내용 비움
    $('#staticBackdrop').on('hidden.bs.modal', function (e) {
        $('#form_in_modal').empty();
    })

    // checkbox 선택된 값이 있는지 확인
    function isChecked(object_type){
        var checked_item = ''

        if (object_type == 'thumbnail') {
            checked_item = $('input[name=thumbnail_checkbox]:checked');
        } else if (object_type == 'detail_image') {
            checked_item = $('input[name=detail_image_checkbox]:checked');
        }

        if (checked_item.length > 0) {
            return checked_item;
        } else {
            return false;
        }
    }

    // Modal안에 input object를 추가하고 view로 PK와 이미지 파일을 넘김
    function openModal(object_type){
        var checked_item = isChecked(object_type);

        if (checked_item) {
            var result = confirm("정말 수정할까요? 기존 이미지는 삭제되며, 되돌릴 수 없습니다!");

            if (result) {
                checked_item = isChecked(object_type);

                $('.modal-body').append('<input type="hidden" name="object_type" value="'+object_type+'">');

                for (var i=0; i<checked_item.length; i++){
                    target_object_pk = checked_item[i].value;
                    $('.modal-body').append('<input type="hidden" name="modal_input_hidden" value="'+target_object_pk+'">');
                    $('.modal-body').append('<input type="file" name="modal_input_file" accept="image/*" id="modal_input_'+target_object_pk+'">');
                }

                $('#staticBackdrop').modal('show');  // Modal open
            }
        } else {
            alert('수정할 이미지를 선택해주세요!');
        }
    }

    // view로 선택된 이미지의 PK를 넘겨줌
    function imageDelete(object_type) {
        var checked_item = isChecked(object_type);

        if (checked_item) {
            var result = confirm("해당 이미지를 정말 삭제하시겠어요?");

            if (result) {
                var target_pk_list = []

                if (object_type == 'thumbnail') {
                    checked_item = $('input[name=thumbnail_checkbox]:checked');
                } else if (object_type == 'detail_image') {
                    checked_item = $('input[name=detail_image_checkbox]:checked');
                }

                for (var i=0; i<checked_item.length; i++) {
                    target_pk_list.push(checked_item[i].value);
                }

                $.post(delete_url ,
                        {
                            'csrfmiddlewaretoken' : csrftoken,
                            'object_type': object_type,
                            'target_pk_list': target_pk_list
                        }, function() {
                            alert('삭제완료!');
                            location.reload();
                        });
            }
        } else {
            alert('삭제할 이미지를 선택해주세요!');
        }

    }