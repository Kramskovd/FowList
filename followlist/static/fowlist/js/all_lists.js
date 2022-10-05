$(document).ready(function(){
    var url = document.location.href + "add-checklist";

    $('.default-list').on('click', function(event){
        list_pk = $('.add-list').attr('id').match(/\d+/g)[0];
        $.get(url, {'list_pk': list_pk}).done(function(data){
            if(data['is_added'] == 'true'){
                $($(event.target).parent()).parent().remove();
            }else{
                alert(data['error']);
            }
        });
    })
});
