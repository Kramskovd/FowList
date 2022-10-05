$(document).ready(function(){
    click_point = 1;
    $(".points").append("<li><input class='input-point' type='text' name='point' placeholder='пункт' id='point_"+ click_point + "'></li>");
    $("#create-point").on('click', function(){
        click_point++;
        $(".points").append("<li><input class='input-point' type='text' placeholder='пункт' name='point' id='point_" + click_point + "'></li>");
    })
});
