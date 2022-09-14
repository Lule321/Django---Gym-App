
$(document).ready(function (){
    $(".Tplan-kartica").on("click", function (){
        let ID = $(this).parent().attr("id");
        $(this).hide(1000);
        $(".Tplan-lista").filter("#V" + ID).show(2000);
    });
    $(".Tplan-lista").on("click", function (){
        let ID = $(this).parent().attr("id");
        $(this).hide(1000);
        $(".Tplan-kartica").filter("#T" + ID).show(2000);
    });
});