$(document).ready(function(){
    $("#button-pretraga").click(function(){
        let tekst = $("#tekst-pretraga").val()
        if(tekst != ""){
            $("#div-rezultat").html("Ucitavam...");
            
            
            $.ajax({
                method: "POST",
                url: "pretraga/",
                data:{
                    tekst: tekst,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(result)
                {
                    $("#div-rezultat").html("");
                    for(let i = 0; i < result.length; i++)
                    {
                        let card = $("<div></div>");
                        card.addClass("card").addClass("col-md-4").addClass("col-12");

                        let img = $("<img>")
                        img.addClass("card-img-top");
                        img.attr("src", "../../../media/" + result[i].slika);
                        img.attr("alt", "Ne radi!");
                        img.attr("width", "250vh");
                        img.attr("height", "250vh");

                        card.append(img);

                        body = $("<div></div>");
                        body.addClass("card-body");
                        title = $("<h3></h3>");
                        title.addClass("card-title");
                        title.html(result[i].naziv);

                        body.append(title);
                        card.append(body);
                        card.attr("id", result[i].id);
                        card.attr("name", result[i].naziv);

                        $("#div-rezultat").append(card);

                    }

                    $(".card").click(function(){
                        let id = parseInt($(this).attr("id"));
                        let naziv = $(this).attr("name");

                        $("#id-stavka").val(id);
                        $("#naziv").val(naziv);
                    });
                }
            });
    }

    });
});