$(document).ready(function() {
    var selected = [];
    var table = $('#myTable').DataTable({
        "lengthChange": false,
        "paging":false,
        stateSave: true
    });
    var data = table.rows({selected:  true}).data();
    var sData;
    $('#myTable tbody').on( 'click', 'tr', function () {
        var id = this.id;
        var index = $.inArray(id, selected);

        if ( index === -1 ) {
            selected.push( id );
        } else {
            selected.splice( index, 1 );
        }

        $(this).toggleClass('selected');
        data = table.rows('.selected').data();
        newArray=[];
        for(var i=0; i<data.length;i++){
            newArray.push(data[i][2]);
        }
        sData = newArray.join();
        var input = document.createElement("input");
        input.setAttribute("type", "hidden");
        input.setAttribute("id","exclude_users");
        input.setAttribute("name", "exc_users");
        input.setAttribute("value", sData);
        document.getElementById("button").appendChild(input);
        url = window.location.href;
        $.getJSON(url, {sData : sData} , function (sData) {
            var response = sData;
            console.log(response);
        });
    } );

    //alert(data);
    console.log("Data:" + sData);
    //var data = table.rows('.selected').data();
    //console.log( "Data: " + data );

    //return data

    $('#button').click( function () {
        table.rows('.selected').remove().draw( false );
    } );
    yadcf.init(table, [
        {column_number : 0, filter_type: "text", exclude: true},
        {column_number : 1, filter_type: "text", exclude: true},
        {column_number : 2, filter_type: "text"},
        {column_number : 3, filter_type: "text", exclude: true},
        {column_number : 4, filter_type: "text"},
        {column_number : 5, filter_type: "text"},
        {column_number : 6, filter_type: "range_number", sort_as: "num"},
        {column_number : 7, filter_type: "range_number", sort_as: "num"},
        {column_number : 8, filter_type: "range_number", sort_as: "num"},
        {column_number : 9, filter_type: "text"},
        {column_number : 10, filter_type: "text"},
        {column_number : 11, data: ["Yes", "No"], filter_default_label: "Select Yes/No"}
    ]);

} );
