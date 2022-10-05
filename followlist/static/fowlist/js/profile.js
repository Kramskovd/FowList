$(document).ready(function(){
    var url_is_done_point = document.location.href + 'is_done';
    var url_delete_list = document.location.href + 'delete_list';
    var url_get_edit_list = document.location.href + 'get_edit_list';
    $("#cancel-edit-list").on("click", function(event){
        $("#container-edit-list").css({"display": "none"});
    });
    $(".point-checklist").on("click", function(event){
        $.get(
            url_is_done_point,
            {'type': 'checklist', 'point_id': $(event.target).attr('value')}
        )
    });
    $(".point-goal").on("click", function(event){
        $.get(
            url_is_done_point,
            {'type': 'goal', 'point_id': $(event.target).attr('value')}
        )
    });
    $(".delete").on("click", function(event){
        var delete_id = $(event.target).attr('id');
        delete_id = delete_id.match(/\d+/g)[0];
        var type = $(event.target).parent().attr('class');
        $.get(
            url_delete_list,
            {'type': type, 'id': delete_id}
        ).done(function(data){
            if(data['is_deleted'] == 'True'){
                $($(event.target).parent()).parent().remove();
            }else{
                alert('Ошибка!');
            }
        })

    });
    $(".edit").on("click", function(event){
        var edit_id = $(event.target).attr('id');
        edit_id = edit_id.match(/\d+/g)[0];
        $.get(
            url_get_edit_list,
            {'id': edit_id}
        ).done(function(data){
            $(".container-edit-list-points").empty();
            $("#input-edit-list-name").attr('value', data["name_list"]);
            $("#pklist").append("<input name='pklist' type='hidden' id='pk-list-input' value='"+ String(data["list_id"]) +"'>");
            var points = data["points"];
            for(item in points){
                point = "<li><input name='point["+ String(item) +"]' class='input-edit-list-point' type='text' value='" + points[item] + "'></li>";
                $(".container-edit-list-points").append(point);
            }
             $("#container-edit-list").css({"display": "block"});
        })
    });
});
