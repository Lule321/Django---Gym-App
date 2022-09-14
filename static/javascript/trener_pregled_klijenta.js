$(document).ready(function(){

    $("#button-posalji-poruku").click(function(){
        
        let poruka = $("#div-nova-poruka").html();
        $("#div-nova-poruka").html("");
        poruka = skiniDivTagoce(poruka);
        if(poruka.length > 0)
        {
            $(this).attr("disabled", "");
            $("#button-osvezi-chat").attr("disabled", "");
            let novaPoruka = $("<div class='div-poruka'><p class='poruka-moja'>Saljem...</p></div>")
            $(".div-chat").prepend(novaPoruka);





            $.ajax({
                method: 'POST',
                url: 'posalji_poruku/',
                data: {
                    poruka: poruka,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(result){
                    $("#button-posalji-poruku").removeAttr("disabled");
                    $("#button-osvezi-chat").removeAttr("disabled");
                    novaPoruka.remove();
                    for(let i = 0; i < result.length; i++)
                    {
                        let tekst = result[i].tekst.replaceAll("\n", "<br>");
                        if(result[i].tudja == "0")
                        {
                            novaPoruka = $("<div class='div-poruka'><p class='poruka-moja'>" + tekst + "</p></div>")
                        }
                        else
                        {
                            novaPoruka = $("<div class='div-poruka'><p class='poruka-tudja'>" + tekst + "</p></div>")
                        }
                        
                        $(".div-chat").prepend(novaPoruka);
                    }

                }
            });

        }

    });

    $("#button-osvezi-chat").click(function(){
        $("#button-posalji-poruku").attr("disabled", "");
        $("#button-osvezi-chat").attr("disabled", "");
        let novaPoruka = $("<div class='div-poruka'><p class='poruka-moja'>Osvezavam...</p></div>")
            $(".div-chat").prepend(novaPoruka);
        $.ajax({
            method: "POST",
            url: "osvezi_chat/",
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(result)
            {
                $("#button-posalji-poruku").removeAttr("disabled");
                $("#button-osvezi-chat").removeAttr("disabled");
                novaPoruka.remove();
                for(let i = 0; i < result.length; i++)
                {
                    let tekst = result[i].tekst.replaceAll("\n", "<br>");
                    if(result[i].tudja == "0")
                    {
                        novaPoruka = $("<div class='div-poruka'><p class='poruka-moja'>" + tekst + "</p></div>")
                    }
                    else
                    {
                        novaPoruka = $("<div class='div-poruka'><p class='poruka-tudja'>" + tekst + "</p></div>")
                    }
                    
                    $(".div-chat").prepend(novaPoruka);
                }
            }
        });
    });

    function skiniDivTagoce(poruka)
    {
        let povratna = "";
        poruka = poruka.replaceAll("<div>", "");
        poruka = poruka.replaceAll("<br>", "");
        povratna = poruka.replaceAll("</div>", "\n");
        return povratna;
    }

    $(".izbrisi").click(function(){
        let id = $(this).attr("id");
        id = id.split("-");

        let idTreninga = id[1]; 

        $("#td-" + idTreninga).html("");

        $.ajax({
            method: "POST",
            url: "izbrisi/",
            data:{
                id_treninga: idTreninga,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(result){
                //alert(result);
            }
        });
    });

    $(".izbrisi-jelo").click(function(){
        let tmp = $(this).attr("id");
        tmp = tmp.split("-");

        let i = parseInt(tmp[2]);

        $("#td-jelo-" + i).html("");

        $.ajax({
            method: "POST",
            url: "izbrisi_obrok/",
            data:{
                id_obrok: i,
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },

            success: function(result){
                alert(result);
            }
        });

    });
});