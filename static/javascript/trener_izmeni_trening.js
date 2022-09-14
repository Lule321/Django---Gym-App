$(document).ready(function(){

    let izmeni = 0;
   // let submit = true;

    $("#forma-pretraga").on('submit',function(){
        $("#pretrazene-vezbe-div").html("Ucitavam");
        let pretraga = $("#input-vezbe").val();
        $.ajax({
            method:'POST',
            url:'pretraga/',
            data:{
                pretraga:$('#input-vezbe').val(),
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(result){
                let pretrazene_div = $("#pretrazene-vezbe-div");
                pretrazene_div.html("");
                for(let i = 0; i < result.length; i++)
                {
                    novi_div = $("<div></div>");
                    novi_div.addClass("col-md-4").addClass("col-12");
                    //novi_div.html(result[i].slika)

                    div_card = $("<div></div>");
                    div_card.addClass("card");
                    div_card.attr("id", result[i].id);
                    div_card.attr("name", result[i].naziv);
                    //div_card.attr("style", "width:auto; height:50%;")

                    card_img_top = $("<img>");
                    card_img_top.addClass("card-img-top");
                    card_img_top.attr("src", "../../../media/" +  result[i].slika);
                    card_img_top.attr("alt", "Ne radi!");
                    card_img_top.attr("width", "250vh");
                    card_img_top.attr("height", "250vh");

                    card_title = $("<h3></h3>");
                    card_title.addClass("card-title");
                    card_title.html(result[i].naziv);


                    div_card_body = $("<div></div>");
                    div_card_body.addClass("card-body");
                    
                    div_card_body.append(card_title);
                    div_card.append(card_img_top);
                    div_card.append(div_card_body);
                    
                    novi_div.append(div_card);

                    pretrazene_div.append(novi_div);
                }

                $(".card").click(function(){
                    if(izmeni != 0){
                        let id = $(this).attr("id");
                        let name = $(this).attr("name");
                        $("#stavka-vezbaId-" + izmeni).val(id);
                        $("#vezba-" + izmeni).val(name);
                    }
                });
            }
        });

    });



    $("#izmeni-vreme").click(function(){
        $("#vreme").removeAttr("readonly");
        $("#vremePromena").val("true");
    });

    $(".izmeni-stavku").click(function(){
        izmeniDugme(this);
    });

    function izmeniDugme(kliknut)
    {
        if(izmeni != 0)
        {
            $("#redniBroj-" + izmeni).attr("readonly","");
            $("#brojPonavljanja-"+izmeni).attr("readonly", "");
            $("#tezina-" + izmeni).attr("readonly", "");
        }
        let idKliknuto = $(kliknut).attr("id");
        let tmp = idKliknuto.split("-");
        let broj = tmp[2];
        izmeni = broj;
        $("#redniBroj-" + broj).removeAttr("readonly");
        $("#brojPonavljanja-"+broj).removeAttr("readonly");
        $("#tezina-" + broj).removeAttr("readonly");
        $("#promena-"+broj).val("true");
    }

    function izbrisi(kliknut)
    {
        let idKliknuto = $(kliknut).attr("id");
        let tmp = idKliknuto.split("-");
        let broj = tmp[2];
        let mojRedniBroj = parseInt($("#redniBroj-" + broj).val());
        if(izmeni == broj)
        {
            izmeni = 0;
        }

        let brojStavki = parseInt($("#brojStavki").val());
        for(let i = 1; i <= brojStavki; i++)
        {
            let trenutniBrojStavke = $("#redniBroj-" + i).val();
            if(trenutniBrojStavke == undefined) continue;
            trenutniBrojStavke = parseInt(trenutniBrojStavke);
            if(trenutniBrojStavke > mojRedniBroj){
                trenutniBrojStavke -= 1;
                $("#redniBroj-" + i).val(trenutniBrojStavke);
                $("#promena-" + i).val("true");
            }
        }

        $("#col-" + broj).remove();
    }

    //ovo ne treba ovde
    $(".card").click(function(){
        if(izmeni != 0){
            let id = $(this).attr("id");
            let name = $(this).attr("name");
            let prosliBroj = parseInt($("#stavka-vezbaId-" + izmeni).val());
            $("#stavka-vezbaId-" + izmeni).val(id);
            $("#vezba-" + izmeni).val(name);
        }
    });

    $("#dodaj-stavku").click(function(){
        let brojStavki = parseInt($("#brojStavki").val());
        brojStavki += 1; 
        $("#brojStavki").val(brojStavki);
        let div = $("<div></div>").addClass("col-12");
        div.attr("id", "col-" + brojStavki);

        let label = $("<label></label>")
                    .attr("for", "redniBroj-" + brojStavki)
                    .html("Redni broj:&nbsp;");
        let input = $("<input>")
                    .attr("type", "number")
                    .val(brojStavki)
                    .attr("id", "redniBroj-" + brojStavki)
                    .attr("name", "redniBroj-" + brojStavki)
                    .attr("size", "8")
                    .attr("readonly", "")
                    .addClass("bitna-polja")
                    .addClass("redniBrojevi");


        

        div.append(label).append(input);
        div.append("&nbsp;");
        label = $("<label></label>")
            .attr("for", "brojPonavljanja-" + brojStavki)
            .html("Broj ponavljanja:&nbsp;");

        input = $("<input>")
                .attr("type", "text")
                .val("")
                .attr("id", "brojPonavljanja-" + brojStavki)
                .attr("name", "brojPonavljanja-" + brojStavki)
                .attr("size", "10")
                .attr("readonly", "");

        div.append(label).append(input);
        div.append("&nbsp;");

        label = $("<label></label>")
        .attr("for", "vezba-" + brojStavki)
        .html("Vezba:&nbsp;");

        input = $("<input>")
            .attr("type", "text")
            .val("")
            .attr("id", "vezba-" + brojStavki)
            .attr("name", "vezba-" + brojStavki)
            .attr("size", "18")
            .attr("readonly", "")
            .attr("required", true);

        div.append(label).append(input);
        div.append("&nbsp;");

        label = $("<label></label>")
        .attr("for", "tezina-" + brojStavki)
        .html("Tezina:&nbsp;");

        input = $("<input>")
            .attr("type", "text")
            .val("")
            .attr("id", "tezina-" + brojStavki)
            .attr("name", "tezina-" + brojStavki)
            .attr("size", "18")
            .attr("readonly", "");

        div.append(label).append(input);
        div.append("&nbsp;");

        input = $("<input>")
        .attr("type", "hidden")
        .val("true")
        .attr("id", "promena-" + brojStavki)
        .attr("name", "promena-" + brojStavki);
        div.append(input);

        input = $("<input>")
        .attr("type", "hidden")
        .val("true")
        .attr("id", "promena-" + brojStavki)
        .attr("name", "promena-" + brojStavki);
        div.append(input);

        input = $("<input>")
        .attr("type", "hidden")
        .val("-1")
        .attr("id", "stavka-vezbaId-" + brojStavki)
        .attr("name", "stavka-vezbaId-" + brojStavki)
        .addClass("stavka-vezbeId");
        div.append(input);

        let button = $("<button></button>")
        .addClass("btn").addClass("btn-primary").addClass("izmeni-stavku")
        .attr("type", "button")
        .html("Izmeni")
        .attr("id", "izmeni-stavku-" + brojStavki);
        div.append(button);

        button.click(function(){
            izmeniDugme(this);
        });

        button = $("<button></button>")
        .addClass("btn").addClass("btn-primary").addClass("izbrisi-stavku")
        .attr("type", "button")
        .html("Izbrisi")
        .attr("id", "izbrisi-stavku-" + brojStavki);
        div.append(button);

        button.click(function(){
            izbrisi(this);
        });

       // submit = false;
       // $("#submit").attr("readonly", "");


        $("#form-sacuvaj-izmene").append(div);

    });

    $(".izbrisi-stavku").click(function(){
        izbrisi(this);
    });

});

function validateForm(){
    let brojStavki = parseInt($("#brojStavki").val());
    let redniBrojString = "#redniBroj-";
    let vezbaIdString = "#stavka-vezbaId-";
    let brojBrojeva = $(".redniBrojevi").length;
    let nizRednihBrojeva = [];
    for(let i = 0; i < brojBrojeva; i++)
    {
        nizRednihBrojeva.push(0);
    }

    for(let j = 1; j <= brojStavki; j++)
    {
        let tmp = $(redniBrojString + j);
        if(tmp.val() == undefined) continue;

        let trenutniBroj = parseInt(tmp.val());
        if(trenutniBroj <= 0 || nizRednihBrojeva.length < trenutniBroj || nizRednihBrojeva[trenutniBroj - 1] > 0)
        {
            alert("Redni brojevi ne idu po redu");
            return false;
        }
        nizRednihBrojeva[trenutniBroj - 1] += 1;

        let trenutniIdVezbe = parseInt($(vezbaIdString + j).val());

        if(trenutniIdVezbe == - 1)
        {
            alert("Nije unesena vezba u sva polja");
            return false;
        }
    }

    for(let i = 0; i < nizRednihBrojeva.length; i++)
    {
        if(nizRednihBrojeva[i] == 0)
        {
            alert("Nisu tu svi redni brojevi");
            return false;
        }
    }
    return true;
}